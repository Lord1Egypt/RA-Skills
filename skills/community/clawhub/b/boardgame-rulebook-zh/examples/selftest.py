#!/usr/bin/env python3
"""End-to-end self-test: build a sample rulebook, extract, translate, render, and verify assets stayed put."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

from make_sample import SAMPLE_TRANSLATIONS, build_pdf  # noqa: E402
from pdf_common import (  # noqa: E402
    drawings_summary,
    page_geometry,
    page_image_infos,
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = dict(**__import__("os").environ)
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(cmd, cwd=str(cwd), text=True, encoding="utf-8",
                            errors="replace", capture_output=True, env=env)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
    return result


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def check_assets(original: Path, output: Path) -> None:
    src = fitz.open(str(original))
    out = fitz.open(str(output))
    if src.page_count != out.page_count:
        fail(f"页数变化：{src.page_count} → {out.page_count}")
    for index in range(src.page_count):
        a, b = src[index], out[index]
        if page_geometry(a) != page_geometry(b):
            fail(f"第 {index + 1} 页尺寸/旋转变化")
        if page_image_infos(a) != page_image_infos(b):
            fail(f"第 {index + 1} 页位图摘要或位置变化")
        if drawings_summary(a) != drawings_summary(b):
            fail(f"第 {index + 1} 页矢量图摘要变化")


def positive_test(base: Path) -> dict:
    sample = base / "sample.pdf"
    work = base / "work"
    out = base / "out"
    for path in (work, out):
        if path.exists():
            shutil.rmtree(path)
    build_pdf(sample)
    result = run([sys.executable, str(ROOT / "scripts" / "extract.py"),
                  str(sample), "-o", str(work), "--force", "--dpi", "120"], ROOT)
    if result.returncode != 0:
        fail("extract.py 失败")
    data = json.loads((work / "segments.json").read_text(encoding="utf-8"))
    segments = data["segments"]
    if len(segments) < 30:
        fail(f"分段过少：{len(segments)}")
    table_cells = sum(1 for seg in segments if seg.get("table"))
    inline = sum(1 for seg in segments if seg.get("inline_art"))
    if table_cells < 9:
        fail(f"表格单元识别过少：{table_cells}")
    if inline < 2:
        fail(f"内嵌图标识别过少：{inline}")

    unmatched = []
    lines = ["# selftest translations", ""]
    for seg in segments:
        text = seg["text"]
        if seg.get("suggest_keep") or text.strip().isdigit():
            value = "="
        else:
            value = SAMPLE_TRANSLATIONS.get(text, "")
            if not value:
                unmatched.append((seg["id"], text))
                value = "MISSING"
        lines.append(f"{seg['id']}\t{value}")
    if unmatched:
        for sid, text in unmatched:
            print(f"  unmatched {sid}: {text!r}")
        fail("样例译文未覆盖全部文字段")
    (work / "translations.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = run([sys.executable, str(ROOT / "scripts" / "render.py"),
                  str(sample), "-w", str(work), "-o", str(out), "--dpi", "130"], ROOT)
    if result.returncode != 0:
        fail("render.py 返回非 0（结构校验未通过）")
    report = json.loads((out / "qa" / "report.json").read_text(encoding="utf-8"))
    if report["summary"]["errors"]:
        for issue in report["issues"]:
            if issue["level"] == "error":
                print(f"  {issue['code']}: {issue['message']}")
        fail("QA 仍有错误")
    if report["summary"]["warnings"]:
        for issue in report["issues"]:
            if issue["level"] == "warning":
                print(f"  {issue['code']}: {issue['message']}")
        fail("QA 仍有警告，样例应保持干净")
    if not (report["summary"]["image_integrity"] and report["summary"]["vector_integrity"]):
        fail("图像/矢量完整性摘要未通过")

    output_pdf = out / "sample_zh.pdf"
    check_assets(sample, output_pdf)
    text = "".join(page.get_text("text") for page in fitz.open(str(output_pdf)))
    for expected in ("游戏准备", "获得2点能量", "抽1张牌", "示例：一块完成的版图。", "获得1胜利点"):
        if expected not in text:
            fail(f"输出中找不到预期译文：{expected}")
    if "MISSING" in text:
        fail("输出中残留 MISSING")

    preview = out / "qa" / "pages" / "page_0001.png"
    if preview.exists():
        shutil.copy2(preview, HERE / "demo_page1.png")
    return {
        "sample": str(sample),
        "work": str(work),
        "out": str(out),
        "segments": len(segments),
        "table_cells": table_cells,
        "inline": inline,
        "errors": report["summary"]["errors"],
        "warnings": report["summary"]["warnings"],
        "infos": report["summary"]["infos"],
    }


def negative_test(base: Path) -> dict:
    work = base / "work"
    bad_work = base / "work_bad"
    bad_out = base / "out_bad"
    if bad_work.exists():
        shutil.rmtree(bad_work)
    if bad_out.exists():
        shutil.rmtree(bad_out)
    shutil.copytree(work, bad_work)
    data = json.loads((bad_work / "segments.json").read_text(encoding="utf-8"))
    segments = data["segments"]
    lines = (bad_work / "translations.tsv").read_text(encoding="utf-8").splitlines()
    meeple_id = next((s["id"] for s in segments if "meeples" in s["text"]), None)
    table_id = next((s["id"] for s in segments if s["text"] == "Resource"), None)
    drop_id = next((s["id"] for s in segments if s["text"] == "SETUP"), None)
    emoji_id = next((s["id"] for s in segments if s["text"] == "SCORING"), None)
    if not all((meeple_id, table_id, drop_id, emoji_id)):
        fail("负向测试找不到目标段落")
    out_lines = []
    for line in lines:
        if line.startswith(drop_id + "\t"):
            continue
        if line.startswith(meeple_id + "\t"):
            sid, value = line.split("\t", 1)
            line = sid + "\t" + value.replace("米宝", "米普")
        elif line.startswith(table_id + "\t"):
            line = table_id + "\t" + "资源" * 40
        elif line.startswith(emoji_id + "\t"):
            line = emoji_id + "\t计分🎲"
        out_lines.append(line)
    (bad_work / "translations.tsv").write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    result = run([sys.executable, str(ROOT / "scripts" / "render.py"),
                  str(base / "sample.pdf"), "-w", str(bad_work), "-o", str(bad_out),
                  "--dpi", "90"], ROOT)
    if result.returncode == 0:
        fail("负向测试未被 QA 拦截")
    report = json.loads((bad_out / "qa" / "report.json").read_text(encoding="utf-8"))
    codes = {issue["code"] for issue in report["issues"] if issue["level"] == "error"}
    expected = {"glossary-wrong", "overflow", "missing-translation", "missing-glyphs"}
    missing = expected - codes
    if missing:
        fail(f"负向测试未触发：{sorted(missing)}；实际错误：{sorted(codes)}")
    return {"exit": result.returncode, "codes": sorted(codes)}


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 boardgame-rulebook-zh 端到端自测")
    parser.add_argument("--negative", action="store_true", help="同时运行故意犯错的负向测试")
    parser.add_argument("--out", default=str(HERE / "_out"), help="测试输出目录")
    args = parser.parse_args()
    base = Path(args.out).resolve()
    base.mkdir(parents=True, exist_ok=True)

    print("== 正向测试：样例规则书 ==")
    info = positive_test(base)
    print(f"通过：{info['segments']} 段（表格 {info['table_cells']}、内嵌图标 {info['inline']}），"
          f"错误 {info['errors']}、警告 {info['warnings']}、提示 {info['infos']}。")
    print(f"输出：{info['out']}")
    if args.negative:
        print("== 负向测试：错译 / 漏译 / 溢出 / 缺字形 ==")
        neg = negative_test(base)
        print(f"通过：QA 以退出码 {neg['exit']} 拦截，错误码 {', '.join(neg['codes'])}。")
    print("SELFTEST OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
