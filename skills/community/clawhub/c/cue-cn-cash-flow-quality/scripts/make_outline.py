#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 把材料清单排成现金流稿骨架（零网络、零计费、不读凭据、不依赖任何通道产物）

输入：一份材料清单 JSONL，一行一份材料，必需三键：
    {"title": "示例科技 2025 年年度报告", "url": "https://example.com/a", "asof": "2026-11-09"}
    `id` 可省，省略时按行序给 S1／S2／…
输出：一份六节骨架 .md。六节都在，每节留「未取到（骨架）」占位，来源节按清单落位。
      **骨架跑机检必然红在占位行上，这是设计**：提醒你补完再交，不让空壳冒充成品。

零通道路径是默认路径：本脚本只读你给的那份 JSONL，不需要 parsed-doc，也不需要凭据。

用法：
    python3 scripts/make_outline.py 清单.jsonl 骨架.md
    python3 scripts/make_outline.py 清单.jsonl          # 打到 stdout
    python3 scripts/make_outline.py --selftest

退码：0 排出骨架 / 1 输入有坏行（逐行点名，不采信坏行）或清单为空 / 2 用法错 / 3 读不到输入。
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-cash-flow-quality"

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED = ("title", "url", "asof")

BODY_SECTIONS = (
    ("经营活动现金流", "经营活动现金流量净额与它的主要构成（销售收现、购买商品付现、支付给职工的现金、支付的各项税费）"),
    ("投资活动现金流", "投资活动现金流量净额与购建固定资产等长期资产支付的现金"),
    ("筹资活动现金流", "筹资活动现金流量净额与取得借款、偿还债务、分配股利利润或偿付利息支付的现金"),
    ("净现比与收现比", "净现比、收现比、自由现金流；原句没有就标〔自算〕并写明分子分母各出自哪句"),
    ("净利润调节表", "间接法调节表逐项照抄，不合并、不取绝对值"),
)

HEAD = """# %(title)s

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：%(subject)s
报告期：%(period)s

> 本文件是 `make_outline.py` 排出的**骨架**。六节都在，但每节的数字位是「未取到（骨架）」占位。
> 骨架故意过不了 `check_cash_flow.py`——把占位行换成带「」原句＋〔锚〕＋[S#] 的事实行，它才该变绿。

"""


def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    平台两个下载计数器都不可信（新 listing 首 48h 一次性播种 50~60），
    本地这枚文件是本件唯一能证明「真有人装上并跑过」的证据。
    解析参数成功后、干正事之前调用；任何失败静默跳过，绝不报错、不改进程退码。
    """
    try:
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001
        pass


def _valid_date(s):
    if not isinstance(s, str) or not ISO.match(s):
        return False
    try:
        date.fromisoformat(s)
    except ValueError:
        return False
    return True


def load_rows(lines):
    """→ (rows, problems)。坏行逐行点名，不静默跳行。"""
    rows, problems = [], []
    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError as exc:
            problems.append((i, "不是合法 JSON（%s）" % str(exc)[:60]))
            continue
        if not isinstance(obj, dict):
            problems.append((i, "不是 JSON 对象"))
            continue
        missing = [k for k in REQUIRED if not obj.get(k)]
        if missing:
            problems.append((i, "缺键 %s" % "、".join(missing)))
            continue
        if not _valid_date(obj["asof"]):
            problems.append((i, "asof 不是 YYYY-MM-DD 日期：%r" % obj["asof"]))
            continue
        if not str(obj["url"]).startswith(("http://", "https://")):
            problems.append((i, "url 不是 http(s) 地址：%r" % obj["url"]))
            continue
        sid = obj.get("id") or "S%d" % (len(rows) + 1)
        rows.append({"id": str(sid), "title": str(obj["title"]).strip(),
                     "url": str(obj["url"]).strip(), "asof": obj["asof"]})
    return rows, problems


def build(rows, subject="待填主体", period="待填报告期"):
    src = "\n".join(
        "- [%s] %s | %s | 检索日 %s | 类型：待填" % (r["id"], r["title"], r["url"], r["asof"])
        for r in rows)
    out = [HEAD % {"title": subject, "subject": subject, "period": period}]
    for name, hint in BODY_SECTIONS:
        out.append("## %s\n\n" % name)
        out.append("- 未取到（骨架）：%s。请回原文补，行末挂「」原句＋〔锚〕＋[S#]。\n\n" % hint)
    out.append("## 口径与未取到\n\n")
    out.append("- 未取到：本骨架全部数字位均未回原文核对，逐条补完后把这一行改成「未取到：无」或逐条点名。\n")
    out.append("- 口径：比率原句没写的一律标〔自算〕并写明分子分母各出自哪句。\n")
    out.append("- 口径：期末现金及现金等价物余额与资产负债表货币资金不是一个数，不互相印证当作相等。\n\n")
    out.append("## 来源\n\n%s\n" % src)
    return "".join(out)


def selftest():
    import io
    cases = []
    # 单行合法 → 出骨架，六节齐、来源行在场
    rows, probs = load_rows(['{"title":"A","url":"https://e.com/a","asof":"2026-11-09"}'])
    txt = build(rows, "A", "2025A")
    cases.append(("单行合法", len(rows) == 1 and not probs
                  and all(("## " + n) in txt for n, _h in BODY_SECTIONS)
                  and "## 来源" in txt and "[S1] A | https://e.com/a" in txt, ""))
    # 非法 JSON
    rows, probs = load_rows(['{bad json'])
    cases.append(("非法 JSON 逐行点名", not rows and len(probs) == 1, ""))
    # 缺键
    rows, probs = load_rows(['{"title":"A","url":"https://e.com/a"}'])
    cases.append(("缺 asof 点名", not rows and len(probs) == 1 and "asof" in probs[0][1], ""))
    # 日期不合形
    rows, probs = load_rows(['{"title":"A","url":"https://e.com/a","asof":"2026/11/09"}'])
    cases.append(("asof 不合形点名", not rows and len(probs) == 1, ""))
    # url 不是 http
    rows, probs = load_rows(['{"title":"A","url":"见年报","asof":"2026-11-09"}'])
    cases.append(("url 非 http 点名", not rows and len(probs) == 1, ""))
    # 好行与坏行混排：好行照收，坏行点名
    rows, probs = load_rows([
        '{"title":"A","url":"https://e.com/a","asof":"2026-11-09"}',
        '{bad',
        '{"title":"B","url":"https://e.com/b","asof":"2026-11-09"}'])
    cases.append(("好坏混排：收 2 点 1 名", len(rows) == 2 and len(probs) == 1, ""))
    # 空清单
    rows, probs = load_rows([])
    cases.append(("空清单", not rows and not probs, ""))

    bad = 0
    for label, cond, _ in cases:
        if cond:
            print("过   %s" % label)
        else:
            bad += 1
            print("不合 %s" % label)
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=0" % (len(cases), bad))
    return 0 if bad == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="把材料清单排成现金流稿骨架（零网络）")
    ap.add_argument("listing", nargs="?", help="材料清单 JSONL")
    ap.add_argument("out", nargs="?", help="输出 .md；省略则打到 stdout")
    ap.add_argument("--subject", default="待填主体", help="主体（股票代码或公司全称）")
    ap.add_argument("--period", default="待填报告期", help="报告期，如 2025 年年度报告")
    ap.add_argument("--selftest", action="store_true", help="跑内置夹具自检")
    args = ap.parse_args(argv)

    mark_first_run()                                     # ← 解析成功之后、干正事之前

    if args.selftest:
        return selftest()
    if not args.listing:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份材料清单 JSONL，或用 --selftest", file=sys.stderr)
        return 2
    try:
        with open(args.listing, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except (IOError, OSError) as exc:
        print("读不到输入：%s（%s）" % (args.listing, exc))
        return 3

    rows, problems = load_rows(lines)
    for lineno, why in problems:
        print("未采信 第 %d 行：%s" % (lineno, why), file=sys.stderr)

    if not rows:
        print("清单里没有一行可用材料——不出空壳（空清单退 1）", file=sys.stderr)
        return 1
    if problems:
        print("清单有 %d 行坏行已点名未采信；可用 %d 行。" % (len(problems), len(rows)),
              file=sys.stderr)

    text = build(rows, args.subject, args.period)
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text)
        except (IOError, OSError) as exc:
            print("写不到输出：%s（%s）" % (args.out, exc), file=sys.stderr)
            return 3
        print("已排出骨架：%s（%d 份材料）" % (args.out, len(rows)), file=sys.stderr)
    else:
        sys.stdout.write(text)

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
