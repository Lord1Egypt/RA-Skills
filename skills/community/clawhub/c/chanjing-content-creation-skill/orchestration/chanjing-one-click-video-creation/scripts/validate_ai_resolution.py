#!/usr/bin/env python3
"""
校验一键成片 workflow 中 AI 分镜与所选数字人分辨率/画幅是否一致。

- 从 `list_figures` 解析 `person_id` + `figure_type` 对应 width×height（与接口返回一致）。
- 用与 `run_render.py` 相同的 `ref_to_ai_submit_params` 映射文生 API 的 aspect_ratio、clarity。
- 未查到形象时：**默认竖屏 1080×1920**（可用 `--width`/`--height` 覆盖）。
- 可选：检查各 AI 镜 `ref_prompt` 是否含竖屏/9:16 等提示（`--check-ref-prompt`）。

用法:
  python validate_ai_resolution.py --input workflow.json
  python validate_ai_resolution.py --input workflow.json --source customised --try-both-sources
  python validate_ai_resolution.py --input workflow.json --check-ref-prompt --strict

说明: 调 `list_figures` 时默认 **`--fetch-all`**；仅调试可加 **`--no-fetch-all`** 配合 **`--max-pages`**。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

# 与 run_render 共用映射逻辑
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
import run_render as rr  # noqa: E402


def repo_root_from_here() -> Path:
    # …/skills/chanjing-content-creation-skill/orchestration/<scene>/scripts/本文件 → 上溯 6 级到仓库根
    return Path(__file__).resolve().parent.parent.parent.parent.parent.parent


def script_path(root: Path, skill: str, name: str) -> Path:
    return (
        root
        / "skills"
        / "chanjing-content-creation-skill"
        / "products"
        / skill
        / "scripts"
        / name
    )


def run_list_figures_json(
    root: Path,
    *,
    source: str,
    page_size: int,
    max_pages: int,
    fetch_all: bool = True,
) -> dict[str, Any]:
    exe = script_path(root, "chanjing-video-compose", "list_figures.py")
    cmd = [
        sys.executable,
        str(exe),
        "--source",
        source,
        "--json",
        "--page-size",
        str(page_size),
    ]
    if fetch_all:
        cmd.append("--fetch-all")
    else:
        cmd += ["--max-pages", str(max_pages)]
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(
            r.stderr.strip() or r.stdout.strip() or f"list_figures exit {r.returncode}"
        )
    return json.loads(r.stdout)


def find_figure_wh(
    payload: dict[str, Any], person_id: str, figure_type: str
) -> Optional[tuple[int, int]]:
    data = payload.get("data") or {}
    items = data.get("list") or []
    pid = person_id.strip()
    ft = (figure_type or "").strip()
    for item in items:
        if str(item.get("id", "")).strip() != pid:
            continue
        for fig in item.get("figures") or []:
            if str(fig.get("type", "")).strip() == ft:
                w = int(fig.get("width") or 0)
                h = int(fig.get("height") or 0)
                if w > 0 and h > 0:
                    return w, h
    return None


def vertical_keywords_pat() -> re.Pattern[str]:
    return re.compile(
        r"(9\s*:\s*16|vertical|portrait|native\s+portrait|upright\s+framing|竖屏|竖版)",
        re.I,
    )


def looks_like_api_person_id(s: str) -> bool:
    """蝉镜 person_id 多为 32 位 hex（可带连字符）。"""
    t = s.replace("-", "").strip()
    return len(t) == 32 and all(c in "0123456789abcdefABCDEF" for c in t)


def looks_like_figure_type(s: str) -> bool:
    if not s or len(s) > 48:
        return False
    if re.search(r"[\u4e00-\u9fff]", s):
        return False
    return re.match(r"^[a-z][a-z0-9_]*$", s, re.I) is not None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="校验 AI 分镜文生参数与所选数字人分辨率是否一致（默认竖屏参照）"
    )
    parser.add_argument("--input", required=True, help="workflow.json 路径")
    parser.add_argument(
        "--source",
        choices=("common", "customised"),
        default="common",
        help="list_figures 数据源（默认 common）",
    )
    parser.add_argument(
        "--try-both-sources",
        action="store_true",
        help="先在 --source 查找，失败则自动再试另一数据源",
    )
    parser.add_argument("--page-size", type=int, default=30)
    parser.add_argument("--max-pages", type=int, default=25)
    parser.add_argument(
        "--no-fetch-all",
        action="store_true",
        help="不全量拉公共列表，仅用 --max-pages（调试；正式选型勿用）",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1080,
        help="未查到形象时的参照宽（默认 1080，竖屏）",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1920,
        help="未查到形象时的参照高（默认 1920，竖屏）",
    )
    parser.add_argument(
        "--check-ref-prompt",
        action="store_true",
        help="检查 AI 镜 ref_prompt 是否含竖屏/9:16 等关键词（与竖屏参照一致时）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="与 --check-ref-prompt 联用：缺失关键词时 exit 1",
    )
    args = parser.parse_args()

    inp = Path(args.input).resolve()
    root = repo_root_from_here()
    data = json.loads(inp.read_text(encoding="utf-8"))
    scenes = data.get("scenes") or []
    if not isinstance(scenes, list):
        raise SystemExit("workflow 缺少 scenes[]")

    ai_scenes = [s for s in scenes if not s.get("use_avatar")]
    if not ai_scenes:
        out = {
            "ok": True,
            "skipped": True,
            "reason": "无 AI 镜（use_avatar=false），无需校验文生画幅",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    person_id = (data.get("person_id") or data.get("avatar_id") or "").strip()
    figure_type = (data.get("figure_type") or "").strip()
    need_lookup = bool(
        person_id
        and figure_type
        and looks_like_api_person_id(person_id)
        and looks_like_figure_type(figure_type)
    )
    if person_id and figure_type and not need_lookup:
        sys.stderr.write(
            "提示: person_id/figure_type 非接口典型格式，跳过 list_figures，使用默认竖屏参照。\n"
        )
    elif not person_id or not figure_type:
        sys.stderr.write(
            f"警告: 缺少 person_id 或 figure_type，使用默认竖屏参照 {args.width}×{args.height}。\n"
        )

    w, h = args.width, args.height
    lookup_source: Optional[str] = None
    lookup_ok = False

    if need_lookup:
        sources = [args.source]
        if args.try_both_sources:
            sources = ["common", "customised"]
            if args.source == "customised":
                sources = ["customised", "common"]
        last_err: Optional[str] = None
        for src in sources:
            try:
                payload = run_list_figures_json(
                    root,
                    source=src,
                    page_size=args.page_size,
                    max_pages=args.max_pages,
                    fetch_all=not args.no_fetch_all,
                )
                wh = find_figure_wh(payload, person_id, figure_type)
                if wh:
                    w, h = wh
                    lookup_source = src
                    lookup_ok = True
                    break
            except Exception as e:
                last_err = str(e)
        if not lookup_ok:
            if last_err:
                sys.stderr.write(
                    f"警告: list_figures 请求失败，使用默认参照 {w}×{h}。详情: {last_err}\n"
                )
            else:
                sys.stderr.write(
                    f"警告: 已在列表中查找但未匹配 person_id/figure_type，使用默认参照 {w}×{h}；"
                    "可增大 --max-pages 或换 --source。\n"
                )
    try:
        aspect_ratio, clarity = rr.ref_to_ai_submit_params({"width": w, "height": h})
    except SystemExit as e:
        raise SystemExit(str(e))

    issues: list[str] = []
    wf_ar = (data.get("ai_aspect_ratio") or data.get("aspect_ratio") or "").strip()
    wf_cl = data.get("ai_clarity")
    if wf_ar and wf_ar != aspect_ratio:
        issues.append(
            f"workflow 声明 ai_aspect_ratio/aspect_ratio={wf_ar!r}，与数字人映射 {aspect_ratio!r} 不一致"
        )
    if wf_cl is not None and str(wf_cl).strip() != "" and int(wf_cl) != int(clarity):
        issues.append(
            f"workflow 声明 ai_clarity={wf_cl!r}，与数字人映射 {clarity!r} 不一致"
        )

    ref_prompt_warnings: list[str] = []
    if args.check_ref_prompt and aspect_ratio == "9:16":
        pat = vertical_keywords_pat()
        for s in ai_scenes:
            sid = s.get("scene_id")
            rp = (s.get("ref_prompt") or "").strip()
            if not pat.search(rp):
                ref_prompt_warnings.append(
                    f"scene_id={sid} ref_prompt 未明显包含竖屏/9:16 类约束，可能与 {aspect_ratio} 数字人不一致"
                )

    if args.strict and ref_prompt_warnings:
        issues.extend(ref_prompt_warnings)

    ok = not issues
    result: dict[str, Any] = {
        "ok": ok,
        "display_width": w,
        "display_height": h,
        "expected_aspect_ratio": aspect_ratio,
        "expected_clarity": clarity,
        "lookup_ok": lookup_ok,
        "lookup_source": lookup_source,
        "person_id": person_id or None,
        "figure_type": figure_type or None,
        "ai_scene_ids": [s.get("scene_id") for s in ai_scenes],
        "issues": issues,
        "ref_prompt_warnings": ref_prompt_warnings,
        "hint": "submit_task 请使用上述 aspect_ratio 与 clarity；与 run_render 行为一致。",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
