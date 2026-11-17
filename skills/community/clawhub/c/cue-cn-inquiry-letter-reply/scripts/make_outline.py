#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 回复公告清单 → 问询函答复核对骨架（零网络、零凭据）

本件**不抓取问询函原文**：交易所函件在公开库里没有正式通道。这里排的是回复侧骨架，
函件原件由用户自己贴进形成稿。本脚本不联网，只读你给的那份清单。

用法：
    python3 scripts/make_outline.py 清单.jsonl 骨架.md
    python3 scripts/make_outline.py --selftest

清单是 JSONL，每行三键必需：title／url／asof（检索日 YYYY-MM-DD），id 可省按行序给 S1/S2…
坏行（非法 JSON／缺键／日期不合形／url 非 http）逐行点名、不采信；好行照收。
空清单退 1，不出空壳。排出的骨架**故意过不了机检**，是设计，不是待修。

退码：0 排出骨架 / 1 输入有坏行或清单为空 / 2 用法错 / 3 读不到输入。
"""

import argparse
import json
import re
import sys
from pathlib import Path

SLUG = "cue-cn-inquiry-letter-reply"

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED = ("title", "url", "asof")

HEADER = """# 监管问询函逐条答复核对

AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：[待人工]
文件：[待人工]
收函日：[待人工]

> 骨架只排了回复侧材料清单。**问询函原件不在公开库里**（交易所函件没有正式公开通道），
> 请自行粘贴或给本地路径后，把每一问抄进第 1 节，再逐条对到第 3 节。

"""


def mark_first_run() -> None:
    try:
        from datetime import date
        import os
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001
        pass


def parse(rows):
    """返回 (好行[(id, title, url, asof)], 坏行[(行号, 原因)])。坏行不采信、不静默跳行。"""
    good, bad = [], []
    for i, raw in enumerate(rows, 1):
        s = raw.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError as exc:
            bad.append((i, "非法 JSON：%s" % str(exc)[:40]))
            continue
        if not isinstance(obj, dict):
            bad.append((i, "不是 JSON 对象"))
            continue
        miss = [k for k in REQUIRED if not str(obj.get(k) or "").strip()]
        if miss:
            bad.append((i, "缺键：%s" % "、".join(miss)))
            continue
        asof = str(obj["asof"]).strip()
        if not ISO_DATE.match(asof):
            bad.append((i, "asof 不是 YYYY-MM-DD：%s" % asof[:20]))
            continue
        url = str(obj["url"]).strip()
        if not re.match(r"^https?://\S+$", url):
            bad.append((i, "url 不是 http(s) 地址：%s" % url[:30]))
            continue
        sid = str(obj.get("id") or "S%d" % len(good + [(None,)])).strip()
        if not re.match(r"^S\d+$", sid):
            bad.append((i, "id 须形如 S1：%s" % sid[:12]))
            continue
        good.append((sid, str(obj["title"]).strip(), url, asof))
    return good, bad


def outline(good):
    """把好行排成骨架：回复侧材料先按主体分栏，函件那三节留空给人填。"""
    out = [HEADER]
    out.append("## 1. 问询事项索引\n\n> 从问询函原件逐条抄。每条一行：`- 问题N <事项>「原句」〔锚：…〕[S#]`\n\n")
    out.append("## 2. 要求提供的材料\n\n> 每问对应要求提供的材料，逐条挂原句与锚。\n\n")
    out.append("## 3. 回复要点\n\n> 每问一行。**没答的写 `- 问题N 未取到：<缺什么>`**，不要留空。\n\n")
    out.append("## 4. 回复文件\n\n")
    if good:
        for sid, title, _url, _asof in good:
            out.append("- 主体：%s｜[%s]\n" % (title, sid))
    else:
        out.append("> 清单为空。\n")
    out.append("\n> 一条问询的公开产出通常是 3–5 份：公司本体、会计师事务所、保荐机构／律师各出。\n"
               "> 只搜公司名会漏掉中介机构那几份，缺的那几份写进第 5 节。\n\n")
    out.append("## 5. 未取到清单\n\n")
    if good:
        out.append("> 有缺项就逐条写 `- 未取到：<项名>`；确实零缺口写 `- 未取到：无`。\n")
    else:
        out.append("- 未取到：全部（清单为空）\n")
    out.append("\n## 来源\n\n")
    for sid, title, url, asof in good:
        out.append("- [%s] %s | %s | 检索日 %s\n" % (sid, title, url, asof))
    return "".join(out)


SAMPLE = [
    '{"title": "示例科技 审核问询函回复公告", "url": "https://example.com/r1", "asof": "2026-11-10"}',
    '{"id": "S2", "title": "关于示例科技审核问询函回复的专项核查意见",'
    ' "url": "https://example.com/r2", "asof": "2026-11-10"}',
]


def selftest():
    forms, bad = 0, 0

    def one(name, want, got):
        nonlocal forms, bad
        forms += 1
        if want != got:
            bad += 1
            print("FAIL 自测 %s：应 %r 实得 %r" % (name, want, got))
        else:
            print("过   自测 %s：%r" % (name, got))

    good, bads = parse(SAMPLE)
    one("两枚好行", ([("S1",), ("S2",)], []),
        ([(x[0],) for x in good], bads))
    one("id 省略按行序给 S1", "S1", good[0][0])
    one("id 显式给 S2", "S2", good[1][0])

    _g, b = parse(['{"title": "只有标题"}'])
    one("缺键逐行点名", 1, len(b))
    _g, b = parse(["这不是 json"])
    one("非法 JSON 点名", 1, len(b))
    _g, b = parse(['{"title": "t", "url": "https://a/b", "asof": "2026/11/10"}'])
    one("日期不合形点名", 1, len(b))
    _g, b = parse(['{"title": "t", "url": "ftp://a/b", "asof": "2026-11-10"}'])
    one("url 非 http 点名", 1, len(b))
    _g, b = parse(['{"title": "t", "url": "https://a/b", "asof": "2026-11-10", "id": "X1"}'])
    one("id 形不合点名", 1, len(b))

    good, bads = parse(SAMPLE + ['{"title": "坏行"}'])
    one("好坏混合：好行照收", 2, len(good))
    one("好坏混合：坏行点名", 1, len(bads))

    body = outline(good)
    one("骨架含四节标题", True,
        all(k in body for k in ("## 1. 问询事项索引", "## 2. 要求提供的材料",
                                "## 3. 回复要点", "## 4. 回复文件")))
    one("骨架把清单排进回复文件节", True, "- 主体：示例科技 审核问询函回复公告｜[S1]" in body)
    one("骨架来源节三件齐", True,
        "- [S1] 示例科技 审核问询函回复公告 | https://example.com/r1 | 检索日 2026-11-10" in body)
    one("空清单不排主体行", False, "- 主体：" in outline([]))
    one("空清单点名全部未取到", True, "- 未取到：全部（清单为空）" in outline([]))

    print("----")
    print("自测形数=%d 不合=%d" % (forms, bad))
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="回复公告清单 → 问询函答复核对骨架（零网络）")
    ap.add_argument("listing", nargs="?", help="材料清单 JSONL")
    ap.add_argument("out", nargs="?", help="输出骨架 markdown")
    ap.add_argument("--selftest", action="store_true", help="跑内置夹具自检")
    a = ap.parse_args()

    mark_first_run()

    if a.selftest:
        return selftest()
    if not a.listing or not a.out:
        ap.print_usage(sys.stderr)
        print("用法错：缺输入清单或输出路径", file=sys.stderr)
        return 2

    try:
        rows = Path(a.listing).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        print("读不到输入：%s" % a.listing, file=sys.stderr)
        return 3

    good, bad = parse(rows)
    for i, why in bad:
        print("坏行 第 %d 行：%s（不采信）" % (i, why), file=sys.stderr)
    if not good:
        print("清单为空或全是坏行，不出空壳", file=sys.stderr)
        return 1

    Path(a.out).write_text(outline(good), encoding="utf-8")
    print("已写出骨架：%s（好行 %d，坏行 %d）" % (a.out, len(good), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
