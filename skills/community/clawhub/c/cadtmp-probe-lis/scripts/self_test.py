#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader 统一自测/回归闭环（第 4 步：CI / self_test 正式化）。

一条命令串起：
  1. doctor 环境体检（scripts/doctor.py --json-only）
  2. 全量自测（scripts/tests/test_*.py，unittest discover）
  3. schema 契约校验（schemas/*.schema.json 原生轻量校验 + scripts/cad_validate.sh）
  4. 样例回归（examples/sample_room.dxf：cad_preflight → cad_scan → contractize → cad_validate）
  5. 坏文件不变量（空文件/坏魔数用 cad_preflight 快速失败）
  6. 可选真实 DWG 回归（--manifest），未提供则报告为“跳过”

输出 doctor + self_test + 回归“三合一”报告（JSON + Markdown）。

用法：
  python3 scripts/self_test.py [--manifest <真图清单.json>]
  python3 scripts/self_test.py --out-dir /tmp/cad-self-test --report-json r.json --report-md r.md
  python3 scripts/self_test.py --json-only --skip-unit --skip-sample --skip-schema  # 快速开发用
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
TESTS_DIR = SCRIPTS_DIR / "tests"
EXAMPLES_DIR = SKILL_DIR / "examples"
SCHEMAS_DIR = SKILL_DIR / "schemas"
SAMPLE_DXF = EXAMPLES_DIR / "sample_room.dxf"
REPORT_SCHEMA = "cad-file-reader/self-test/v1"
STATUS_OK = "pass"
STATUS_FAIL = "fail"
STATUS_SKIP = "skipped"


def _now() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _resolve_python() -> Path:
    candidates = [
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3",
    ]
    try:
        candidates += sorted((Path.home() / ".cache" / "codex-runtimes").glob("*/dependencies/python/bin/python3"))
    except OSError:
        pass
    candidates.append(Path(shutil.which("python3") or "/nonexistent"))
    for cand in candidates:
        if cand and cand.is_file() and os.access(str(cand), os.X_OK):
            return cand
    return Path(sys.executable)


# --------------------------------------------------------------------------- #
# 1) 本地轻量 JSON Schema 校验（无需 jsonschema 依赖，兼容随包两个 schema）
# --------------------------------------------------------------------------- #
def _type_matches(instance, expected) -> bool:
    names = [expected] if isinstance(expected, str) else expected
    for name in names:
        if name == "object":
            if isinstance(instance, dict):
                return True
        elif name == "array":
            if isinstance(instance, list):
                return True
        elif name == "string":
            if isinstance(instance, str):
                return True
        elif name == "number":
            if isinstance(instance, (int, float)) and not isinstance(instance, bool):
                return True
        elif name == "integer":
            if isinstance(instance, int) and not isinstance(instance, bool):
                return True
        elif name == "boolean":
            if isinstance(instance, bool):
                return True
        elif name == "null":
            if instance is None:
                return True
    return False


def _resolve_ref(root: dict, ref: str):
    if ref == "#":
        return root
    if ref.startswith("#/$defs/"):
        name = ref[len("#/$defs/"):]
        return (root.get("$defs") or {}).get(name)
    return None


def validate_schema(instance, schema, root=None) -> list[str]:
    """递归校验 instance 对 schema；返回错误列表。仅覆盖随包两个 schema 用到的关键字。"""
    if not isinstance(schema, dict):
        return []
    root = root if root is not None else schema
    errors: list[str] = []

    ref = schema.get("$ref")
    if isinstance(ref, str):
        resolved = _resolve_ref(root, ref)
        if resolved is None:
            return [f"$ref 无法解析: {ref}"]
        return validate_schema(instance, resolved, root)

    type_rule = schema.get("type")
    if type_rule is not None and not _type_matches(instance, type_rule):
        return [f"类型不符（期望 {json.dumps(type_rule, ensure_ascii=False)}）"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"const 不匹配（期望 {json.dumps(schema['const'], ensure_ascii=False)}）")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append("值不在 enum 允许范围内")

    if "minLength" in schema and isinstance(instance, str) and len(instance) < schema["minLength"]:
        errors.append(f"长度 {len(instance)} 小于 minLength {schema['minLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{instance} 小于 minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{instance} 大于 maximum {schema['maximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"数组长度 {len(instance)} 小于 minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"数组长度 {len(instance)} 大于 maxItems {schema['maxItems']}")
        items_rules = schema.get("items")
        if items_rules is not None:
            for idx, item in enumerate(instance):
                errors.extend(f"items[{idx}]: {e}" for e in validate_schema(item, items_rules, root))

    if isinstance(instance, dict):
        for field in schema.get("required", []):
            if field not in instance:
                errors.append(f"缺少必需字段 {field}")
        props = schema.get("properties")
        if isinstance(props, dict):
            for key, subschema in props.items():
                if key in instance:
                    errors.extend(f"{key}: {e}" for e in validate_schema(instance[key], subschema, root))

    if "oneOf" in schema:
        variants = schema["oneOf"]
        if not isinstance(variants, list):
            errors.append("oneOf 不是数组")
        else:
            ok_count = sum(1 for variant in variants if not validate_schema(instance, variant, root))
            if ok_count != 1:
                errors.append(f"oneOf 分支命中数 = {ok_count}（应为 1）")
    return errors


def validate_schema_file(instance, schema_path: Path) -> tuple[bool, list[str]]:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, [f"读 schema 失败: {exc}"]
    errors = validate_schema(instance, schema)
    return (len(errors) == 0), errors


# --------------------------------------------------------------------------- #
# 2) 全量 unittest（通过子进程发现，避免本进程污染 sys.path/vendor）
# --------------------------------------------------------------------------- #
def cmd_unit_json() -> int:
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR), pattern="test_*.py")
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1)
    result = runner.run(suite)
    failed = [t[0].id() for t in result.failures] + [t[0].id() for t in result.errors]
    payload = {
        "ok": bool(result.wasSuccessful()),
        "tests_run": int(result.testsRun),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "failed_tests": failed,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if result.wasSuccessful() else 1


def run_unit_tests(python: Path) -> tuple[dict, int]:
    proc = subprocess.run(
        [str(python), str(Path(__file__).resolve()), "--unit-json"],
        cwd=str(SKILL_DIR),
        capture_output=True,
        text=True,
        timeout=1800,
    )
    try:
        data = json.loads((proc.stdout or "{}").strip() or "{}")
    except Exception as exc:
        data = {"ok": False, "error": f"解析 unittest 输出失败: {exc}", "tests_run": 0}
    data["rc"] = proc.returncode
    stderr_text = proc.stderr or ""
    data["stderr_tail"] = stderr_text.strip().splitlines()[-8:]
    # 保留关键 traceback 摘要，避免 CI 只留最后五行而无法定位失败点
    data["stderr_trace"] = [
        ln for ln in stderr_text.splitlines()
        if ln.startswith(("Traceback", "  File ", "    ")) or ln.startswith(("ERROR:", "FAIL:", "TypeError", "UnicodeEncodeError"))
    ][:80]
    if data.get("ok") is not True:
        data["ok"] = False
    return data, (0 if data.get("ok") else 1)


# --------------------------------------------------------------------------- #
# 3) schema 契约校验安装/样例选择
# --------------------------------------------------------------------------- #
def _iter_qto_samples() -> list[Path]:
    base = EXAMPLES_DIR / "qto-sample" / "识别"
    if base.is_dir():
        return sorted(base.rglob("*.json"))
    return []


def _sample_for_schema(schema_path: Path) -> list[Path]:
    out: list[Path] = []
    for p in _iter_qto_samples():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        name = schema_path.name
        if name == "candidate-v0.schema.json" and (data.get("contract") or {}).get("schema") == "cad-file-reader/v0":
            out.append(p)
        elif name == "qto-project-v1.schema.json" and data.get("qto_spec") == "qto-project/v1":
            out.append(p)
    return out


def _negative_samples(schema_path: Path) -> list[dict]:
    name = schema_path.name
    good_paths = _sample_for_schema(schema_path)
    if not good_paths:
        return []
    good = json.loads(good_paths[0].read_text(encoding="utf-8"))
    if name == "candidate-v0.schema.json":
        out = []
        bad1 = json.loads(json.dumps(good))
        bad1["contract"]["schema"] = "cad-file-reader/wrong"
        bad1["_label"] = "contract.schema 篡改"
        out.append(bad1)
        # 样例 candidates 可能为空，手工构造一条带 final_quantity=true 的候选触发 const false。
        bad2 = {
            "contract": {
                "schema": "cad-file-reader/v0",
                "source": "synthetic_bad",
                "origin_schema": "synthetic",
                "summary": {},
                "review_reasons": [],
                "candidates": [{
                    "id": "x1", "kind": "text", "value": None, "unit": None,
                    "layer": "A", "block_name": None, "text": "t", "bbox": None,
                    "evidence": [], "method": "m", "confidence": 0.9,
                    "confidence_tier": "confirmed_evidence", "review_reasons": [],
                    "review_notes": "", "source_schema": "cad-file-reader/v0",
                    "source_id": "s", "final_quantity": True,
                }],
                "review_candidates": [],
                "boundary": "b",
            }
        }
        bad2["_label"] = "final_quantity=true"
        out.append(bad2)
        bad3 = json.loads(json.dumps(good))
        bad3.pop("contract", None)
        bad3["_label"] = "缺 contract"
        out.append(bad3)
        return out
    if name == "qto-project-v1.schema.json":
        out = []
        bad1 = json.loads(json.dumps(good))
        bad1.pop("qto_spec", None)
        bad1["_label"] = "缺 qto_spec"
        out.append(bad1)
        bad2 = json.loads(json.dumps(good))
        bad2["project_key"] = {"project": "x"}
        bad2["_label"] = "project_key 缺字段"
        out.append(bad2)
        bad3 = json.loads(json.dumps(good))
        bad3["draft_type"] = "not_allowed"
        bad3["_label"] = "draft_type 非法"
        out.append(bad3)
        return out
    return []


def run_schema_steps(python: Path) -> tuple[dict, int]:
    results: list[dict] = []
    failed_total = 0
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        item = {"schema": schema_path.name, "samples": [], "type_ok": True, "ok": True, "errors": []}
        try:
            schema_obj = json.loads(schema_path.read_text(encoding="utf-8"))
            if not isinstance(schema_obj, dict) or "$schema" not in schema_obj:
                item["type_ok"] = False
                item["ok"] = False
                item["errors"].append("schema 文件不是合法 JSON Schema 对象")
        except Exception as exc:
            item["type_ok"] = False
            item["ok"] = False
            item["errors"].append(f"schema JSON 解析失败: {exc}")
        for sample in _sample_for_schema(schema_path):
            try:
                data = json.loads(sample.read_text(encoding="utf-8"))
                ok, errs = validate_schema_file(data, schema_path)
            except Exception as exc:
                ok, errs = False, [f"读样例失败: {exc}"]
            item["samples"].append({"file": str(sample), "ok": ok, "errors": errs[:6]})
            if not ok:
                item["ok"] = False
        negative_ok = True
        if item["type_ok"]:
            for bad in _negative_samples(schema_path):
                bad_payload = {k: v for k, v in bad.items() if k != "_label"}
                ok, errs = validate_schema_file(bad_payload, schema_path)
                if ok:
                    negative_ok = False
                    item["ok"] = False
                    item["errors"].append(f"负向样例未拦截: {bad.get('_label', '?')}")
        item["ok"] = bool(item["ok"] and negative_ok)
        results.append(item)
        if not item["ok"]:
            failed_total += 1

    contract_files: list[Path] = []
    for p in _iter_qto_samples():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and (data.get("contract") or {}).get("schema") == "cad-file-reader/v0":
                contract_files.append(p)
        except Exception:
            continue
    validate_steps: list[dict] = []
    for path in contract_files:
        proc = subprocess.run(
            [str(python), str(SCRIPTS_DIR / "cad_validate.py"), str(path)],
            cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=120,
        )
        ok = proc.returncode == 0
        validate_steps.append({"file": str(path), "ok": ok, "rc": proc.returncode,
                               "output_tail": (proc.stdout or proc.stderr).strip().splitlines()[-3:]})
        if not ok:
            failed_total += 1
    step = {
        "name": "schema_contract",
        "schemas": results,
        "cad_validate_samples": {"ok": all(v["ok"] for v in validate_steps), "checks": validate_steps},
        "ok": failed_total == 0,
    }
    return step, (0 if failed_total == 0 else 1)


# --------------------------------------------------------------------------- #
# 4) 样例 DXF + 坏文件不变量
# --------------------------------------------------------------------------- #
def run_sample_regression(python: Path) -> tuple[dict, int]:
    step = {"name": "sample_dxf", "ok": False, "detail": {}}
    if not SAMPLE_DXF.is_file():
        step["detail"]["error"] = f"样例缺失: {SAMPLE_DXF}"
        return step, 1
    with tempfile.TemporaryDirectory(prefix="cad-selftest-sample-") as tmpd:
        tmp = Path(tmpd)
        detail = tmp / "sample_detail.json"
        out_prefix = tmp / "sample_out"
        env = dict(os.environ)
        env.setdefault("PYTHONPATH", str(SKILL_DIR / "vendor"))
        env["CAD_CONCISE"] = "0"
        proc = subprocess.run(
            [str(python), str(SCRIPTS_DIR / "run_cad.py"), "cad_scan", str(SAMPLE_DXF),
             "--format", "json", "--detail-json", str(detail), "-o", str(out_prefix)],
            cwd=str(SKILL_DIR), env=env, capture_output=True, text=True, timeout=600,
        )
        step["detail"]["scan_rc"] = proc.returncode
        step["detail"]["scan_stderr_tail"] = (proc.stderr or "").strip().splitlines()[-4:]
        if proc.returncode != 0 or not detail.is_file():
            step["detail"]["error"] = "cad_scan 样例失败或未产出详情"
            return step, 1
        try:
            payload = json.loads(detail.read_text(encoding="utf-8"))
        except Exception as exc:
            step["detail"]["error"] = f"样例详情解析失败: {exc}"
            return step, 1
        old_path = list(sys.path)
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from cad_contract import contractize_payload, validate_contract_payload  # noqa
            out_json = tmp / "sample_contract.json"
            contracted = contractize_payload(payload, source=str(SAMPLE_DXF), concise=False)
            out_json.write_text(json.dumps(contracted, ensure_ascii=False, indent=2), encoding="utf-8")
            payload_errors = validate_contract_payload(contracted)
            cli = subprocess.run(
                [str(python), str(SCRIPTS_DIR / "cad_validate.py"), str(out_json)],
                cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=60,
            )
            step["detail"]["contract_file"] = str(out_json)
            step["detail"]["text_total"] = payload.get("text_total")
            step["detail"]["files"] = len(payload.get("files") or [])
            step["detail"]["contract_errors"] = payload_errors[:6]
            if payload_errors or cli.returncode != 0:
                step["detail"]["error"] = "样例契约校验失败（cad_contract 或 cad_validate.py）"
                return step, 1
            if not (payload.get("files") or payload.get("text_total") or payload.get("text_records")):
                step["detail"]["error"] = "样例扫描没有产出任何文字/文件记录"
                return step, 1
            step["ok"] = True
            return step, 0
        finally:
            sys.path[:] = old_path


def run_bad_file_invariants(python: Path) -> tuple[dict, int]:
    step = {"name": "bad_file_invariants", "ok": False, "checks": []}
    old_path = list(sys.path)
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from cad_preflight import preflight_file  # noqa
        with tempfile.TemporaryDirectory(prefix="cad-selftest-bad-") as tmpd:
            tmp = Path(tmpd)
            empty = tmp / "empty.dxf"
            empty.write_bytes(b"")
            bad = tmp / "bad.dxf"
            bad.write_bytes(b"not-cad\n" * 300)
            t0 = time.time()
            r1 = preflight_file(empty)
            r2 = preflight_file(bad)
            elapsed = round(time.time() - t0, 3)
            checks = [
                {"case": "空文件", "ok": r1.get("ok") is False and "空" in r1.get("reason", ""), "detail": r1.get("reason")},
                {"case": "坏魔数", "ok": r2.get("ok") is False and "魔数" in r2.get("reason", ""), "detail": r2.get("reason")},
                {"case": "快速失败<5s", "ok": elapsed < 5.0, "detail": f"{elapsed}s"},
            ]
            step["checks"] = checks
            step["ok"] = all(c["ok"] for c in checks)
            step["elapsed_seconds"] = elapsed
            return step, (0 if step["ok"] else 1)
    except Exception as exc:
        step["ok"] = False
        step["detail"] = f"cad_preflight 导入失败: {exc}"
        return step, 1
    finally:
        sys.path[:] = old_path


# --------------------------------------------------------------------------- #
# 5) 真实 DWG 回归
# --------------------------------------------------------------------------- #
def run_real_dwg_regression(python: Path, manifest, out_dir: Path) -> tuple[dict, int]:
    step = {"name": "real_dwg_regression"}
    if not manifest or not Path(manifest).exists():
        step["status"] = STATUS_SKIP
        step["detail"] = "未提供 --manifest，跳过真实图纸回归"
        return step, 0
    report_json = out_dir / "real-dwg-regression-report.json"
    proc = subprocess.run(
        [str(python), str(SCRIPTS_DIR / "run_real_dwg_regression.py"),
         "--manifest", str(Path(manifest)), "--report-json", str(report_json)],
        cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=3600,
    )
    step["status"] = STATUS_OK if proc.returncode == 0 else STATUS_FAIL
    step["rc"] = proc.returncode
    step["stderr_tail"] = (proc.stderr or "").strip().splitlines()[-5:]
    step["report_json"] = str(report_json) if report_json.exists() else None
    return step, (0 if proc.returncode == 0 else 1)


# --------------------------------------------------------------------------- #
# 6) doctor
# --------------------------------------------------------------------------- #
def run_doctor(python: Path) -> tuple[dict, int]:
    proc = subprocess.run(
        [str(python), str(SCRIPTS_DIR / "doctor.py"), "--json-only"],
        cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=120,
    )
    ok = proc.returncode == 0
    try:
        report = json.loads(proc.stdout or "{}")
    except Exception as exc:
        report = {"error": f"doctor 输出解析失败: {exc}"}
    return ({"name": "doctor", "ok": ok, "rc": proc.returncode, "report": report,
             "stderr_tail": (proc.stderr or "").strip().splitlines()[-5:]},
            (0 if ok else 1))


# --------------------------------------------------------------------------- #
# 7) 汇总报告
# --------------------------------------------------------------------------- #
def _md_report(report: dict) -> str:
    summary = report.get("summary") or {}
    L = ["# cad-file-reader 自测/回归三合一报告", "",
         f"- 生成时间：`{report.get('generated_at')}`",
         f"- 技能根目录：`{report.get('skill_root')}`",
         f"- 总体状态：**{('PASS' if summary.get('ok') else 'FAIL')}**"
         f"（通过 {summary.get('steps_pass')} / {summary.get('steps_total')}"
         f"，跳过 {summary.get('steps_skip')}，失败 {summary.get('steps_fail')}）", ""]
    doctor = report.get("doctor") or {}
    L += ["## 1) doctor 环境体检", ""]
    if doctor.get("ok"):
        caps = (doctor.get("report") or {}).get("tier0", {}).get("capabilities", {})
        for key, val in caps.items():
            L.append(f"- `{key}`：{val.get('status')}")
    elif doctor.get("status") == STATUS_SKIP:
        L.append("- 已跳过")
    else:
        L.append("- 运行失败，见 JSON 报告 stderr_tail")
    L.append("")

    unit = report.get("unit_tests") or {}
    L += ["## 2) 全量自测", "", f"- 运行：{unit.get('tests_run', 0)} 项",
          f"- 失败：{unit.get('failures', 0)}，错误：{unit.get('errors', 0)}"]
    if unit.get("failed_tests"):
        L.append("- 失败用例：" + "、".join(unit["failed_tests"][:20]))
    L.append("")

    schema = report.get("schema_contract") or {}
    L += ["## 3) schema + cad_validate 契约校验", ""]
    for item in schema.get("schemas", []):
        L.append(f"- `{item['schema']}`：{'OK' if item['ok'] else 'FAIL'}"
                 f"（样例 {len(item['samples'])} 个，含负向不变量）")
    cv = schema.get("cad_validate_samples") or {}
    L.append(f"- cad_validate.py 样例：{'OK' if cv.get('ok') else 'FAIL'}（{len(cv.get('checks') or [])} 个）")
    L.append("")

    sample = report.get("sample_dxf") or {}
    L += ["## 4) 样例回归（sample_room.dxf）", ""]
    if sample.get("ok"):
        d = sample.get("detail", {})
        L.append(f"- cad_scan rc=0，文字 {d.get('text_total')} 条，文件 {d.get('files')} 个，契约校验通过")
    elif sample.get("status") == STATUS_SKIP:
        L.append("- 已跳过")
    else:
        L.append("- FAIL：" + str(sample.get("detail")))
    L.append("")

    bad = report.get("bad_file_invariants") or {}
    L += ["## 5) 坏文件不变量", "", f"- {'OK' if bad.get('ok') else 'FAIL'}（{bad.get('elapsed_seconds', '?')}s）"]
    for c in bad.get("checks", []):
        L.append(f"  - {c['case']}：{'OK' if c['ok'] else 'FAIL'} — {c.get('detail')}")
    L.append("")

    reg = report.get("real_dwg_regression") or {}
    L += ["## 6) 真实 DWG 回归", "", f"- 状态：{reg.get('status')}"
          + (f"（rc={reg.get('rc')}）" if reg.get("rc") is not None else "")]
    if reg.get("report_json"):
        L.append(f"- 报告：`{reg['report_json']}`")
    L += ["", "---", "*三合一报告由 `scripts/self_test.py` 生成。*"]
    return "\n".join(L)


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="cad-file-reader 统一自测/回归闭环")
    ap.add_argument("--manifest", default=None, help="真实 DWG 回归清单 JSON（可选，缺省则跳过回归）")
    ap.add_argument("--out-dir", default=".", help="报告输出目录（默认当前目录）")
    ap.add_argument("--report-json", default=None, help="自定义报告 JSON 路径")
    ap.add_argument("--report-md", default=None, help="自定义报告 Markdown 路径")
    ap.add_argument("--json-only", action="store_true", help="只输出 JSON 到 stdout，不写文件")
    ap.add_argument("--skip-doctor", action="store_true", help="跳过 doctor")
    ap.add_argument("--skip-unit", action="store_true", help="跳过全量 unittest")
    ap.add_argument("--skip-schema", action="store_true", help="跳过 schema/cad_validate 校验")
    ap.add_argument("--skip-sample", action="store_true", help="跳过样例 DXF 回归")
    ap.add_argument("--unit-json", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.unit_json:
        return cmd_unit_json()

    python = _resolve_python()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    steps: list[tuple[str, dict, int]] = []
    if not args.skip_doctor:
        doctor, rc = run_doctor(python)
        steps.append(("doctor", doctor, rc))
    else:
        steps.append(("doctor", {"status": STATUS_SKIP, "detail": "skip-doctor"}, 0))

    if not args.skip_unit:
        unit, rc = run_unit_tests(python)
        steps.append(("unit_tests", unit, rc))
    else:
        steps.append(("unit_tests", {"status": STATUS_SKIP, "detail": "skip-unit"}, 0))

    if not args.skip_schema:
        schema_step, rc = run_schema_steps(python)
        steps.append(("schema_contract", schema_step, rc))
    else:
        steps.append(("schema_contract", {"status": STATUS_SKIP, "detail": "skip-schema"}, 0))

    if not args.skip_sample:
        sample, rc = run_sample_regression(python)
        steps.append(("sample_dxf", sample, rc))
    else:
        steps.append(("sample_dxf", {"status": STATUS_SKIP, "detail": "skip-sample"}, 0))

    bad, rc_bad = run_bad_file_invariants(python)
    steps.append(("bad_file_invariants", bad, rc_bad))

    reg, rc_reg = run_real_dwg_regression(python, args.manifest, out_dir)
    steps.append(("real_dwg_regression", reg, rc_reg))

    report: dict = {
        "tool": "cad-file-reader-self-test",
        "schema": REPORT_SCHEMA,
        "generated_at": _now(),
        "skill_root": str(SKILL_DIR),
        "cli": {"manifest": str(Path(args.manifest).resolve()) if args.manifest else None,
                "out_dir": str(out_dir),
                "skip_doctor": args.skip_doctor,
                "skip_unit": args.skip_unit,
                "skip_schema": args.skip_schema,
                "skip_sample": args.skip_sample},
    }
    for key, step, _ in steps:
        report[key] = step

    failed = 0
    fail_steps = []
    for name, step, rc in steps:
        if step.get("status") == STATUS_SKIP:
            continue
        if step.get("ok") is not True and rc != 0:
            failed += 1
            fail_steps.append(name)
    report["summary"] = {
        "ok": failed == 0,
        "steps_total": len(steps),
        "steps_pass": sum(1 for _, s, rc in steps
                          if s.get("status") != STATUS_SKIP and (s.get("ok") is True or rc == 0)),
        "steps_skip": sum(1 for _, s, _ in steps if s.get("status") == STATUS_SKIP),
        "steps_fail": failed,
        "failed_steps": fail_steps,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_only:
        print(text)
        return 0 if report["summary"]["ok"] else 1

    report_json = Path(args.report_json) if args.report_json else out_dir / "cad-self-test-report.json"
    report_md = Path(args.report_md) if args.report_md else report_json.with_suffix(".md")
    report_json.write_text(text + "\n", encoding="utf-8")
    report_md.write_text(_md_report(report), encoding="utf-8")
    print(f"✅ 三合一报告已写出：{report_json}")
    print(f"✅ Markdown 摘要已写出：{report_md}")
    print(text)
    return 0 if report["summary"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
