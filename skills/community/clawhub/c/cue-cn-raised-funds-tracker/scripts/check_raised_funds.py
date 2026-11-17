#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""募集资金使用与募投进度·逐条挂源 —— 五道机检（零网络、纯标准库、零凭据）。

用法：
    python3 scripts/check_raised_funds.py 你的募集资金稿.md
    python3 scripts/check_raised_funds.py --selftest     包内夹具自检
    python3 scripts/check_raised_funds.py --demo         打印一份完整合规样例（零输入可跑）
    python3 scripts/check_raised_funds.py --help

退码：0 全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿。

五道：
    RF-STRUCT  形制：头部四件自标、主体/报告期/数据口径三行、六节齐且有序、
               前四节各至少一条发现行
    RF-QUOTE   原句与锚：发现行以「」+〔锚…〕+[S#] 收尾（标 [待人工] 的行豁免），
               来源行齐编号+http(s) URL+检索日，正文引用的编号须已登记
    RF-NOSELF  不得自算：进度百分比须能在同一行原句里逐字找到；找不到的标〔自算〕
               并写明分子分母各出自哪句
    RF-GAP     未取到两向点名：正文与第五节互校；零缺口须显式写「未取到：无」
    RF-LINE    红线与合计：合规/违规断言、项目好坏、评级目标价、后续进度预测零命中；
               专户余额与累计投入出现「合计/小计」一律发
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-raised-funds-tracker"

CODES = ("RF-STRUCT", "RF-QUOTE", "RF-NOSELF", "RF-GAP", "RF-LINE")

SECTIONS = ("募集概况", "专户余额", "投入进度", "变更与置换",
            "未取到与口径", "来源")

HEADER = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
# 同一行可以有盾牌式多段（承诺额/累计额/进度各挂一个），逐段收。
SEGMENT = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
SOURCE_HEAD = re.compile(r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL = re.compile(r"^https?://\S+$")
HEADING = re.compile(r"^(#{2,6})\s*(.*?)\s*$")
NUM_PREFIX = re.compile(r"^[一二三四五六七八九十]+、\s*")
GAP_TOKEN = re.compile(r"未取到\s*[:：]?\s*([^\s，。；,;｜|、〔」:：]+)")
GAP_EXCUSE = ("不适用", "无此项", "无需披露")
CALIBER = re.compile(r"^数据口径\s*[:：]\s*(?P<v>.+)$")

SELF_MARK = "〔自算〕"
# 进度百分比：同一行原句里必须能找到同一个数（容一个百分号写法差异）。
PCT = re.compile(r"(?P<v>\d+(?:\.\d+)?)\s*[%％]")
# 自算形状：分子＝… [S#]｜分母＝… [S#]
MOL_DEN = re.compile(
    r"分子\s*[=＝]\s*[^｜|]*\[S\d+\]\s*[｜|]\s*分母\s*[=＝]\s*[^｜|]*\[S\d+\]"
)

MERGE_WORDS = ("合计", "小计")
REDLINE = re.compile(
    "违规使用|违规占用|构成资金占用|已被挪用|挪用募集资金|"
    "合规性|是否合规|不存在问题|"
    "前景良好|前景广阔|产能消化存疑|项目可行|不值得投|"
    "评级|目标价|买入|卖出|增持|减持|建议关注|"
    "可达产|将按期完成|将上涨|将下跌"
)
# 「未发生变更」这类否定式声明不能误伤——它们是照抄披露的否定句。
NEGATED_OK = re.compile(r"未发生|不存在|无变更|未变更")


# --------------------------------------------------------------------------- 埋点
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


# --------------------------------------------------------------------------- 工具
def outside_quotes(text: str) -> str:
    return re.sub(r"「[^」]*」", "", text)


def sec_name(heading: str):
    t = NUM_PREFIX.sub("", heading.strip())
    for name in SECTIONS:
        if t == name:
            return name
        if t.startswith(name):
            nxt = t[len(name):len(name) + 1]
            if not nxt.isalnum():
                return name
    return None


def split_doc(text: str):
    lines = text.splitlines()
    first = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), None)
    head = lines if first is None else lines[:first]
    body = [] if first is None else lines[first:]
    out = []
    for ln in body:
        m = HEADING.match(ln)
        if m and len(m.group(1)) == 2:
            out.append([sec_name(m.group(2)), []])
            continue
        if out:
            out[-1][1].append(ln)
    return head, [(n, ls) for n, ls in out]


def findings_of(lines):
    return [ln.strip() for ln in lines if ln.strip().startswith("- ")]


def by_section(sections):
    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)
    return smap


# --------------------------------------------------------------------------- 判据
def check_struct(head, sections):
    out = []
    head_text = "\n".join(head)
    for label in HEADER:
        if label not in head_text:
            out.append(f"头部四件自标缺「{label}」（须写在第一个 ## 之前）")
    for key in ("主体", "报告期"):
        if not re.search(rf"^{key}\s*[:：]\s*\S", head_text, re.M):
            out.append(f"头部缺「{key}：…」行")

    cal = None
    for ln in head:
        m = CALIBER.match(ln.strip())
        if m:
            cal = m.group("v").strip()
    if cal is None:
        out.append("头部缺「数据口径：…」行（这一格是本件与发行条款件的分界）")
    elif not cal.startswith("募集资金"):
        out.append(f"数据口径须以「募集资金」起头，现为「{cal[:20]}」")

    names = [n for n, _ in sections]
    missing = [s for s in SECTIONS if s not in names]
    if missing:
        out.append("缺节：" + "、".join(missing))
    seen = [n for n in names if n in SECTIONS]
    if seen != [n for n in SECTIONS if n in seen]:
        out.append("节序不对：现序 " + "→".join(seen))

    smap = by_section(sections)
    for n in SECTIONS[:4]:
        if not findings_of(smap.get(n, [])):
            out.append(f"「{n}」节没有发现行（空节等于把这一节藏起来）")
        for ln in smap.get(n, []):
            s = ln.strip()
            if s and not s.startswith("- "):
                out.append(f"「{n}」节内有非发现行：{s[:36]}")
    return out


def check_quote(sections):
    out = []
    smap = by_section(sections)
    cited = set()
    for n in SECTIONS[:4]:
        for ln in findings_of(smap.get(n, [])):
            if "[待人工]" in ln:
                continue
            if not TRIPLE.search(ln):
                out.append(f"「{n}」发现行缺「」原句或〔锚…〕或[S#]：{ln[:44]}")
                continue
            for m in TRIPLE.finditer(ln):
                if not m.group("q").strip():
                    out.append(f"「{n}」原句为空：{ln[:44]}")
                if not m.group("a").strip():
                    out.append(f"「{n}」锚为空：{ln[:44]}")
                cited.add(m.group("s"))

    registered = {}
    for ln in findings_of(smap.get("来源", [])):
        m = SOURCE_HEAD.match(ln)
        if not m:
            out.append(f"来源行形制不对（须「- [S#] 标题｜URL｜检索日 YYYY-MM-DD」）：{ln[:44]}")
            continue
        sid = m.group("s")
        parts = [p.strip() for p in re.split(r"[｜|]", m.group("rest"))]
        if sid in registered:
            out.append(f"来源编号重复登记：{sid}")
        url = next((p for p in parts if URL.match(p)), None)
        day = None
        for p in parts:
            p2 = re.sub(r"^检索日\s*[:：]?\s*", "", p)
            if DATE.match(p2):
                day = p2
                break
        if not url:
            out.append(f"来源行 {sid} 缺可点 http(s) URL")
        if not day:
            out.append(f"来源行 {sid} 缺检索日 YYYY-MM-DD")
        registered[sid] = bool(url and day)

    if not findings_of(smap.get("来源", [])):
        out.append("「来源」节为空（没有来源就没有原句可回查）")

    for s in sorted(cited):
        if s not in registered:
            out.append(f"正文引用的 [{s}] 未在来源节登记")
    return out


def check_noself(sections):
    """进度百分比不改写口径：披露写了就同一行能找到，没写就必须走〔自算〕形状。"""
    out = []
    smap = by_section(sections)
    for n in ("投入进度", "变更与置换"):
        for ln in findings_of(smap.get(n, [])):
            if "[待人工]" in ln:
                continue
            has_self = SELF_MARK in ln
            if has_self:
                if not MOL_DEN.search(ln):
                    out.append(f"「{n}」标了〔自算〕却没写分子与分母各自出自哪句：{ln[:44]}")
                continue
            # 没有〔自算〕：每个百分比都必须在同一行的某条原句里逐字出现
            quoted = " ".join(m.group("q") for m in SEGMENT.finditer(ln))
            for m in PCT.finditer(outside_quotes(ln)):
                v = m.group("v")
                if v not in quoted:
                    out.append(
                        f"「{n}」百分比 {v}% 不在同一行原句里，也未标〔自算〕：{ln[:44]}")
                    break
    return out


def check_gap(sections):
    out = []
    smap = by_section(sections)
    body_text = "\n".join(ln for n in SECTIONS[:4] for ln in smap.get(n, []))
    tail_text = "\n".join(smap.get("未取到与口径", []))

    body = set(GAP_TOKEN.findall(body_text))
    tail = set(GAP_TOKEN.findall(tail_text))

    for name in GAP_EXCUSE:
        if name in body_text or name in tail_text:
            out.append(f"出现「{name}」——那是把没查当成没有；没取到就写未取到")

    if not tail and not body:
        out.append("零缺口须显式写「- 未取到：无」")
        return out

    for x in sorted(body - tail):
        out.append(f"正文写了未取到「{x}」，第五节没点名")
    for x in sorted(tail - body):
        out.append(f"第五节点名了「{x}」，正文没有对应表述")
    return out


def check_line(sections):
    out = []
    smap = by_section(sections)
    for n in ("专户余额", "投入进度"):
        for ln in findings_of(smap.get(n, [])):
            for w in MERGE_WORDS:
                if w in outside_quotes(ln):
                    out.append(f"「{n}」出现「{w}」——专户与项目不许合成一个总数：{ln[:36]}")
                    break

    for n in SECTIONS[:5]:
        for ln in smap.get(n, []):
            for clause in re.split(r"[；;。，,｜|]", outside_quotes(ln)):
                hit = REDLINE.search(clause)
                if not hit:
                    continue
                if NEGATED_OK.search(clause):
                    continue
                if "[待人工]" in clause:
                    continue
                out.append(f"「{n}」红线命中「{hit.group(0)}」：{clause.strip()[:40]}")
    return out


def analyze(text: str):
    head, sections = split_doc(text)
    return {
        "RF-STRUCT": check_struct(head, sections),
        "RF-QUOTE": check_quote(sections),
        "RF-NOSELF": check_noself(sections),
        "RF-GAP": check_gap(sections),
        "RF-LINE": check_line(sections),
    }


def run(text: str, label: str = "<稿>") -> int:
    if not text.strip():
        print(f"读不到内容（空稿）：{label}", file=sys.stderr)
        return 3
    found = analyze(text)
    total = sum(len(v) for v in found.values())
    for code in CODES:
        for msg in found[code]:
            print(f"{code} {msg}")
    print("----")
    print(f"{label} 发条={total}｜" + "｜".join(f"{c}={len(found[c])}" for c in CODES))
    return 0 if total == 0 else 1


# --------------------------------------------------------------------------- 样例
DEMO = """\
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：示例科技股份有限公司
报告期：2025-06-30
数据口径：募集资金存放与实际使用情况（存续期台账）

## 一、募集概况

- 募集方式：「向特定对象发行股票」〔锚：2025 年半年度募集资金存放与实际使用情况的专项报告·第 1 页〕[S1]
- 募集资金总额：「募集资金总额为人民币 108,000.00 万元」〔锚：专项报告·第 1 页·募集资金基本情况〕[S1]
- 募集资金净额：「扣除发行费用后，募集资金净额为人民币 105,420.00 万元」〔锚：专项报告·第 1 页·募集资金基本情况〕[S1]
- 到账日：「募集资金已于 2024 年 3 月 12 日全部到位」〔锚：专项报告·第 1 页·募集资金基本情况〕[S1]

## 二、专户余额

- 专户一（招商银行深圳分行·末四位 8821）：「余额为人民币 21,340.55 万元」〔锚：专项报告·第 3 页·募集资金专户存储情况〕[S1]
- 专户二（中国银行深圳分行·末四位 4477）：「余额为人民币 8,120.30 万元」〔锚：专项报告·第 3 页·募集资金专户存储情况〕[S1]

## 三、投入进度

- 募投项目一「智能制造产线建设项目」：「承诺投入募集资金 45,000.00 万元，截至 2025 年 6 月 30 日累计投入 28,057.50 万元，投入进度 62.35%」〔锚：专项报告·第 4 页·募集资金投资项目进度表〕[S2]
- 募投项目二「研发中心建设项目」：「承诺投入募集资金 32,000.00 万元，截至 2025 年 6 月 30 日累计投入 12,800.00 万元，投入进度 40.00%」〔锚：专项报告·第 4 页·募集资金投资项目进度表〕[S2]

## 四、变更与置换

- 变更情况：「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]
- 置换先期投入：「公司以募集资金置换预先投入自筹资金 6,430.00 万元」〔锚：专项报告·第 5 页·置换先期投入情况〕[S2]
- 补充流动资金：「使用闲置募集资金暂时补充流动资金 10,000.00 万元，已于 2025 年 5 月 20 日全部归还」〔锚：专项报告·第 6 页·闲置募集资金使用情况〕[S3]
- 结项节余：未取到：结项节余 [待人工]

## 五、未取到与口径

- 未取到：结项节余
- 口径：募集概况、专户余额、投入进度与变更事项均为照抄披露原文，进度百分比为披露值，未自行计算

## 六、来源

- [S1] 示例科技股份有限公司 2025 年半年度募集资金存放与实际使用情况的专项报告｜https://example.com/000001-2025h1-raised-funds.pdf｜检索日 2026-11-09
- [S2] 同上·募集资金投资项目进度表与变更情况节｜https://example.com/000001-2025h1-raised-funds.pdf｜检索日 2026-11-09
- [S3] 示例科技股份有限公司关于归还暂时补充流动资金的募集资金的公告｜https://example.com/000001-2025-repay.pdf｜检索日 2026-11-09
"""


# --------------------------------------------------------------------------- 自测
def _mutate(text: str, old: str, new: str) -> str:
    assert old in text, f"夹具替换目标不在样例里：{old[:40]}"
    return text.replace(old, new, 1)


def selftest() -> int:
    cases = []

    def case(name, text, want_codes, want_rc):
        cases.append((name, text, set(want_codes), want_rc))

    case("好样零发条", DEMO, set(), 0)

    case("缺节", _mutate(DEMO, "## 六、来源", "## 六、出处"), {"RF-STRUCT", "RF-QUOTE"}, 1)
    case("口径写错", _mutate(DEMO, "数据口径：募集资金", "数据口径：定增条款"), {"RF-STRUCT"}, 1)
    case("空节", _mutate(DEMO, "- 变更情况：", "本报告期内募投项目未发生变更。"), {"RF-STRUCT"}, 1)

    case("原句为空", _mutate(DEMO, "「向特定对象发行股票」", "「」"), {"RF-QUOTE"}, 1)
    case("来源缺 URL",
         _mutate(DEMO, "｜https://example.com/000001-2025-repay.pdf", ""), {"RF-QUOTE"}, 1)
    case("引用未登记",
         _mutate(DEMO, "〔锚：专项报告·第 6 页·闲置募集资金使用情况〕[S3]",
                 "〔锚：专项报告·第 6 页·闲置募集资金使用情况〕[S9]"),
         {"RF-QUOTE"}, 1)

    # 自算格的三条夹具都动**引号外**的文字：这一格判的是「卡面自己写了个数、原句里没有」。
    # 改引号内（把原句的数换个值）判不到——那属于抄错原文，不是自算。
    case("进度自算充披露",
         _mutate(DEMO, "- 募投项目一「智能制造产线建设项目」：",
                 "- 募投项目一「智能制造产线建设项目」投入进度 62.36%："),
         {"RF-NOSELF"}, 1)
    case("自算缺分母",
         _mutate(DEMO, "- 变更情况：「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]",
                 "- 变更情况：进度合计〔自算〕分子＝累计投入 12,800.00 万元 [S1]「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]"),
         {"RF-NOSELF"}, 1)
    case("自算形状齐 → 不红（反证）",
         _mutate(DEMO, "- 变更情况：「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]",
                 "- 变更情况：投资完成度〔自算〕分子＝累计投入 12,800.00 万元 [S1]｜分母＝承诺投入 32,000.00 万元 [S2]「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]"),
         set(), 0)

    case("正文缺口未点名",
         _mutate(DEMO, "- 未取到：结项节余\n", "- 未取到：无\n"), {"RF-GAP"}, 1)
    case("第五节多点了名",
         _mutate(DEMO, "- 未取到：结项节余", "- 未取到：结项节余\n- 未取到：会计师鉴证意见"),
         {"RF-GAP"}, 1)
    case("搪塞词",
         _mutate(DEMO, "- 未取到：结项节余", "- 未取到：结项节余（不适用）"), {"RF-GAP"}, 1)

    case("违规断言",
         _mutate(DEMO, "- 变更情况：", "- 变更情况：公司存在违规使用募集资金情形。"), {"RF-LINE"}, 1)
    case("合计行",
         _mutate(DEMO, "- 专户二（中国银行深圳分行·末四位 4477）",
                 "- 专户合计：「余额合计 29,460.85 万元」"), {"RF-LINE"}, 1)
    case("否定式不误伤（反证）",
         _mutate(DEMO, "「本报告期内募投项目未发生变更」",
                 "「本报告期内募投项目未发生变更，不存在违规使用情形」"),
         set(), 0)
    case("待人工豁免只到分句",
         _mutate(DEMO, "未取到：结项节余 [待人工]",
                 "未取到：结项节余 [待人工]，预计年内可达产"),
         {"RF-LINE"}, 1)

    bad = 0
    for name, text, want_codes, want_rc in cases:
        found = analyze(text)
        got_codes = {c for c in CODES if found[c]}
        got_rc = 0 if sum(len(v) for v in found.values()) == 0 else 1
        if got_codes != want_codes or got_rc != want_rc:
            bad += 1
            print(f"不合 {name}：期望 {sorted(want_codes) or '∅'}/rc={want_rc}，"
                  f"实得 {sorted(got_codes) or '∅'}/rc={got_rc}")
            for c in sorted(got_codes):
                for m in found[c][:2]:
                    print(f"     {c} {m[:70]}")
        else:
            print(f"过   {name}")

    empty_rc = run("", "<空稿>")
    if empty_rc != 3:
        bad += 1
        print(f"不合 空稿：rc={empty_rc} 应 3")
    else:
        print("过   空稿 rc=3")

    print("----")
    print(f"自测 夹具={len(cases) + 1} 不合={bad}")
    return 0 if bad == 0 else 1


# --------------------------------------------------------------------------- 入口
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        add_help=True,
        description="募集资金使用与募投进度·逐条挂源 —— 五道机检（零网络、零凭据）",
    )
    ap.add_argument("note", nargs="?", help="募集资金稿 markdown 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    args = ap.parse_args(argv)

    mark_first_run()                                     # ← 解析成功之后、干正事之前

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.note:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份募集资金稿路径，或用 --demo / --selftest", file=sys.stderr)
        return 2
    try:
        text = Path(args.note).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"读不到文件：{args.note}（{exc}）", file=sys.stderr)
        return 3
    return run(text, args.note)


if __name__ == "__main__":
    sys.exit(main())
