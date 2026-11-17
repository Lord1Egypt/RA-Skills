#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manual_package.py — 手动发布整理

过内容门禁 → 首图叠标题 → 原图按上传顺序编号 → 生成文案.txt，交用户在点评 App 里手动发布。
合成首图需要 Pillow（python3 -m pip install pillow）；没有图时仍只用标准库。

用法:
  manual_package.py --json post.json [--kind note|review] [--out-dir DIR] [--no-gate]
      post.json: {"shop": "品牌（分店）", "title": "笔记标题", "body": "…", "tags": ["#…"],
                  "images": ["/abs/01.jpg", …], "facts": {…事实卡…},
                  "cover": {"title": "<大邑 · 赵公山东线>",
                            "lines": ["起点：赵公山游客中心", "用时：3h"],
                            "picks": [0, 1, 2]},
                  "stars": 4.5, "scores": {"口味": 4}, "per_capita": 38}
      默认输出到当前项目的 dist/<店名>-发布/<评价|笔记>/（--out-dir 可覆盖）
      有图时多一张 01-封面.jpg（1080×1440），原图从 02 开始编号。

退出码: 0 成功 1 门禁未过或输入错误
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from content_gate import check, format_report, load_sibling_hooks  # noqa: E402
from cover_card import CoverError, paint_cover, validate_cover  # noqa: E402

IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png")
KIND_LABEL = {"review": "评价", "note": "笔记"}


class PublishError(Exception):
    """本文件用到 E401 门禁未过 / E402 字段或星级不合法 / E403 图片问题 / E404 首图标题；全表见 Pro 版的发布文档。"""

    def __init__(self, message: str, code: str = ""):
        super().__init__(message)
        self.code = code

    def __str__(self):
        msg = super().__str__()
        return f"[{self.code}] {msg}" if self.code else msg


def _valid_star(v, allow_half: bool) -> bool:
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not 1 <= v <= 5:
        return False
    return float(v * 2).is_integer() if allow_half else isinstance(v, int)


def validate_payload(payload: dict, kind: str, no_gate: bool, allow_half: bool = False) -> list:
    """allow_half：手动发布可填半星；自动代发只会点整星，必须是整数。"""
    if not payload.get("shop"):
        raise PublishError("缺少 shop（店铺名，用于搜索与店铺断言）", code="E402")
    if not payload.get("body"):
        raise PublishError("缺少 body", code="E402")
    if kind == "note" and not payload.get("title"):
        raise PublishError("笔记缺少 title", code="E402")
    if kind == "review":
        unit = "0.5 为步长" if allow_half else "整数"
        if not _valid_star(payload.get("stars"), allow_half):
            raise PublishError(f"评价必须给 stars（1–5，{unit}，来自用户真实打分）", code="E402")
        for label, s in (payload.get("scores") or {}).items():
            if not _valid_star(s, allow_half):
                raise PublishError(f"scores.{label} 必须是 1–5（{unit}）", code="E402")
    if not no_gate and payload.get("facts") is None:
        raise PublishError("缺少事实卡 facts（访谈事实，用于校验数字有出处）", code="E402")
    images = [Path(p) for p in payload.get("images", [])]
    for img in images:
        if not img.exists():
            raise PublishError(f"图片不存在: {img}", code="E403")
        if img.suffix.lower() not in IMAGE_SUFFIXES:
            raise PublishError(f"图片格式不支持: {img.name}（先转成 JPG）", code="E403")
    return images


def run_gate(title: str, body: str, kind: str, payload: dict) -> dict:
    report = check(title, body, kind, payload.get("facts"), per_capita=payload.get("per_capita"),
                   siblings=load_sibling_hooks(payload.get("shop")))
    print(format_report(report))
    if not report["pass"]:
        raise PublishError("内容门禁未通过（--no-gate 可跳过，但不建议）", code="E401")
    return report


def manual_text(payload: dict, kind: str) -> str:
    lines = []
    if kind == "note":
        lines += [payload["title"], ""]
    lines.append(payload["body"])
    if payload.get("tags"):
        lines += ["", " ".join(payload["tags"])]
    meta = []
    if kind == "review":
        meta.append(f"总体星级：{payload.get('stars')}")
        meta += [f"{k}：{v}" for k, v in (payload.get("scores") or {}).items()]
    if payload.get("per_capita") is not None:
        meta.append(f"人均：{payload['per_capita']}")
    if meta:
        lines += ["", "—— 发布时填写 ——"] + meta
    cover = payload.get("cover") or {}
    if cover.get("title") and cover.get("lines"):
        lines += ["", "—— 首图上的字 ——", cover["title"], *cover["lines"]]
    return "\n".join(lines) + "\n"


def stage_manual(payload: dict, kind: str, out_root: str = "", no_gate: bool = False) -> Path:
    images = validate_payload(payload, kind, no_gate, allow_half=True)
    title = payload.get("title", "") if kind == "note" else ""
    cover_spec = None
    if images:
        if not payload.get("cover"):
            raise PublishError("有图就要首图标题 cover（title + 2–4 行 lines），否则封面留不住人", code="E404")
        try:
            cover_spec = validate_cover(payload["cover"], len(images), payload.get("facts"),
                                        check_facts=not no_gate)
        except CoverError as e:
            raise PublishError(str(e), code="E404") from e
        payload = {**payload, "cover": cover_spec}
    if not no_gate:
        run_gate(title, payload["body"], kind, payload)
    root = Path(out_root) if out_root else Path.cwd() / "dist" / f"{payload['shop']}-发布"
    d = root / KIND_LABEL[kind]
    if d.exists():
        print(f"⚠️ 覆盖已存在的发布目录 {d}（之前手动改过的内容会丢失）")
        shutil.rmtree(d)
    d.mkdir(parents=True)
    try:
        start = 1
        if cover_spec:
            paint_cover(images, cover_spec, d / "01-封面.jpg")
            start = 2
        for i, img in enumerate(images, start):
            shutil.copy(img, d / f"{i:02d}-{img.name}")
        (d / "文案.txt").write_text(manual_text(payload, kind), encoding="utf-8")
    except CoverError as e:
        shutil.rmtree(d, ignore_errors=True)
        raise PublishError(str(e), code="E404") from e
    except Exception:
        shutil.rmtree(d, ignore_errors=True)
        raise
    if cover_spec:
        print(f"✅ 已整理到 {d}（封面 1 张 + 原图 {len(images)} 张 + 文案.txt）")
    else:
        print(f"✅ 已整理到 {d}（无图，只有文案.txt）")
    return d


def main():
    ap = argparse.ArgumentParser(description="手动发布整理：门禁 + 图片编号 + 文案")
    ap.add_argument("--json", required=True, help="post.json")
    ap.add_argument("--kind", default="note", choices=["note", "review"])
    ap.add_argument("--out-dir", help="默认 ./dist/<店名>-发布/")
    ap.add_argument("--no-gate", action="store_true")
    args = ap.parse_args()
    try:
        payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
        stage_manual(payload, args.kind, args.out_dir, args.no_gate)
    except PublishError as e:
        print(f"⛔ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
