#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qto-project/v1 校验器：schema、必填字段、目录/文件名约定、占位完整性。

- 新输出（带 qto_spec）：校验 qto_spec/project_key/draft_type/specialty 与 v0 contract。
- 旧输出（仅 cad-file-reader/v0）：只 warning 不 fail，保证历史文件不被新规范打断。
- 输出回归口径：regression_pass（原始 v0/cad 契约是否全通过）与
  precision_note（候选需人工核对清单）分开统计。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from cad_contract import validate_contract_payload  # noqa: E402
from qto_project import (  # noqa: E402
    PLACEHOLDER_NOT_INSTALLED,
    PROJECT_YAML_REL,
    FILENAME_RE,
    LEGACY_SPEC,
    QTO_SPEC,
    RECOG_DIR,
    SKILL_SLUGS,
    DRAFT_TYPES,
    PROJECT_KEY_FIELDS,
    KEY_SOURCES,
    load_simple_yaml,
    read_project_yaml,
)


def _as_list(v: Any) -> list[Any]:
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return list(v.items())
    return []


def validate_project_yaml(project_dir: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    yaml_path = project_dir / PROJECT_YAML_REL
    if not yaml_path.is_file():
        return [f"缺少 {PROJECT_YAML_REL}"], [], {}
    data = read_project_yaml(project_dir)
    if not data:
        return [f"{PROJECT_YAML_REL} 无法解析"], [], {}
    if data.get("schema") != "qto-project/v1":
        errors.append(".qto/project.yaml schema 必须是 qto-project/v1")
    pk = data.get("project_key")
    if not isinstance(pk, dict):
        errors.append(".qto/project.yaml 缺少 project_key")
    else:
        if not pk.get("project"):
            errors.append("project_key.project 不能为空")
        if pk.get("source") not in KEY_SOURCES:
            errors.append(f"project_key.source 必须是 {'/'.join(KEY_SOURCES)}")
        if "review_required" not in pk:
            warnings.append("project_key 旧结构缺 review_required，视为需核对")
    if data.get("base_skill") != "cad-file-reader":
        errors.append("base_skill 必须是 cad-file-reader")
    specialties = data.get("specialties")
    if not isinstance(specialties, dict):
        errors.append("缺少 specialties 映射")
    else:
        missing = [s for s in SKILL_SLUGS if s not in specialties]
        if missing:
            errors.append(f"specialties 缺少占位登记: {', '.join(missing)}")
        known_status = ("active", "installed", PLACEHOLDER_NOT_INSTALLED, "recognition")
        for slug, st in specialties.items():
            if slug not in SKILL_SLUGS:
                warnings.append(f"specialties 含未登记 slug: {slug}")
            elif st not in known_status:
                warnings.append(f"specialties.{slug} 状态未知: {st}")
    return errors, warnings, data


def _validate_qto_json(path: Path) -> tuple[list[str], list[str], dict[str, Any] | None]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path.name}: 不是合法 JSON（{exc}）"], [], None

    name = FILENAME_RE.match(path.name)
    if not name:
        warnings.append(f"{path.name}: 文件名不符合 <project_key_safe>__<专业>__<YYYYMMDD>.json 约定")
    else:
        slug = name.group("slug")
        if slug not in SKILL_SLUGS:
            warnings.append(f"{path.name}: 文件名里的专业 slug 未登记: {slug}")

    if data.get("qto_spec") is None:
        # 旧 cad-file-reader/v0 输出：只 warning 不 fail
        try:
            legacy_err = validate_contract_payload(data)
        except Exception as exc:
            legacy_err = [f"{type(exc).__name__}: {exc}"]
        if legacy_err:
            warnings.append(f"{path.name}: 旧 v0 输出校验告警（不阻断）：{'；'.join(legacy_err[:5])}")
        return [], warnings, data

    if data.get("qto_spec") != QTO_SPEC:
        errors.append(f"{path.name}: qto_spec 必须是 {QTO_SPEC}")
    pk = data.get("project_key")
    if not isinstance(pk, dict):
        errors.append(f"{path.name}: 缺少 project_key")
    else:
        for field in PROJECT_KEY_FIELDS:
            if field not in pk:
                errors.append(f"{path.name}: project_key.{field} 缺失")
        if pk.get("source") not in KEY_SOURCES:
            errors.append(f"{path.name}: project_key.source 非法")
        if not isinstance(pk.get("review_required"), bool):
            errors.append(f"{path.name}: project_key.review_required 必须是布尔")
        if not pk.get("project") and pk.get("source") != "file":
            errors.append(f"{path.name}: project_key.source=file 之外必须有 project 字段")
        if pk.get("specialty") and pk["specialty"] != data.get("specialty"):
            errors.append(f"{path.name}: project_key.specialty 与顶层 specialty 不一致")
    if data.get("draft_type") not in DRAFT_TYPES:
        errors.append(f"{path.name}: draft_type 必须是 {'/'.join(DRAFT_TYPES)}")
    if not data.get("specialty"):
        errors.append(f"{path.name}: 缺少 specialty")
    ct = data.get("contract")
    if not isinstance(ct, dict):
        errors.append(f"{path.name}: 缺少 contract")
        return errors, warnings, data
    if ct.get("schema") != LEGACY_SPEC:
        errors.append(f"{path.name}: contract.schema 必须是 {LEGACY_SPEC}")
    try:
        v_err = validate_contract_payload(data)
    except Exception as exc:
        v_err = [f"{type(exc).__name__}: {exc}"]
    for e in v_err:
        errors.append(f"{path.name}: {e}")
    return errors, warnings, data


def _precision_note(path: Path, data: dict[str, Any] | None) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    if data is None:
        return notes
    ph = data.get("placeholder")
    if isinstance(ph, dict):
        notes.append({"file": path.name, "kind": ph.get("kind", "placeholder"),
                      "note": ph.get("note", "占位")})
        return notes
    contract = data.get("contract")
    if not isinstance(contract, dict):
        return notes
    for row in contract.get("review_candidates") or []:
        notes.append({
            "file": path.name,
            "id": row.get("id"),
            "kind": row.get("kind"),
            "confidence_tier": "review_required",
            "review_reasons": row.get("review_reasons") or [],
            "review_notes": row.get("review_notes") or "",
        })
    return notes


def validate_project(project_dir: Path) -> dict[str, Any]:
    project_dir = Path(project_dir)
    errors, warnings, yaml_data = validate_project_yaml(project_dir)
    specialties: dict[str, str] = {}
    if yaml_data:
        sp = yaml_data.get("specialties")
        if isinstance(sp, dict):
            specialties = sp
    missing_dirs: list[str] = []
    for slug in SKILL_SLUGS:
        d = project_dir / RECOG_DIR / slug
        if not d.is_dir():
            missing_dirs.append(slug)
    if missing_dirs:
        errors.append(f"识别/ 缺少专业目录: {', '.join(missing_dirs)}")

    files: list[dict[str, Any]] = []
    real_qto = 0
    placeholder_count = 0
    for slug in SKILL_SLUGS:
        d = project_dir / RECOG_DIR / slug
        if not d.is_dir():
            continue
        json_files = sorted(d.glob("*.json"))
        expected_status = specialties.get(slug, "not_installed")
        if not json_files and expected_status == PLACEHOLDER_NOT_INSTALLED:
            warnings.append(f"{slug}: 未安装但缺少占位文件（建议生成 placeholder）")
            continue
        if not json_files:
            errors.append(f"{slug}: 无识别 JSON 且未登记占位")
            continue
        has_placeholder = False
        for fp in json_files:
            fer, fw, fdata = _validate_qto_json(fp)
            if fdata and fdata.get("placeholder"):
                has_placeholder = True
            if fer:
                errors.extend(fer)
            if fw:
                warnings.extend(fw)
            files.append({
                "path": str(fp.relative_to(project_dir)),
                "specialty": slug,
                "name": fp.name,
                "qto_spec": fdata.get("qto_spec") if fdata else None,
                "placeholder": bool(fdata and fdata.get("placeholder")),
                "errors": fer,
                "warnings": fw,
            })
            if fdata:
                precision = _precision_note(fp, fdata)
                if fdata.get("placeholder"):
                    placeholder_count += 1
                else:
                    real_qto += 1
                files[-1]["precision_note"] = precision
        if expected_status == PLACEHOLDER_NOT_INSTALLED and not has_placeholder:
            errors.append(f"{slug}: 登记为未安装，但识别/ 下没有占位文件")
        if expected_status in ("active", "installed", "recognition") and json_files and all(
                f.get("placeholder") for f in files if f["specialty"] == slug):
            errors.append(f"{slug}: 已装/识别专业不应全是占位文件")

    regression_pass = not errors
    precision_note: list[dict[str, Any]] = []
    added_precision: set[str] = set()
    for f in files:
        for item in f.get("precision_note") or []:
            key = f"{f['path']}|{item.get('id')}|{item.get('kind')}"
            if key not in added_precision:
                added_precision.add(key)
                precision_note.append(item)
    report = {
        "schema": "qto-project/validate/v1",
        "ok": regression_pass,
        "regression_pass": regression_pass,
        "project_dir": str(project_dir),
        "base_skill": yaml_data.get("base_skill") if yaml_data else None,
        "project_key": (yaml_data or {}).get("project_key"),
        "specialties": specialties,
        "errors": errors,
        "warnings": warnings,
        "files": files,
        "file_count": len(files),
        "real_qto_count": real_qto,
        "placeholder_count": placeholder_count,
        "precision_note": precision_note,
        "precision_note_count": len(precision_note),
    }
    return report


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="qto-project/v1 项目目录校验")
    ap.add_argument("project_dir", help="项目目录（含 .qto/project.yaml）")
    ap.add_argument("--report-json", help="可选：输出报告 JSON 到文件")
    args = ap.parse_args()
    report = validate_project(Path(args.project_dir))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.report_json:
        Path(args.report_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
