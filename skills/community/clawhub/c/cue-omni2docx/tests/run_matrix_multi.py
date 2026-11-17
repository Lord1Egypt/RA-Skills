#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_matrix_multi.py — omni2docx 三格式闭环回归（展示 HTML / 汇报 PPTX）+ 专项。

读取 tests/fixtures/ 里的 _t_M*.json 中间件（真实语料，含 grounding/outline），
批量渲染 HTML 与 PPTX，并用随 skill 发布的 validate_html.py / validate_pptx.py 验收
（回归同时覆盖验收器本身）；docx 引擎回归见 run_matrix_test.py。
专项用例：多源合并（HTML+PPTX）、--md 直出、空 markdown、纯表格。

路径全部相对本文件，跨平台可跑（python3 即可，需装 python-docx）。
生成产物落在 tests/out/（不入库，见 .gitignore）。
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
OUT = HERE / "out"
SKILL = HERE.parent / "scripts"
PY = sys.executable
HTML = str(SKILL / "render_html.py")
PPTX = str(SKILL / "render_pptx.py")
VH = str(SKILL / "validate_html.py")
VP = str(SKILL / "validate_pptx.py")

PROFILE_OF = [
    ("_t_M01_etf_xlsx_gov", "gov"), ("_t_M02_bond_pdf_finance", "finance"),
    ("_t_M03_report_pdf_legal", "legal"), ("_t_M04_html_academic", "academic"),
    ("_t_M04_html_academic_quote", "academic"), ("_t_M05_audio_default", "default"),
    ("_t_M06_docx_custom_profile", '{"body_east":"宋体","body_size":11,"line_spacing":"1.5倍"}'),
    ("_t_M07_pptx_default", "default"), ("_t_M08_jpg_ocr_strip", "default"),
    ("_t_M09_huge1000p_gov", "gov"), ("_t_M10_truncated_default", "default"),
    ("_t_M11_edge_all_flags", "academic"), ("_t_M12_edge_default_noStrip", "default"),
]

MAX_SLIDES = 80


def run(cmd):
    return subprocess.run([PY] + cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def verdict(out_text):
    for line in out_text.splitlines():
        if line.startswith("判定"):
            return "PASS" if "PASS" in line else line.strip()
    return "FAIL(无判定行)"


def check_html(src_json, out_html, profile):
    r = run([HTML, "--json", str(src_json), "--out", str(out_html),
             "--profile", profile, "--page-marks"])
    if r.returncode != 0:
        return "FAIL(render): %s" % ((r.stderr.strip().splitlines() or ["?"])[-1][:90])
    v = run([VH, "--json", str(src_json), "--html", str(out_html)])
    return verdict(v.stdout) if v.returncode == 0 else "FAIL(验收): %s" % v.stdout.strip()[-90:]


def check_pptx(src_json, out_pptx, profile):
    r = run([PPTX, "--json", str(src_json), "--out", str(out_pptx),
             "--profile", profile, "--max-slides", str(MAX_SLIDES)])
    if r.returncode != 0:
        return "FAIL(render): %s" % ((r.stderr.strip().splitlines() or ["?"])[-1][:90])
    v = run([VP, "--json", str(src_json), "--pptx", str(out_pptx),
             "--max-slides", str(MAX_SLIDES)])
    return verdict(v.stdout) if v.returncode == 0 else "FAIL(验收): %s" % v.stdout.strip()[-90:]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, profile in PROFILE_OF:
        src = FIX / (name + ".json")
        if not src.exists():
            rows.append((name + " SKIP(无源)", "")); continue
        rows.append((name + " ·HTML",
                     check_html(src, OUT / ("r_%s.html" % name), profile)))
        rows.append((name + " ·PPTX",
                     check_pptx(src, OUT / ("r_%s.pptx" % name), profile)))

    # ---- 专项 1：多源合并（3 个真实源 + analysis）----
    multi = OUT / "_spec_multisource.json"
    sources = []
    for n in ("_t_M01_etf_xlsx_gov", "_t_M05_audio_default", "_t_M04_html_academic"):
        d = json.load(open(FIX / (n + ".json"), encoding="utf-8"))
        sources.append({"source": n.replace("_t_", "").replace("_", " "),
                        "markdown": d.get("markdown") or "",
                        "grounding": d.get("grounding"),
                        "outline": d.get("outline"), "detail": "text"})
    multi.write_text(json.dumps(
        {"title": "多源合并专项", "analysis": {
            "source": "整合分析",
            "markdown": "# 综合结论\n\n三份来源交叉验证：覆盖率口径一致。"},
         "sources": sources}, ensure_ascii=False), encoding="utf-8")
    rows.append(("spec 多源 ·HTML",
                 check_html(multi, OUT / "r_spec_multi.html", "gov")))
    rows.append(("spec 多源 ·PPTX",
                 check_pptx(multi, OUT / "r_spec_multi.pptx", "gov")))

    # ---- 专项 2：--md 直出（不依赖 omni 的场景①）----
    md_src = OUT / "_spec_direct.md"
    d1 = json.load(open(FIX / "_t_M01_etf_xlsx_gov.json", encoding="utf-8"))
    md_src.write_text(d1.get("markdown") or "", encoding="utf-8")
    r = run([HTML, "--md", str(md_src), "--out", str(OUT / "r_spec_direct.html"),
             "--profile", "gov"])
    v = run([VH, "--md", str(md_src), "--html", str(OUT / "r_spec_direct.html")])
    rows.append(("spec --md ·HTML",
                 "FAIL(render)" if r.returncode else verdict(v.stdout)))
    r = run([PPTX, "--md", str(md_src), "--out", str(OUT / "r_spec_direct.pptx"),
             "--profile", "gov", "--max-slides", str(MAX_SLIDES)])
    v = run([VP, "--md", str(md_src), "--pptx", str(OUT / "r_spec_direct.pptx"),
             "--max-slides", str(MAX_SLIDES)])
    rows.append(("spec --md ·PPTX",
                 "FAIL(render)" if r.returncode else verdict(v.stdout)))

    # ---- 专项 3：空 markdown / 纯表格边界 ----
    for tag, mdtext in (("empty", "# 空文档\n\n（正文待补充。）\n"),
                        ("tableonly", "| 列一 | 列二 |\n|---|---|\n| 甲 | 1 |\n| 乙 | 2 |\n")):
        f = OUT / ("_spec_%s.json" % tag)
        f.write_text(json.dumps({"markdown": mdtext, "source": tag},
                                ensure_ascii=False), encoding="utf-8")
        rows.append(("spec %s ·HTML" % tag,
                     check_html(f, OUT / ("r_spec_%s.html" % tag), "default")))
        rows.append(("spec %s ·PPTX" % tag,
                     check_pptx(f, OUT / ("r_spec_%s.pptx" % tag), "default")))

    # ---- 专项 4：--inline 公众号导出（0.6.0 起手工验证，补回归）----
    # 断言：验收 PASS + style 属性内联落地 + var() 零残留 + 无外链（自包含保持）
    inline_out = OUT / "r_spec_inline.html"
    r = run([HTML, "--md", str(md_src), "--out", str(inline_out),
             "--profile", "gov", "--inline"])
    if r.returncode != 0:
        rows.append(("spec --inline ·HTML",
                     "FAIL(render): %s" % ((r.stderr.strip().splitlines() or ["?"])[-1][:90])))
    else:
        v = run([VH, "--md", str(md_src), "--html", str(inline_out)])
        verdict_str = verdict(v.stdout) if v.returncode == 0 else "FAIL(验收): %s" % v.stdout.strip()[-90:]
        if verdict_str != "PASS":
            rows.append(("spec --inline ·HTML", verdict_str))
        else:
            h = inline_out.read_text(encoding="utf-8")
            problems = []
            n_inline_style = h.count('style="')
            if n_inline_style < 20:  # 实测样本 55 元素级；留足余量防回归退化
                problems.append("style 属性过少(%d)" % n_inline_style)
            import re as _re
            # <style> 块是刻意保留的（悬停/斑马纹本地不退化），var() 只允许出现在那里；
            # style 属性里出现 var() 才说明变量没解掉（粘贴到剥离 <style> 的环境会掉样式）
            h_nostyle = _re.sub(r"<style[\s\S]*?</style>", "", h)
            if "var(" in h_nostyle:
                problems.append("style 属性 var() 残留")
            ext = _re.findall(r'(?:src|href)="(https?://[^"]+)"', h)
            if ext:
                problems.append("外链 %d 处" % len(ext))
            rows.append(("spec --inline ·HTML",
                         "PASS（内联 style %d 处）" % n_inline_style if not problems
                         else "FAIL(%s)" % "; ".join(problems)))

    # ---- 汇总 ----
    print("=" * 72)
    bad = 0
    for name, res in rows:
        ok = res == "PASS" or res.startswith("PASS（")  # 带附加信息的 PASS 变体（如 --inline 内联计数）
        bad += 0 if ok else 1
        print("%-38s %s" % (name, res))
    print("=" * 72)
    print("合计 %d 例，PASS %d，FAIL %d" % (len(rows), len(rows) - bad, bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
