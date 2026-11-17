from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

import perf_trace
from _common import (
    SCHEMA_VERSION,
    SkillError,
    import_fitz,
    internal_job_path,
    load_json,
    sha256_file,
    utc_now,
    write_json,
)
from candidate_analysis import open_candidate_analysis
from candidate_page_map import (
    candidate_page_map_path,
    validate_candidate_page_map,
)
from renderer_identity import renderer_build_id as current_renderer_build_id
from review_policy import post_repair_confirmation_template


def _reset_review(path: Path, source_hash: str) -> None:
    role = "independent" if "independent" in path.name else "producer"
    write_json(
        path,
        {
            "schema_version": SCHEMA_VERSION,
            "reviewer_role": role,
            "reviewer_id": None,
            "decision": "PENDING",
            "source_sha256": source_hash,
            "candidate_sha256": None,
            "coverage": [],
            "reviewed_pages": [],
            "issues": [],
            "residual_risks": [],
            "reviewed_at": None,
        },
    )


def _link_or_copy(source: str, destination: str) -> str:
    try:
        os.link(source, destination)
        return destination
    except OSError:
        return shutil.copy2(source, destination)


def _copy_if_present(source: Path, destination: Path) -> None:
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        _link_or_copy(str(source), str(destination))
    elif source.is_dir():
        shutil.copytree(
            source,
            destination,
            copy_function=_link_or_copy,
        )


def _clear_directory_contents(directory: Path) -> None:
    if not directory.is_dir():
        return
    for path in directory.iterdir():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()


def _preflight_allows_inventory_binding(
    job_dir: Path,
    job: dict,
    *,
    candidate_hash: str,
    base_iteration: int,
    renderer: str,
    renderer_version: str | None,
    renderer_build_id: str | None,
    inventory_path: Path,
) -> bool:
    if not isinstance(renderer_version, str) or not renderer_version.strip():
        return False
    files = job.get("files", {})
    ledger_path = internal_job_path(
        job_dir,
        files.get("preflight_ledger", "staging/preflight-ledger.json"),
    )
    readiness_path = internal_job_path(
        job_dir,
        files.get("render_readiness", "staging/render-readiness.json"),
    )
    if (
        not ledger_path.is_file()
        or not readiness_path.is_file()
        or not inventory_path.is_file()
    ):
        return False
    ledger = load_json(ledger_path)
    readiness_hash = sha256_file(readiness_path)
    inventory_hash = sha256_file(inventory_path)
    for cycle in ledger.get("cycles", []):
        if (
            not isinstance(cycle, dict)
            or cycle.get("base_iteration") != base_iteration
            or cycle.get("renderer") != renderer.strip()
            or (
                cycle.get("renderer_build_id") != renderer_build_id
                if renderer_build_id
                else (
                    bool(cycle.get("renderer_build_id"))
                    or cycle.get("renderer_version")
                    != renderer_version.strip()
                )
            )
        ):
            continue
        for run in cycle.get("runs", []):
            if (
                isinstance(run, dict)
                and run.get("candidate_sha256") == candidate_hash
                and run.get("status") == "READY_TO_REGISTER"
                and run.get("render_readiness_sha256") == readiness_hash
                and run.get("figure_inventory_sha256") == inventory_hash
            ):
                return True
    return False


def _archive_previous_iteration(
    job_dir: Path,
    job: dict,
    destination: Path,
    provenance_path: Path,
    notes: str | None,
    allow_additional_iteration: bool,
) -> tuple[int, str | None]:
    provenance = load_json(provenance_path)
    previous_hash = provenance.get("candidate_sha256")
    if not previous_hash:
        if destination.exists():
            raise SkillError("发现未注册的 candidate.pdf，请先移出作业目录后再注册")
        return 1, None
    if not destination.is_file():
        raise SkillError("候选来源记录存在，但 candidate.pdf 已丢失")
    if sha256_file(destination) != previous_hash:
        raise SkillError(
            "candidate.pdf 已在注册入口之外被改写，无法可靠归档上一轮"
        )
    if not isinstance(notes, str) or not notes.strip():
        raise SkillError("重新注册候选时必须用 --notes 记录本轮修复原因")

    previous_iteration = int(provenance.get("iteration") or 1)
    review = job.get("review")
    if isinstance(review, dict):
        max_repair_rounds = int(review.get("max_repair_rounds") or 0)
        max_candidates = 1 + max_repair_rounds
    else:
        max_candidates = 2
    if (
        previous_iteration >= max_candidates
        and not allow_additional_iteration
    ):
        raise SkillError(
            f"当前质量档位最多允许 {max_candidates} 个正式候选；"
            "如需在已用尽额度后升级生成器，请显式使用 "
            "--reopen-iteration"
        )
    archive_dir = job_dir / "history" / f"iteration-{previous_iteration:04d}"
    if archive_dir.exists():
        raise SkillError(f"历史归档目录已存在，拒绝覆盖: {archive_dir}")
    archive_dir.mkdir(parents=True)

    files = job["files"]
    archived_paths = [
        (destination, archive_dir / "candidate.pdf"),
        (provenance_path, archive_dir / "candidate_provenance.json"),
        (
            internal_job_path(job_dir, files["translation"]),
            archive_dir / "translation.json",
        ),
        (
            internal_job_path(job_dir, files["retained_source"]),
            archive_dir / "retained_source.json",
        ),
        (
            internal_job_path(job_dir, files["figure_inventory"]),
            archive_dir / "figure_inventory.json",
        ),
        (
            internal_job_path(job_dir, files["layout_overrides"]),
            archive_dir / "layout_overrides.json",
        ),
        (internal_job_path(job_dir, files["qa"]), archive_dir / "qa.json"),
        (
            internal_job_path(job_dir, files["independent_review"]),
            archive_dir / "reviews" / "independent.json",
        ),
        (
            internal_job_path(job_dir, files["finalization"]),
            archive_dir / "finalization.json",
        ),
        (
            internal_job_path(
                job_dir,
                files.get(
                    "post_repair_confirmation",
                    "reviews/post-repair.json",
                ),
            ),
            archive_dir / "reviews" / "post-repair.json",
        ),
        (job_dir / "renders", archive_dir / "renders"),
        (job_dir / "comparisons", archive_dir / "comparisons"),
    ]
    previous_map_path = candidate_page_map_path(job_dir, job)
    if previous_map_path.is_file():
        archived_paths.append(
            (
                previous_map_path,
                archive_dir / "candidate-page-map.json",
            )
        )
    if "producer_review" in files:
        archived_paths.append(
            (
                internal_job_path(job_dir, files["producer_review"]),
                archive_dir / "reviews" / "producer.json",
            )
        )
    for source, archived in archived_paths:
        _copy_if_present(source, archived)

    write_json(
        archive_dir / "archive_manifest.json",
        {
            "schema_version": SCHEMA_VERSION,
            "archived_at": utc_now(),
            "iteration": previous_iteration,
            "candidate_sha256": previous_hash,
            "translation_sha256": provenance.get("translation_sha256"),
            "layout_overrides_sha256": provenance.get(
                "layout_overrides_sha256"
            ),
            "superseded_by_reason": notes.strip(),
            "storage_strategy": "hardlink-with-copy-fallback",
        },
    )
    return previous_iteration + 1, previous_hash


def _timed_register_candidate(
    job_dir: Path,
    generated_pdf: Path,
    renderer: str,
    renderer_version: str | None,
    notes: str | None,
    *,
    renderer_build_id: str | None = None,
    allow_additional_iteration: bool = False,
) -> dict:
    job_dir = job_dir.resolve()
    generated_pdf = generated_pdf.resolve()
    if not generated_pdf.is_file():
        raise SkillError(f"候选 PDF 不存在: {generated_pdf}")
    if not renderer.strip():
        raise SkillError("--renderer 不能为空")
    if renderer.strip() == "academic-pdf-layout":
        expected_build_id = current_renderer_build_id()
        if (
            isinstance(renderer_build_id, str)
            and renderer_build_id.strip()
            and renderer_build_id.strip() != expected_build_id
        ):
            raise SkillError("renderer_build_id 与当前统一生成器代码不一致")
        renderer_build_id = expected_build_id
    elif isinstance(renderer_build_id, str):
        renderer_build_id = renderer_build_id.strip() or None

    job = load_json(job_dir / "job.json")
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    source_hash = sha256_file(source_path)
    candidate_hash = sha256_file(generated_pdf)
    if candidate_hash == source_hash:
        raise SkillError("候选 PDF 与原文哈希相同，拒绝注册")

    fitz = import_fitz()
    try:
        candidate_handle = open_candidate_analysis(generated_pdf)
        candidate_document = candidate_handle.document
    except Exception as exc:
        raise SkillError(f"候选 PDF 无法打开: {exc}") from exc
    if candidate_document.page_count < 1:
        raise SkillError("候选 PDF 没有页面")
    candidate_page_count = candidate_document.page_count
    candidate_handle.release()

    files = job.get("files", {})
    sidecar_map_path = generated_pdf.with_suffix(".page-map.json")
    mapping = None
    if sidecar_map_path.is_file():
        mapping = load_json(sidecar_map_path)
        translation = load_json(
            internal_job_path(job_dir, files["translation"])
        )
        unit_ids = {
            str(unit.get("id"))
            for unit in translation.get("units", [])
            if isinstance(unit, dict) and str(unit.get("id") or "")
        }
        map_errors = validate_candidate_page_map(
            mapping,
            source_page_count=int(job["source"]["page_count"]),
            candidate_page_count=candidate_page_count,
            translation_unit_ids=unit_ids,
            candidate_sha256=candidate_hash,
        )
        if map_errors:
            raise SkillError("候选页映射无效: " + "；".join(map_errors))
    elif "candidate_page_map" in files:
        raise SkillError(
            f"缺少候选页映射侧车文件: {sidecar_map_path}"
        )

    destination = internal_job_path(job_dir, job["files"]["candidate"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    provenance_path = internal_job_path(
        job_dir, job["files"]["candidate_provenance"]
    )
    if generated_pdf == destination and destination.is_file():
        raise SkillError(
            "请在作业目录外生成 PDF，再通过注册入口接入；不能原地改写 candidate.pdf"
        )
    iteration, supersedes_hash = _archive_previous_iteration(
        job_dir,
        job,
        destination,
        provenance_path,
        notes,
        allow_additional_iteration,
    )
    official_map_path = candidate_page_map_path(job_dir, job)
    if mapping is None and official_map_path.is_file():
        official_map_path.unlink()
    if generated_pdf != destination:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
        try:
            shutil.copy2(generated_pdf, temp_path)
            os.replace(temp_path, destination)
        finally:
            if temp_path.exists():
                temp_path.unlink()
    registered_hash = sha256_file(destination)
    registered_map_hash = None
    if mapping is not None:
        write_json(official_map_path, mapping)
        registered_map_hash = sha256_file(official_map_path)
    provenance = {
        "schema_version": SCHEMA_VERSION,
        "iteration": iteration,
        "registered_at": utc_now(),
        "renderer": renderer.strip(),
        "renderer_version": renderer_version.strip()
        if isinstance(renderer_version, str) and renderer_version.strip()
        else None,
        "renderer_build_id": renderer_build_id,
        "producer_id": job.get("review", {}).get("producer_id"),
        "original_candidate_path": str(generated_pdf),
        "candidate_sha256": registered_hash,
        "translation_sha256": sha256_file(
            internal_job_path(job_dir, job["files"]["translation"])
        ),
        "layout_overrides_sha256": sha256_file(
            internal_job_path(job_dir, job["files"]["layout_overrides"])
        ),
        "candidate_page_map_sha256": registered_map_hash,
        "supersedes_candidate_sha256": supersedes_hash,
        "notes": notes.strip() if isinstance(notes, str) and notes.strip() else None,
    }
    write_json(provenance_path, provenance)
    for review_key in ("producer_review", "independent_review"):
        if review_key not in job["files"]:
            continue
        _reset_review(
            internal_job_path(job_dir, job["files"][review_key]),
            source_hash,
        )
    inventory_path = internal_job_path(
        job_dir, job["files"]["figure_inventory"]
    )
    inventory = load_json(inventory_path)
    unresolved_inventory = any(
        isinstance(item, dict)
        and (
            str(item.get("text_status") or "").lower() == "unresolved"
            or str(item.get("status") or "").lower() == "unresolved"
        )
        for item in inventory.get("items", [])
    )
    preflight_bound = (
        inventory.get("inventory_complete") is True
        and not unresolved_inventory
        and _preflight_allows_inventory_binding(
            job_dir,
            job,
            candidate_hash=registered_hash,
            base_iteration=max(0, iteration - 1),
            renderer=renderer,
            renderer_version=renderer_version,
            renderer_build_id=renderer_build_id,
            inventory_path=inventory_path,
        )
    )
    inventory["inventory_complete"] = (
        inventory.get("inventory_complete") is True
        and not unresolved_inventory
    )
    inventory["candidate_sha256"] = (
        registered_hash if preflight_bound else None
    )
    write_json(inventory_path, inventory)
    for directory in (
        job_dir / "renders" / "source",
        job_dir / "renders" / "candidate",
        job_dir / "comparisons",
    ):
        _clear_directory_contents(directory)
    write_json(
        internal_job_path(job_dir, job["files"]["finalization"]),
        {
            "schema_version": SCHEMA_VERSION,
            "review_mode": (
                job.get("review", {}).get("mode", "legacy-double")
            ),
            "formal_pdf": None,
            "sha256": None,
            "zotero": {
                "parent_item": None,
                "source_attachment": None,
                "translation_attachment": None,
                "source_index_check": False,
                "translation_index_check": False,
            },
        },
    )
    write_json(
        internal_job_path(
            job_dir,
            job["files"].get(
                "post_repair_confirmation",
                "reviews/post-repair.json",
            ),
        ),
        post_repair_confirmation_template(source_hash),
    )
    if job.get("status") in {"candidate", "accepted", "finalized"}:
        job["status"] = "translated"
        write_json(job_dir / "job.json", job)
    return provenance



def register_candidate(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("register_candidate"):
        return _timed_register_candidate(*args, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="将外部排版器生成的 PDF 安全接入统一译制作业"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("generated_pdf", type=Path)
    parser.add_argument("--renderer", required=True)
    parser.add_argument("--renderer-version")
    parser.add_argument("--renderer-build-id")
    parser.add_argument("--notes")
    parser.add_argument(
        "--reopen-iteration",
        action="store_true",
        help="已用尽档位候选额度后，显式允许一次生成器升级注册",
    )
    args = parser.parse_args()
    try:
        provenance = register_candidate(
            args.job_dir,
            args.generated_pdf,
            args.renderer,
            args.renderer_version,
            args.notes,
            renderer_build_id=args.renderer_build_id,
            allow_additional_iteration=args.reopen_iteration,
        )
        print("候选已注册")
        print(f"渲染器: {provenance['renderer']}")
        print(f"SHA-256: {provenance['candidate_sha256']}")
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
