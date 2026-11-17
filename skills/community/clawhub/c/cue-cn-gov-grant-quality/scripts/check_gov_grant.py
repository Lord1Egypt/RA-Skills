#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政府补助与利润依赖·逐条挂源 —— 五道机检（零网络、纯标准库、零凭据）。

用法：
    python3 scripts/check_gov_grant.py 你的政府补助稿.md
    python3 scripts/check_gov_grant.py --selftest     包内夹具自检
    python3 scripts/check_gov_grant.py --demo         打印一份完整合规样例（零输入可跑）
    python3 scripts/check_gov_grant.py --help

退码：0 全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿。

五道：
    GG-STRUCT  形制：头部四件自标、主体/报告期/数据口径三行、六节齐且有序、
               前四节各至少一条发现行
    GG-QUOTE   原句与锚：发现行以「」+〔锚…〕+[S#] 收尾（标 [待人工] 的行豁免），
               来源行齐编号+http(s) URL+检索日，正文引用的编号须已登记
    GG-NOSELF  不得自算：占利润比例须能在同一行原句里逐字找到；找不到的标〔自算〕
               并写明分子分母各出自哪句；「合计」行须挂原句，不自己加总
    GG-GAP     未取到两向点名：正文与第五节互校；零缺口须显式写「未取到：无」
    GG-LINE    红线：盈利质量断言、合规断言、评级目标价、可持续性预测零命中
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-gov-grant-quality"

CODES = ("GG-STRUCT", "GG-QUOTE", "GG-NOSELF", "GG-GAP", "GG-LINE")

SECTIONS = ("补助概况", "分项登记", "会计处理", "与利润的关系",
            "未取到与口径", "来源")

HEADER = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
SOURCE_HEAD = re.compile(r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL = re.compile(r"^https?://\S+$")
HEADING = re.compile(r"^(#{2,6})\s*(.*?)\s*$")
NUM_PREFIX = re.compile(r"^[一二三四五六七八九十]+、\s*")
GAP_TOKEN = re.compile(r"未取到\s*[:：]?\s*([^\s，。；,;｜|、〔」:：]+)")
GAP_EXCUSE = ("不适用", "无此项", "无需披露")
CALIBER = re.compile(r"^数据口径\s*[:：]\s*(?P<v>.+)$")

SELF_MARK = "〔自算〕"
# 比例：百分数。同一行原句里须能找到同一个数。
PCT = re.compile(r"(?P<v>\d+(?:\.\d+)?)\s*[%％]")
MOL_DEN = re.compile(
    r"分子\s*[=＝]\s*[^｜|]*\[S\d+\]\s*[｜|]\s*分母\s*[=＝]\s*[^｜|]*\[S\d+\]"
)
# 「合计」断言：出现合计/总计且该行没有原句 → 那是自己加的。
SUM_WORDS = ("合计", "总计", "合共")

REDLINE = re.compile(
    "严重依赖|依赖补助|靠补助|保壳|盈利质量差|盈利质量存疑|业绩全靠|"
    "骗补|补助依据不足|套取|违规取得|"
    "评级|目标价|买入|卖出|增持|减持|建议关注|"
    "预计明年|可持续性存疑|不可持续|将持续获得|仍可获得|"
    "将上涨|将下跌"
)
NEGATED_OK = re.compile(r"未发生|不存在|未取得|无此项")


# --------------------------------------------------------------------------- 埋点
def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    平台两个下载计数器都不可信（新 listing 首 48h 一次性播种 50~60），
    本地这枚文件是本件唯一能证明「真有人装上并跑过」的证据。
    解析参数成功后、干正事之前调用；任何失败静默跳过，绝不报错、绝不改进程退码。
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
        out.append("头部缺「数据口径：…」行（这一格是本件与利润表点评的分界）")
    elif not cal.startswith("政府补助"):
        out.append(f"数据口径须以「政府补助」起头，现为「{cal[:20]}」")

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
    out = []
    smap = by_section(sections)
    for n in SECTIONS[:4]:
        for ln in findings_of(smap.get(n, [])):
            if "[待人工]" in ln:
                continue
            has_self = SELF_MARK in ln
            if has_self:
                if not MOL_DEN.search(ln):
                    out.append(f"「{n}」标了〔自算〕却没写分子与分母各自出自哪句：{ln[:44]}")
                continue
            quoted = " ".join(m.group("q") for m in TRIPLE.finditer(ln))
            for m in PCT.finditer(outside_quotes(ln)):
                v = m.group("v")
                if v not in quoted:
                    out.append(f"「{n}」百分比 {v}% 不在同一行原句里，也未标〔自算〕：{ln[:44]}")
                    break
            # 合计断言：写了合计却该行没有任何原句 → 自己加的总数
            if any(w in outside_quotes(ln) for w in SUM_WORDS) and not TRIPLE.search(ln):
                out.append(f"「{n}」出现合计数却没有挂原句——那是自己加的：{ln[:44]}")
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
        "GG-STRUCT": check_struct(head, sections),
        "GG-QUOTE": check_quote(sections),
        "GG-NOSELF": check_noself(sections),
        "GG-GAP": check_gap(sections),
        "GG-LINE": check_line(sections),
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
报告期：2025 年度
数据口径：政府补助（附注逐项登记，不评盈利质量）

## 一、补助概况

- 本期计入损益的补助总额：「本期计入其他收益的政府补助合计 3,842.16 万元」〔锚：2025 年年度报告·附注七·政府补助·第 168 页〕[S1]
- 期末递延收益余额：「期末递延收益余额为 1,205.40 万元」〔锚：2025 年年度报告·附注七·递延收益·第 169 页〕[S2]
- 涉及项目数：「本期涉及政府补助项目共 12 项」〔锚：2025 年年度报告·附注七·政府补助·第 168 页〕[S1]

## 二、分项登记

- 补助项目一「智能装备产业化专项」：「智能装备产业化专项补助 1,800.00 万元」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]
- 补助项目二「研发费用后补助」：「研发费用后补助 960.00 万元」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]
- 补助项目三「稳岗补贴」：「稳岗补贴 182.16 万元」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]
- 其余项目：「另有 9 项政府补助，详见附注七·政府补助·明细表」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]

## 三、会计处理

- 计入科目：「与日常活动相关的政府补助计入其他收益；与日常活动无关的计入营业外收入」〔锚：附注七·政府补助·会计处理·第 168 页〕[S1]
- 递延处理：「与资产相关的政府补助确认为递延收益，在相关资产使用寿命内按合理、系统的方法分期计入损益」〔锚：附注七·政府补助·会计处理·第 168 页〕[S1]

## 四、与利润的关系

- 占利润总额比例：「政府补助占利润总额的比例为 38.42%」〔锚：2025 年年度报告·附注七·政府补助·第 168 页〕[S1]
- 可持续性：未取到：补助的可持续性说明 [待人工]

## 五、未取到与口径

- 未取到：补助的可持续性说明
- 口径：分项金额、合计与占利润比例均为照抄披露原文，未自行加总、未自行相除

## 六、来源

- [S1] 示例科技股份有限公司 2025 年年度报告·附注七 政府补助｜https://example.com/000001-2025-annual.pdf｜检索日 2026-11-09
- [S2] 示例科技股份有限公司 2025 年年度报告·附注七 递延收益｜https://example.com/000001-2025-annual.pdf｜检索日 2026-11-09
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

    case("缺节", _mutate(DEMO, "## 六、来源", "## 六、出处"), {"GG-STRUCT", "GG-QUOTE"}, 1)
    case("口径写错", _mutate(DEMO, "数据口径：政府补助", "数据口径：利润表点评"), {"GG-STRUCT"}, 1)
    case("空节", _mutate(DEMO, "- 计入科目：", "与日常活动相关的政府补助计入其他收益。"), {"GG-STRUCT"}, 1)

    case("原句为空", _mutate(DEMO, "「稳岗补贴 182.16 万元」", "「」"), {"GG-QUOTE"}, 1)
    case("来源缺检索日",
         _mutate(DEMO, "｜https://example.com/000001-2025-annual.pdf｜检索日 2026-11-09\n- [S2]",
                 "｜https://example.com/000001-2025-annual.pdf\n- [S2]"),
         {"GG-QUOTE"}, 1)
    case("引用未登记",
         _mutate(DEMO, "〔锚：附注七·政府补助·会计处理·第 168 页〕[S1]\n- 递延处理",
                 "〔锚：附注七·政府补助·会计处理·第 168 页〕[S9]\n- 递延处理"),
         {"GG-QUOTE"}, 1)

    case("比例自算充披露",
         _mutate(DEMO, "- 占利润总额比例：", "- 占利润总额比例：38.43%「政府补助占利润总额的比例为 38.42%」〔锚：附注七·政府补助·第 168 页〕[S1]"),
         {"GG-NOSELF"}, 1)
    # 一行没挂原句会同时撞两道：原句格（这行没有引文）与自算格（合计是自己加的）。
    # 两道都该发——这是设计，不是互相溅。
    case("合计自己加",
         _mutate(DEMO,
                 "- 其余项目：「另有 9 项政府补助，详见附注七·政府补助·明细表」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]",
                 "- 补助合计：2,942.16 万元"),
         {"GG-NOSELF", "GG-QUOTE"}, 1)
    case("自算缺分母",
         _mutate(DEMO, "- 其余项目：", "- 补助占比〔自算〕分子＝补助 3,842.16 万元 [S1]「另有 9 项政府补助」〔锚：附注七·明细表·第 168 页〕[S1]"),
         {"GG-NOSELF"}, 1)
    case("自算形状齐 → 不红（反证）",
         _mutate(DEMO, "- 其余项目：", "- 补助占比〔自算〕分子＝补助 3,842.16 万元 [S1]｜分母＝利润总额 10,000.00 万元 [S2]「另有 9 项政府补助」〔锚：附注七·明细表·第 168 页〕[S1]"),
         set(), 0)

    case("正文缺口未点名",
         _mutate(DEMO, "- 未取到：补助的可持续性说明\n", "- 未取到：无\n"), {"GG-GAP"}, 1)
    case("第五节多点了名",
         _mutate(DEMO, "- 未取到：补助的可持续性说明",
                 "- 未取到：补助的可持续性说明\n- 未取到：补助批文文号"),
         {"GG-GAP"}, 1)
    case("搪塞词",
         _mutate(DEMO, "- 未取到：补助的可持续性说明", "- 未取到：补助的可持续性说明（不适用）"),
         {"GG-GAP"}, 1)

    case("盈利质量断言",
         _mutate(DEMO, "- 口径：分项金额", "- 口径：公司利润严重依赖政府补助。分项金额"),
         {"GG-LINE"}, 1)
    case("合规断言",
         _mutate(DEMO, "- 口径：分项金额", "- 口径：该笔补助存在套取嫌疑。分项金额"),
         {"GG-LINE"}, 1)
    case("否定式不误伤（反证）",
         _mutate(DEMO, "「期末递延收益余额为 1,205.40 万元」",
                 "「期末递延收益余额为 1,205.40 万元，本期未发生补助退回」"),
         set(), 0)
    case("待人工豁免只到分句",
         _mutate(DEMO, "- 未取到：补助的可持续性说明",
                 "- 未取到：补助的可持续性说明 [待人工]，预计明年仍可获得"),
         {"GG-LINE"}, 1)

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
        description="政府补助与利润依赖·逐条挂源 —— 五道机检（零网络、零凭据）",
    )
    ap.add_argument("note", nargs="?", help="政府补助稿 markdown 路径")
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
        print("缺入参：给一份政府补助稿路径，或用 --demo / --selftest", file=sys.stderr)
        return 2
    try:
        text = Path(args.note).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"读不到文件：{args.note}（{exc}）", file=sys.stderr)
        return 3
    return run(text, args.note)


if __name__ == "__main__":
    sys.exit(main())
