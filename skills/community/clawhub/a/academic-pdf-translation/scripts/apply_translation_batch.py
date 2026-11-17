"""把一个翻译批次的结果写回 translation.json。

批次负责执行，校验仍然逐单元进行：ID 必须存在、不得重复、不得修改原文、
数量必须与批次一致、必填锚点不能丢失。任何一项不满足就整批拒绝，
translation.json 保持原样。

每批成功后原子写入并记录状态，因此中断可以从最后一个成功批次继续，
修改第 8 批也不会重新翻译前 7 批。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, load_json, sha256_file, utc_now, write_json
from content_anchors import anchors_present
from plan_translation_batches import PLAN_FILE_NAME, load_plan
from translation_cache import TranslationCache
from translation_truthfulness import evaluate_batch, refresh_coverage

ALLOWED_RESULT_KEYS = {
    "id",
    "translation",
    "keep_source_code",
    "keep_source_reason",
    "review_flags",
}


def _normalize_results(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("results", "units", "translations"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
    if not isinstance(payload, list):
        raise SkillError("批次结果必须是数组，或含 results/units 数组的对象")
    results: list[dict[str, Any]] = []
    for index, item in enumerate(payload, 1):
        if not isinstance(item, dict):
            raise SkillError(f"批次结果第 {index} 项不是对象")
        unknown = set(item) - ALLOWED_RESULT_KEYS
        if unknown:
            raise SkillError(
                f"批次结果第 {index} 项含未批准字段: "
                + ", ".join(sorted(unknown))
            )
        results.append(item)
    return results


def _validate_against_batch(
    batch: dict[str, Any],
    results: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    expected = {
        str(unit["id"]): unit
        for unit in batch.get("units", [])
        if isinstance(unit, dict) and str(unit.get("id") or "")
    }
    if len(results) != len(expected):
        raise SkillError(
            f"批次 {batch['batch_id']} 需要 {len(expected)} 条结果，"
            f"实际收到 {len(results)} 条"
        )

    seen: set[str] = set()
    problems: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for item in results:
        unit_id = str(item.get("id") or "")
        if unit_id not in expected:
            problems.append(f"{unit_id or '<空 id>'}: 不属于本批次")
            continue
        if unit_id in seen:
            problems.append(f"{unit_id}: 重复出现")
            continue
        seen.add(unit_id)

        translation = item.get("translation")
        keep_code = item.get("keep_source_code")
        keep_reason = item.get("keep_source_reason")
        has_translation = isinstance(translation, str) and translation.strip()
        has_keep_code = isinstance(keep_code, str) and keep_code.strip()
        has_keep_reason = isinstance(keep_reason, str) and keep_reason.strip()
        if not has_translation and not has_keep_code:
            problems.append(
                f"{unit_id}: 既没有译文，也没有结构化的 keep_source_code"
            )
            continue
        if has_translation and (has_keep_code or has_keep_reason):
            problems.append(
                f"{unit_id}: 不能同时给出译文和保留原文声明"
            )
            continue

        flags = item.get("review_flags", [])
        if flags is not None and not isinstance(flags, list):
            problems.append(f"{unit_id}: review_flags 必须是数组")
            continue

        if has_translation:
            missing = anchors_present(
                expected[unit_id].get("required_anchors") or {},
                str(translation),
            )
            lost = {
                category: values
                for category, values in missing.items()
                if values
            }
            if lost:
                detail = "; ".join(
                    f"{category}: {', '.join(map(str, values))}"
                    for category, values in sorted(lost.items())
                )
                problems.append(f"{unit_id}: 译文丢失必填锚点 [{detail}]")
                continue
        by_id[unit_id] = item

    missing_ids = sorted(set(expected) - seen)
    if missing_ids:
        problems.append("缺少结果: " + ", ".join(missing_ids))
    if problems:
        raise SkillError(
            f"批次 {batch['batch_id']} 校验失败，未写入任何译文:\n"
            + "\n".join(f"- {problem}" for problem in problems)
        )
    return by_id


def _truthfulness_units(
    batch: dict[str, Any],
    accepted: dict[str, dict[str, Any]],
    element_roles: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """把批次里的冻结原文和本次结果拼成待检查的单元。

    元素角色必须一起带上：作者、单位、出版元数据和参考文献题录按角色
    免除目标语言占比门槛，也按角色允许 `publication-front-matter` 与
    `bibliography-entry` 保留原文。批次文件里带了就用批次里的，
    早先编排的批次没有这个字段，回 `translation.json` 查同一个单元。
    """

    roles = element_roles or {}
    merged: list[dict[str, Any]] = []
    for unit in batch.get("units", []):
        unit_id = str(unit.get("id") or "")
        item = accepted.get(unit_id)
        if item is None:
            continue
        merged.append(
            {
                "id": unit_id,
                "page": unit.get("page"),
                "kind": unit.get("kind"),
                "element_role": str(
                    unit.get("element_role") or roles.get(unit_id) or ""
                ),
                "source": unit.get("source"),
                "source_bbox": unit.get("source_bbox"),
                "translation": item.get("translation"),
                "keep_source_code": item.get("keep_source_code"),
                "keep_source_reason": item.get("keep_source_reason"),
            }
        )
    return merged


def _assert_truthful(
    job_dir: Path,
    batch: dict[str, Any],
    translation: dict[str, Any],
    accepted: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """写入 translation.json 和缓存之前执行的译文真实性检查。

    缓存命中走的也是这条路径，因此缓存不能绕过检查。
    """

    retained_path = job_dir / "retained_source.json"
    retained = load_json(retained_path) if retained_path.is_file() else None
    element_roles = {
        str(unit.get("id") or ""): str(unit.get("element_role") or "")
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    }
    # unit_bindings.json 是角色的权威来源：元素纠正后重新绑定，
    # 那里是新的，translation.json 里单元自带的可能还是旧的。
    bindings_path = job_dir / "unit_bindings.json"
    if bindings_path.is_file():
        for binding in load_json(bindings_path).get("bindings") or []:
            if isinstance(binding, dict) and binding.get("unit_id"):
                role = str(binding.get("element_role") or "")
                if role:
                    element_roles[str(binding["unit_id"])] = role
    report = evaluate_batch(
        _truthfulness_units(batch, accepted, element_roles),
        translation_document=translation,
        retained_source=retained,
        batch_id=str(batch.get("batch_id") or ""),
    )
    if not report["accepted"]:
        lines = [
            f"- {problem.get('unit_id') or problem.get('batch_id') or '整批'}"
            f" [{problem['code']}]: {problem['message']}"
            for problem in report["problems"]
        ]
        raise SkillError(
            f"批次 {batch['batch_id']} 未通过译文真实性检查，未写入任何译文:\n"
            + "\n".join(lines)
        )
    return report


def _assert_plan_ready(plan: dict[str, Any]) -> None:
    """术语表没确认之前不执行批次。"""

    if plan.get("terminology_reviewed") is not True:
        raise SkillError(
            "翻译计划记录的 terminology_reviewed 不是 true；"
            "术语表确认之前不得执行翻译批次，请确认术语表后重新编排。"
        )


def _assert_model_matches_plan(
    plan: dict[str, Any],
    model: str | None,
) -> None:
    """写回结果时验证实际模型与计划中的模型一致。"""

    planned = str(plan.get("model") or "")
    actual = str(model or "")
    if planned and actual and planned != actual:
        raise SkillError(
            f"实际模型 {actual!r} 与计划模型 {planned!r} 不一致；"
            "请用同一个模型重新翻译，或按新模型重新编排批次。"
        )
    if planned and not actual:
        raise SkillError(
            f"计划记录的模型是 {planned!r}，写回时必须用 --model 声明"
            "实际执行的模型。"
        )


def cache_identity(
    plan: dict[str, Any],
    model: str,
    batch_id: str,
) -> dict[str, Any]:
    """缓存条目的身份：换任何一项都不允许复用旧结果。"""

    return {
        "batch_id": batch_id,
        "applied_at": utc_now(),
        "model": model,
        "prompt_version": plan.get("prompt_version"),
        "strategy_version": plan.get("strategy_version"),
        "terminology_sha256": plan.get("terminology_sha256"),
        "target_language": plan.get("target_language"),
    }


def _refresh_coverage(
    translation: dict[str, Any],
    retained_source: Any,
) -> dict[str, Any]:
    """按真实性判定刷新覆盖率；complete 只在全部单元通过检查后为 true。"""

    return refresh_coverage(translation, retained_source=retained_source)


def _timed_apply_translation_batch(
    job_dir: Path,
    batch_id: str,
    results: list[dict[str, Any]],
    *,
    elapsed_seconds: float | None = None,
    model: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    retries: int = 0,
) -> dict[str, Any]:
    job_dir = Path(job_dir).resolve()
    job = load_json(job_dir / "job.json")
    translation_path = job_dir / job["files"]["translation"]
    plan = load_plan(job_dir)

    entry = next(
        (
            item
            for item in plan.get("batches", [])
            if str(item.get("batch_id")) == batch_id
        ),
        None,
    )
    if entry is None:
        raise SkillError(f"翻译计划中没有批次 {batch_id}")
    _assert_plan_ready(plan)
    _assert_model_matches_plan(plan, model)
    batch = load_json(job_dir / entry["file"])

    perf_trace.count(perf_trace.COUNTER_TRANSLATION_BATCH)
    normalized = _normalize_results(results)
    accepted = _validate_against_batch(batch, normalized)

    translation = load_json(translation_path)
    truthfulness = _assert_truthful(job_dir, batch, translation, accepted)
    index = {
        str(unit.get("id")): unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    }
    for unit_id, item in accepted.items():
        unit = index.get(unit_id)
        if unit is None:
            raise SkillError(
                f"translation.json 中缺少批次单元 {unit_id}，请重新编排批次"
            )
        source_unit = next(
            source
            for source in batch["units"]
            if str(source["id"]) == unit_id
        )
        if str(unit.get("source") or "") != str(source_unit.get("source") or ""):
            raise SkillError(
                f"{unit_id}: 原文与批次不一致，批次已过期，请重新编排"
            )
        translated = item.get("translation")
        keep_reason = item.get("keep_source_reason")
        unit["translation"] = (
            str(translated).strip()
            if isinstance(translated, str) and translated.strip()
            else None
        )
        keep_code = item.get("keep_source_code")
        unit["keep_source_code"] = (
            str(keep_code).strip()
            if isinstance(keep_code, str) and keep_code.strip()
            else None
        )
        unit["keep_source_reason"] = (
            str(keep_reason).strip()
            if isinstance(keep_reason, str) and keep_reason.strip()
            else None
        )
        flags = item.get("review_flags")
        if isinstance(flags, list):
            unit["review_flags"] = flags

    retained_path = job_dir / "retained_source.json"
    retained = load_json(retained_path) if retained_path.is_file() else None
    coverage = _refresh_coverage(translation, retained)
    write_json(translation_path, translation)

    applied_model = model or plan.get("model")
    if applied_model:
        # 只有记录了模型的批次才进正式缓存。没有模型标识的结果无法证明
        # 是谁翻的，缓存下来就会被别的模型误复用。
        cache = TranslationCache(job_dir)
        cache.put(
            str(entry["cache_key"]),
            [accepted[unit_id] for unit_id in sorted(accepted)],
            metadata=cache_identity(plan, applied_model, batch_id),
        )

    entry["status"] = "applied"
    entry["applied_at"] = utc_now()
    entry["retries"] = int(retries)
    entry["applied_model"] = applied_model
    entry["applied_unit_ids"] = sorted(accepted)
    entry["elapsed_seconds"] = elapsed_seconds
    entry["input_tokens"] = input_tokens
    entry["output_tokens"] = output_tokens
    plan["translation_sha256"] = sha256_file(translation_path)
    write_json(job_dir / PLAN_FILE_NAME, plan)

    from run_metrics import record_run_metric

    record_run_metric(
        job_dir,
        stage="translation-batch",
        status="complete",
        elapsed_seconds=elapsed_seconds,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        metadata={
            "batch_id": batch_id,
            "unit_count": entry["unit_count"],
            "source_chars": entry["source_chars"],
            "retries": int(retries),
            "cache_key": entry["cache_key"],
        },
    )

    pending = [
        item
        for item in plan["batches"]
        if item.get("status") != "applied"
    ]
    return {
        "batch_id": batch_id,
        "applied_units": len(accepted),
        "coverage": coverage,
        "pending_batches": [item["batch_id"] for item in pending],
        "translation_sha256": plan["translation_sha256"],
        "truthfulness": {
            "batch_id": truthfulness["batch_id"],
            "target_script_ratio": truthfulness["target_script_ratio"],
        },
    }


def apply_cached_batches(job_dir: Path) -> list[str]:
    """把缓存中已有结果的待处理批次直接写回，不重新翻译。

    命中缓存不等于可以少做检查：模型、提示版本、术语表和目标语言逐项复核，
    随后仍然走同一条写入校验和译文真实性检查。
    """

    job_dir = Path(job_dir).resolve()
    plan = load_plan(job_dir)
    _assert_plan_ready(plan)
    cache = TranslationCache(job_dir)
    restored: list[str] = []
    for entry in plan.get("batches", []):
        if entry.get("status") == "applied":
            continue
        cache_key = str(entry.get("cache_key") or "")
        cached = cache.get(cache_key)
        if not cached:
            continue
        metadata = cache.metadata(cache_key)
        expected = cache_identity(
            plan,
            str(plan.get("model") or ""),
            str(entry["batch_id"]),
        )
        mismatched = [
            field
            for field in (
                "model",
                "prompt_version",
                "strategy_version",
                "terminology_sha256",
                "target_language",
            )
            if metadata.get(field) != expected[field]
        ]
        if mismatched:
            raise SkillError(
                f"批次 {entry['batch_id']} 的缓存身份与当前计划不一致: "
                + ", ".join(mismatched)
                + "。缓存不得跨模型或跨术语表复用，请重新翻译该批次。"
            )
        apply_translation_batch(
            job_dir,
            str(entry["batch_id"]),
            cached,
            model=str(plan.get("model") or "") or None,
        )
        restored.append(str(entry["batch_id"]))
    return restored


def verify_plan_execution(job_dir: Path) -> dict[str, Any]:
    """最后一道账：计划批次、已验证批次和实际单元数量必须对得上。

    少执行一批时，这里必须失败，而不是靠调用方自己汇报。
    """

    job_dir = Path(job_dir).resolve()
    plan = load_plan(job_dir)
    job = load_json(job_dir / "job.json")
    translation = load_json(job_dir / job["files"]["translation"])
    batches = [item for item in plan.get("batches", []) if isinstance(item, dict)]
    applied = [item for item in batches if item.get("status") == "applied"]
    pending = [item["batch_id"] for item in batches if item not in applied]
    planned_units = sum(int(item.get("unit_count") or 0) for item in batches)
    applied_units = sum(
        len(item.get("applied_unit_ids") or []) for item in applied
    )
    document_units = len(
        [unit for unit in translation.get("units", []) if isinstance(unit, dict)]
    )
    coverage = translation.get("coverage", {})
    problems: list[str] = []
    if pending:
        problems.append(
            f"还有 {len(pending)} 批未执行: " + ", ".join(map(str, pending[:20]))
        )
    if planned_units != document_units:
        problems.append(
            f"计划单元 {planned_units} 与 translation.json 单元 "
            f"{document_units} 不一致"
        )
    if applied_units != document_units:
        problems.append(
            f"已写回单元 {applied_units} 与 translation.json 单元 "
            f"{document_units} 不一致"
        )
    if int(coverage.get("invalid_or_unverified_units") or 0):
        problems.append(
            f"仍有 {coverage['invalid_or_unverified_units']} 个单元未通过"
            "译文真实性检查"
        )
    report = {
        "batch_count": len(batches),
        "applied_batches": len(applied),
        "pending_batches": pending,
        "planned_units": planned_units,
        "applied_units": applied_units,
        "document_units": document_units,
        "complete": not problems,
        "problems": problems,
    }
    if problems:
        raise SkillError(
            "翻译批次执行不完整:\n"
            + "\n".join(f"- {problem}" for problem in problems)
        )
    return report



def apply_translation_batch(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("apply_batch"):
        return _timed_apply_translation_batch(*args, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--batch", help="批次 ID，例如 batch-0001")
    parser.add_argument(
        "--results-dir",
        type=Path,
        help="按批次顺序串行写回该目录下的全部结果文件"
        "（<batch_id>.result.json）。翻译可以并行，写回必须由"
        "唯一的写回者走这一个入口，检查逐批照跑",
    )
    parser.add_argument(
        "--result",
        type=Path,
        help="批次结果 JSON；使用 - 表示从标准输入读取",
    )
    parser.add_argument(
        "--from-cache",
        action="store_true",
        help="把缓存中已有结果的待处理批次直接写回",
    )
    parser.add_argument("--elapsed-seconds", type=float)
    parser.add_argument("--model")
    parser.add_argument("--input-tokens", type=int)
    parser.add_argument("--output-tokens", type=int)
    parser.add_argument("--retries", type=int, default=0)
    args = parser.parse_args()
    try:
        if args.from_cache:
            restored = apply_cached_batches(args.job_dir)
            print(
                "从缓存写回批次: " + (", ".join(restored) or "无")
            )
            return 0
        if args.results_dir is not None:
            plan = load_json(args.job_dir / "translation-plan.json")
            applied: list[str] = []
            missing: list[str] = []
            for batch in plan.get("batches", []):
                batch_id = str(batch.get("batch_id") or "")
                result_path = args.results_dir / f"{batch_id}.result.json"
                if batch.get("status") == "applied":
                    continue
                if not result_path.is_file():
                    missing.append(batch_id)
                    continue
                payload = json.loads(
                    result_path.read_text(encoding="utf-8")
                )
                apply_translation_batch(
                    args.job_dir,
                    batch_id,
                    payload,
                    elapsed_seconds=args.elapsed_seconds,
                    model=args.model,
                    retries=args.retries,
                )
                applied.append(batch_id)
            print(f"串行写回 {len(applied)} 批: " + (", ".join(applied) or "无"))
            if missing:
                print(
                    f"还缺 {len(missing)} 批的结果文件: "
                    + ", ".join(missing)
                )
            return 0
        if not args.batch or args.result is None:
            raise SkillError("请提供 --batch 和 --result，或使用 --from-cache")
        started = time.perf_counter()
        if str(args.result) == "-":
            payload = json.loads(sys.stdin.read())
        else:
            payload = json.loads(
                args.result.resolve().read_text(encoding="utf-8")
            )
        report = apply_translation_batch(
            args.job_dir,
            args.batch,
            payload,
            elapsed_seconds=(
                args.elapsed_seconds
                if args.elapsed_seconds is not None
                else round(time.perf_counter() - started, 3)
            ),
            model=args.model,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            retries=args.retries,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (SkillError, json.JSONDecodeError) as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
