#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qto-project/v1 联动模型：主键、目录约定、占位、包装与项目报告。

P0 内容：五件套联动的地图契约全部放在底座 cad-file-reader。
- project_key 三级规则：显式(.qto/project.yaml) -> 图内推断(source=auto) -> 文件级回退(source=file, review_required=true)。
- 目录约定：<项目目录>/.qto/project.yaml、识别/<专业slug>/、算量/<专业>/（P1）、汇总/（P2）。
- 输出契约：在 cad-file-reader/v0 之上追加可选顶层字段 qto_spec/project_key/draft_type/specialty/producer/placeholder；
  旧 v0 输出不改名不改语义，校验器只 warning 不 fail。

本模块不改四个算量既有算法与口径，不输出最终工程量/金额。
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

QTO_SPEC = "qto-project/v1"
QTO_VERSION = "0.1.0"
LEGACY_SPEC = "cad-file-reader/v0"
PROJECT_YAML_REL = Path(".qto") / "project.yaml"
RECOG_DIR = "识别"
QTY_DIR = "算量"
SUMMARY_DIR = "汇总"
PLACEHOLDER_NOT_INSTALLED = "not_installed"

# 正式 slug 映射（发布 slug 为准；本机目录可能不同）。发布包不携带本机绝对路径。
SKILL_MAP = [
    {"slug": "cad-file-reader", "short": "cad", "role": "recognition", "default_status": "recognition"},
    {"slug": "tujian-suanliang", "short": "tujian", "role": "quantity", "default_status": "not_installed"},
    {"slug": "anzhuang-suanliang", "short": "anzhuang", "role": "quantity", "default_status": "not_installed"},
    {"slug": "zhuangshi-suanliang", "short": "zhuangshi", "role": "quantity", "default_status": "not_installed"},
    {"slug": "yuanlin-suanliang", "short": "yuanlin", "role": "quantity", "default_status": "not_installed"},
]
SKILL_SLUGS = [s["slug"] for s in SKILL_MAP]
DRAFT_TYPES = ("概算", "物资计划", "draft_type_pending")
KEY_SOURCES = ("explicit", "auto", "file")
PROJECT_KEY_FIELDS = ("project", "building", "floor", "zone", "room", "specialty", "source", "review_required")
ILLEGAL_FILENAME_CHARS = re.compile(r'[/\\:*?"<>|]')
FILENAME_RE = re.compile(r"^(?P<key>.+)__(?P<slug>[a-zA-Z0-9][a-zA-Z0-9-]*)__(?P<date>\d{8})\.json$")


def safe_name(value: Any) -> str:
    """project_key_safe：去掉 / \\ : * ? \" < > | 并把空白折叠为下划线。"""
    if value is None:
        return ""
    text = str(value).strip()
    text = ILLEGAL_FILENAME_CHARS.sub("_", text)
    text = re.sub(r"\s+", "_", text)
    return text.strip("_. ")


def default_project_key(project: str, specialty: str, source: str = "file", building: str = "",
                        floor: str = "", zone: str = "", room: str = "",
                        review_required: bool | None = None) -> dict[str, Any]:
    if review_required is None:
        review_required = source == "file"
    return {
        "project": project,
        "building": building,
        "floor": floor,
        "zone": zone,
        "room": room,
        "specialty": specialty,
        "source": source,
        "review_required": review_required,
    }


def make_qto(payload: dict[str, Any], project_key: dict[str, Any], specialty: str,
             draft_type: str = "draft_type_pending", placeholder: dict[str, Any] | None = None) -> dict[str, Any]:
    """在 v0 contract 顶层追加 qto-project 可选字段，保持 v0 语义不变。"""
    p = copy.deepcopy(payload)
    p["qto_spec"] = QTO_SPEC
    p["qto_version"] = QTO_VERSION
    p["project_key"] = project_key
    p["specialty"] = specialty
    p["draft_type"] = draft_type if draft_type in DRAFT_TYPES else "draft_type_pending"
    p["placeholder"] = None
    if placeholder is not None:
        p["placeholder"] = placeholder
    p.setdefault("producer", {"skill": "cad-file-reader", "role": "recognition"})
    return p


# ---------------- 极简 YAML subset（项目文件只有 1~2 层，避免 PyYAML 依赖） ----------------

def dump_simple_yaml(data: dict[str, Any]) -> str:
    def scalar(v: Any) -> str:
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        s = str(v)
        if s == "":
            return '""'
        if any(ch in s for ch in ":#\n\"'") or s != s.strip():
            return json.dumps(s, ensure_ascii=False)
        return s

    lines: list[str] = []
    for k, v in data.items():
        lines.append(f"{k}:")
        if isinstance(v, dict):
            for k2, v2 in v.items():
                if isinstance(v2, dict):
                    lines.append(f"  {k2}:")
                    for k3, v3 in v2.items():
                        lines.append(f"    {k3}: {scalar(v3)}")
                elif isinstance(v2, list):
                    lines.append(f"  {k2}:")
                    for item in v2:
                        lines.append(f"    - {scalar(item)}")
                else:
                    lines.append(f"  {k2}: {scalar(v2)}")
        elif isinstance(v, list):
            for item in v:
                lines.append(f"  - {scalar(item)}")
        else:
            if v is None:
                lines[-1] = f"{k}: null"
            else:
                lines[-1] = f"{k}: {scalar(v)}"
    return "\n".join(lines) + "\n"


def _parse_scalar(s: str) -> Any:
    s = s.strip()
    if s in ("null", "~", ""):
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", s):
        return float(s)
    if s.startswith('"') and s.endswith('"'):
        try:
            return json.loads(s)
        except Exception:
            return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    return s


def _strip_inline_comment(s: str) -> str:
    out = []
    quote = None
    for i, ch in enumerate(s):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ('"', "'"):
            quote = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def load_simple_yaml(text: str) -> dict[str, Any]:
    """解析本套 schema 使用的 1~2 层 YAML subset。"""
    root: dict[str, Any] = {}
    top_key: str | None = None
    sub_key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = _strip_inline_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()
        if indent == 0:
            m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", content)
            if not m:
                raise ValueError(f"无法解析顶层行: {content}")
            top_key, val = m.group(1), m.group(2).strip()
            if val == "":
                root[top_key] = {}
                sub_key = None
            else:
                root[top_key] = _parse_scalar(val)
                sub_key = None
        elif indent == 2:
            if top_key is None:
                continue
            m = re.match(r"^-\s+(.*)$", content)
            if m:
                root.setdefault(top_key, []).append(_parse_scalar(m.group(1)))
                sub_key = None
                continue
            m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", content)
            if not m:
                raise ValueError(f"无法解析二级行: {content}")
            sub_key = m.group(1)
            val = m.group(2).strip()
            cur = root.setdefault(top_key, {})
            if not isinstance(cur, dict):
                cur = {}
                root[top_key] = cur
            if val == "":
                cur[sub_key] = {}
            else:
                cur[sub_key] = _parse_scalar(val)
        elif indent >= 4:
            if not isinstance(root.get(top_key, {}), dict):
                continue
            cur = root[top_key]
            if sub_key is None:
                continue
            if not isinstance(cur.get(sub_key), list):
                cur[sub_key] = []
            m = re.match(r"^-\s+(.*)$", content)
            if m:
                cur[sub_key].append(_parse_scalar(m.group(1)))
    return root


def read_project_yaml(project_dir: Path) -> dict[str, Any]:
    p = project_dir / PROJECT_YAML_REL
    if not p.is_file():
        return {}
    return load_simple_yaml(p.read_text(encoding="utf-8"))


def write_project_yaml(project_dir: Path, data: dict[str, Any]) -> Path:
    p = project_dir / PROJECT_YAML_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dump_simple_yaml(data), encoding="utf-8")
    return p


def build_project_yaml(project: str, specialties: dict[str, str] | None = None,
                       source: str = "explicit", building: str = "", floor: str = "",
                       zone: str = "", room: str = "", created_at: str | None = None) -> dict[str, Any]:
    if created_at is None:
        created_at = date.today().isoformat()
    if specialties is None:
        specialties = {s["slug"]: s["default_status"] for s in SKILL_MAP}
    return {
        "schema": "qto-project/v1",
        "project_key": {
            "project": project,
            "building": building,
            "floor": floor,
            "zone": zone,
            "room": room,
            "specialty": "",
            "source": source,
            "review_required": False,
        },
        "base_skill": "cad-file-reader",
        "specialties": specialties,
        "created_at": created_at,
    }


def init_project(project_dir: Path, project: str, source: str = "explicit",
                 building: str = "", floor: str = "", zone: str = "", room: str = "",
                 recognized: list[str] | None = None) -> dict[str, Path]:
    """建 .qto/ 与 识别/、算量/、汇总/ 目录；默认只 base 识别已装，四算量占位 not_installed。"""
    project_dir = Path(project_dir)
    (project_dir / RECOG_DIR).mkdir(parents=True, exist_ok=True)
    (project_dir / QTY_DIR).mkdir(parents=True, exist_ok=True)
    (project_dir / SUMMARY_DIR).mkdir(parents=True, exist_ok=True)
    specialties = {s["slug"]: s["default_status"] for s in SKILL_MAP}
    if recognized:
        for slug in recognized:
            if slug in specialties:
                specialties[slug] = "active"
            (project_dir / RECOG_DIR / slug).mkdir(parents=True, exist_ok=True)
    for s in SKILLS_ALL:
        (project_dir / RECOG_DIR / s["slug"]).mkdir(parents=True, exist_ok=True)
    yml = write_project_yaml(project_dir, build_project_yaml(
        project, specialties=specialties, source=source, building=building,
        floor=floor, zone=zone, room=room))
    return {"yaml": yml}


SKILLS_ALL = SKILL_MAP


def _load_source(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(source, dict):
        return copy.deepcopy(source)
    p = Path(source)
    return json.loads(p.read_text(encoding="utf-8"))


def _trim_candidates(payload: dict[str, Any], max_candidates: int | None) -> dict[str, Any]:
    if not max_candidates or max_candidates <= 0:
        return payload
    contract = payload.get("contract")
    if not isinstance(contract, dict):
        return payload
    for key in ("candidates", "review_candidates"):
        rows = contract.get(key)
        if isinstance(rows, list) and len(rows) > max_candidates:
            contract[key] = rows[:max_candidates]
    cand = contract.get("candidates") or []
    rev = contract.get("review_candidates") or []
    summary = contract.get("summary")
    if isinstance(summary, dict):
        summary["total"] = len(cand) + len(rev)
        summary["candidate_count"] = len(cand)
        summary["review_required"] = len(rev)
        summary["confirmed_evidence"] = sum(1 for r in cand if r.get("confidence_tier") == "confirmed_evidence")
        summary["inferred_candidate"] = sum(1 for r in cand if r.get("confidence_tier") == "inferred_candidate")
        contract["summary"] = summary
    return payload


def wrap(source: str | Path | dict[str, Any], specialty: str, project_key: dict[str, Any],
         draft_type: str = "draft_type_pending", max_candidates: int | None = None,
         allow_big: bool = False, max_source_mb: float = 10.0) -> dict[str, Any]:
    """把既有识图/测量候选包装成带 qto-project/v1 字段的输出。"""
    if specialty not in SKILL_SLUGS:
        raise ValueError(f"unknown specialty slug: {specialty}")
    if isinstance(source, (str, Path)) and not isinstance(source, dict):
        size = Path(source).stat().st_size / 1e6
        if size > max_source_mb and not allow_big:
            raise RuntimeError(f"源文件 {size:.1f} MB > {max_source_mb} MB；大文件请先评估资源，或加 --allow-big 显式处理")
    data = _load_source(source)
    if isinstance(data.get("contract"), dict) and data["contract"].get("schema") == LEGACY_SPEC:
        payload = data
    else:
        from cad_contract import contractize_payload
        payload = contractize_payload(data)
    payload = _trim_candidates(payload, max_candidates)
    return make_qto(payload, project_key, specialty, draft_type=draft_type)


def make_placeholder_payload(specialty: str, project_key: dict[str, Any], note: str) -> dict[str, Any]:
    contract = {
        "schema": LEGACY_SPEC,
        "source": "",
        "origin_schema": "qto-placeholder",
        "summary": {"total": 0, "confirmed_evidence": 0, "inferred_candidate": 0,
                    "review_required": 0, "candidate_count": 0, "duplicate_candidate": 0},
        "review_reasons": [],
        "candidates": [],
        "review_candidates": [],
        "boundary": "占位：专业未安装或 P1 未接入，不参与汇总主线。",
    }
    payload = {"contract": contract}
    return make_qto(payload, project_key, specialty,
                    placeholder={"kind": PLACEHOLDER_NOT_INSTALLED, "note": note})


def output_path(project_dir: Path, specialty: str, project_key: dict[str, Any],
                when: str | None = None) -> Path:
    if when is None:
        when = date.today().strftime("%Y%m%d")
    key = safe_name(project_key.get("project") or project_key.get("building") or "project")
    if project_key.get("building"):
        key = safe_name(project_key["building"])
    return project_dir / RECOG_DIR / specialty / f"{key}__{specialty}__{when}.json"


def _cli_init(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="qto init")
    ap.add_argument("project_dir")
    ap.add_argument("--project", required=True)
    ap.add_argument("--source", default="explicit")
    ap.add_argument("--building", default="")
    ap.add_argument("--floor", default="")
    ap.add_argument("--zone", default="")
    ap.add_argument("--room", default="")
    ap.add_argument("--recognized", nargs="+", action="append", default=[],
                       help="可多次传；例如 --recognized tujian-suanliang anzhuang-suanliang")
    args = ap.parse_args(argv)
    out = init_project(Path(args.project_dir), args.project, source=args.source,
                       building=args.building, floor=args.floor, zone=args.zone,
                       room=args.room, recognized=[x for chunk in args.recognized for x in chunk])
    print(json.dumps({"ok": True, "created": {k: str(v) for k, v in out.items()}}, ensure_ascii=False))
    return 0


def _cli_wrap(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="qto wrap")
    ap.add_argument("source")
    ap.add_argument("--specialty", required=True, choices=SKILL_SLUGS)
    ap.add_argument("--project", required=True)
    ap.add_argument("--source-mode", default="file", choices=("explicit", "auto", "file"))
    ap.add_argument("--building", default="")
    ap.add_argument("--floor", default="")
    ap.add_argument("--zone", default="")
    ap.add_argument("--room", default="")
    ap.add_argument("--draft-type", default="draft_type_pending")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-candidates", type=int, default=None)
    ap.add_argument("--allow-big", action="store_true")
    args = ap.parse_args(argv)
    pkey = default_project_key(args.project, args.specialty, source=args.source_mode,
                               building=args.building, floor=args.floor, zone=args.zone, room=args.room)
    payload = wrap(args.source, args.specialty, pkey, draft_type=args.draft_type,
                   max_candidates=args.max_candidates, allow_big=args.allow_big)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out)}, ensure_ascii=False))
    return 0


def _cli_placeholder(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="qto placeholder")
    ap.add_argument("project_dir")
    ap.add_argument("--specialty", required=True, choices=SKILL_SLUGS)
    ap.add_argument("--project", required=True)
    ap.add_argument("--building", default="")
    ap.add_argument("--note", default="P1 未接入/未安装，保持占位")
    args = ap.parse_args(argv)
    pkey = default_project_key(args.project, args.specialty, source="file", building=args.building,
                               review_required=True)
    payload = make_placeholder_payload(args.specialty, pkey, args.note)
    out = output_path(Path(args.project_dir), args.specialty, pkey)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out)}, ensure_ascii=False))
    return 0


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    if len(sys.argv) < 2:
        print("用法: qto_project init|wrap|placeholder ...", file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    argv = sys.argv[2:]
    if cmd == "init":
        return _cli_init(argv)
    if cmd == "wrap":
        return _cli_wrap(argv)
    if cmd == "placeholder":
        return _cli_placeholder(argv)
    print(f"未知子命令: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
