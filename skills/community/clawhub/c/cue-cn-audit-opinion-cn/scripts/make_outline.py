#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计意见稿·零通道骨架（零网络、零凭据、不依赖任何通道产物）。

把一份材料清单排成审计稿骨架：六节按序落位，来源行按清单逐条登记，
正文与结论留 [待人工]，等用户回原文补。

用法：
    python3 scripts/make_outline.py 清单.jsonl 骨架.md
    python3 scripts/make_outline.py --selftest
    python3 scripts/make_outline.py --help

清单是 JSONL，每行至少三键：
    title  材料标题（年报／审计报告）
    url    可点 http(s) 链接
    asof   检索日 YYYY-MM-DD
可选：
    id     来源编号，缺省按行序给 S1／S2…
    page   页码范围，写进锚里

退码：0 排出骨架 / 1 输入有坏行或清单为空 / 2 用法错 / 3 读不到输入。

两条硬规矩（写在这里防后人放宽）：
  · 零通道路径是**默认路径**：本脚本只读用户给的那份 JSONL，不需要 parsed-doc，也不需要凭据。
  · 坏行**逐行点名、不采信**，好行照收；空清单退 1，不出空壳。
  · 排出的骨架**故意过不了机检**——那是设计（提醒补完再交），不是待修。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-audit-opinion-cn"
REQUIRED = ("title", "url", "asof")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://\S+$")

SECTIONS = ("一、审计意见", "二、形成意见的基础", "三、关键审计事项",
            "四、其他信息与持续经营", "五、未取到与口径", "六、来源")


def mark_first_run() -> None:
    """首次运行埋点：~/.cue-usage/<slug>-<日期> 落一枚空文件。

    平台的两个下载计数器都不可信（新 listing 首 48h 一次性播种 50~60），
    本地这枚文件才是「真有人装上并跑过」的证据。任何失败静默跳过，绝不影响主流程。
    """
    try:
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001
        pass


def load_rows(text: str):
    """→ (rows, problems)。坏行逐行点名，不静默跳行。"""
    rows, problems = [], []
    for i, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            problems.append(f"第 {i} 行：非法 JSON（{exc.msg}）")
            continue
        if not isinstance(obj, dict):
            problems.append(f"第 {i} 行：不是 JSON 对象")
            continue
        miss = [k for k in REQUIRED if not str(obj.get(k) or "").strip()]
        if miss:
            problems.append(f"第 {i} 行：缺键 {'、'.join(miss)}")
            continue
        url = str(obj["url"]).strip()
        if not URL_RE.match(url):
            problems.append(f"第 {i} 行：url 不是 http(s)（{url[:40]}）")
            continue
        asof = str(obj["asof"]).strip()
        if not DATE_RE.match(asof):
            problems.append(f"第 {i} 行：asof 不是 YYYY-MM-DD（{asof[:20]}）")
            continue
        rows.append({
            "id": str(obj.get("id") or f"S{len(rows) + 1}"),
            "title": str(obj["title"]).strip(),
            "url": url,
            "asof": asof,
            "page": str(obj.get("page") or "").strip(),
        })
    return rows, problems


def render(rows) -> str:
    anchor = "骨架占位"
    if rows and rows[0]["page"]:
        anchor = f"{rows[0]['title']}·第 {rows[0]['page']} 页"
    lines = [
        "AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]",
        "",
        "主体：",
        "报告期：",
        "数据口径：审计报告（审计意见与非标事项逐项登记）",
        "",
    ]
    for head in SECTIONS[:-1]:
        lines.append(f"## {head}")
        lines.append("")
        if head.startswith("五"):
            lines.append("- 未取到：")
        else:
            lines.append(f"- 待补：「」〔锚：{anchor}〕[{rows[0]['id'] if rows else 'S1'}]")
        lines.append("")
    lines.append("## 六、来源")
    lines.append("")
    for r in rows:
        lines.append(f"- [{r['id']}] {r['title']}｜{r['url']}｜检索日 {r['asof']}")
    if not rows:
        lines.append("- ")
    lines.append("")
    return "\n".join(lines)


def selftest() -> int:
    cases = []

    good = ('{"title":"示例科技 2025 年年度报告","url":"https://example.com/a.pdf",'
            '"asof":"2026-11-09"}\n{"title":"示例科技 2024 年年度报告",'
            '"url":"https://example.com/b.pdf","asof":"2026-11-09","page":"112"}')
    rows, probs = load_rows(good)
    cases.append(("合法两行", rows, probs, 2, 0))

    rows, probs = load_rows('{"title":"x","url":"https://e.com/x","asof":"2026-11-09"}\nnot json')
    cases.append(("非法 JSON 逐行点名", rows, probs, 1, 1))

    rows, probs = load_rows('{"url":"https://e.com/x","asof":"2026-11-09"}')
    cases.append(("缺 title", rows, probs, 0, 1))

    rows, probs = load_rows('{"title":"x","url":"ftp://e.com/x","asof":"2026-11-09"}')
    cases.append(("url 非 http", rows, probs, 0, 1))

    rows, probs = load_rows('{"title":"x","url":"https://e.com/x","asof":"2026/11/09"}')
    cases.append(("asof 不合形", rows, probs, 0, 1))

    rows, probs = load_rows('{"title":"x","url":"https://e.com/x","asof":"2026-11-09","id":"S7"}')
    cases.append(("id 可省也给", rows, probs, 1, 0))

    rows, probs = load_rows("")
    cases.append(("空清单", rows, probs, 0, 0))

    bad = 0
    for name, rows, probs, want_rows, want_probs in cases:
        if len(rows) != want_rows or len(probs) != want_probs:
            bad += 1
            print(f"不合 {name}：rows={len(rows)}（应 {want_rows}）"
                  f"problems={len(probs)}（应 {want_probs}）")
        else:
            print(f"过   {name}")

    text = render(load_rows(good)[0])
    for need in ("## 一、审计意见", "## 六、来源", "检索日 2026-11-09"):
        if need not in text:
            bad += 1
            print(f"不合 骨架缺「{need}」")
    print(f"过   骨架渲染 {len(text)} 字节" if bad == 0 else "")
    print("----")
    print(f"自测 夹具={len(cases) + 1} 不合={bad}")
    return 0 if bad == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        add_help=True,
        description="材料清单 JSONL → 审计稿骨架（零网络、零凭据、零通道产物）",
    )
    ap.add_argument("listing", nargs="?", help="材料清单 JSONL 路径")
    ap.add_argument("out", nargs="?", help="骨架输出路径（缺省打印到标准输出）")
    ap.add_argument("--selftest", action="store_true", help="跑内置夹具自检")
    args = ap.parse_args(argv)

    mark_first_run()                                     # ← 解析成功之后、干正事之前

    if args.selftest:
        return selftest()
    if not args.listing:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份清单 JSONL，或用 --selftest", file=sys.stderr)
        return 2
    try:
        text = Path(args.listing).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"读不到输入：{args.listing}（{exc}）", file=sys.stderr)
        return 3

    rows, problems = load_rows(text)
    for p in problems:
        print(f"坏行 {p}", file=sys.stderr)
    if not rows:
        print("清单为空：一行可用材料都没有，不出空壳。补齐 title／url／asof 再来。",
              file=sys.stderr)
        return 1

    out = render(rows)
    if args.out:
        try:
            Path(args.out).write_text(out, encoding="utf-8")
        except OSError as exc:
            print(f"写不出骨架：{args.out}（{exc}）", file=sys.stderr)
            return 3
        print(f"骨架已落盘：{args.out}｜采信 {len(rows)} 行｜坏行 {len(problems)} 行")
    else:
        sys.stdout.write(out)
        print(f"采信 {len(rows)} 行｜坏行 {len(problems)} 行", file=sys.stderr)
    # 有坏行仍出骨架，但退 1 让调用方看得见——不静默吞掉半份清单。
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
