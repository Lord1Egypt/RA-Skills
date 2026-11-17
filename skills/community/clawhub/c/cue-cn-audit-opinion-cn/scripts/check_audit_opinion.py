#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计意见与非标事项·逐条挂源 —— 五道机检（零网络、纯标准库、零凭据）。

用法：
    python3 scripts/check_audit_opinion.py 你的审计稿.md
    python3 scripts/check_audit_opinion.py --selftest     包内夹具自检
    python3 scripts/check_audit_opinion.py --demo         打印一份完整合规样例（零输入可跑）
    python3 scripts/check_audit_opinion.py --help

退码：0 全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿。

五道：
    AU-STRUCT   形制：头部四件自标、主体/报告期/数据口径三行、六节齐且有序、
                前四节各至少一条发现行、意见类型行恰一行
    AU-QUOTE    原句与锚：发现行以「」+〔锚…〕+[S#] 收尾（标 [待人工] 的行豁免），
                来源行齐编号+http(s) URL+检索日，正文引用的编号须已登记
    AU-OPINION  意见类型：只认在册六种写法；引号内出现的类型名必须与声明一致；
                引号外把「非标」当结论用一律发
    AU-GAP      未取到两向点名：正文与第五节互校；零缺口须显式写「未取到：无」
    AU-LINE     红线：造假/舞弊/暴雷/退市/评级目标价/买卖建议/下一年度预测零命中

判据边界（写明防误读）：本机检判**形制与在册写法**，判不了「分类对不对」——
报告实际是保留意见而卡面写成标准无保留，机检看不出来。那一步必须人回原文核。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-audit-opinion-cn"

CODES = ("AU-STRUCT", "AU-QUOTE", "AU-OPINION", "AU-GAP", "AU-LINE")

SECTIONS = ("审计意见", "形成意见的基础", "关键审计事项",
            "其他信息与持续经营", "未取到与口径", "来源")

HEADER = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

# 在册六种。按长度降序取用：先认长的，免得「带强调事项段的无保留意见」被
# 里面的「无保留意见」抢先认掉，再被当成另一个类型。
TYPES = (
    "带持续经营重大不确定性段落的无保留意见",
    "带强调事项段的无保留意见",
    "标准无保留意见",
    "无法表示意见",
    "保留意见",
    "否定意见",
)
TYPES_BY_LEN = tuple(sorted(TYPES, key=len, reverse=True))

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE_SPAN = re.compile(r"「[^」]*」")
SOURCE_HEAD = re.compile(r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL = re.compile(r"^https?://\S+$")
HEADING = re.compile(r"^(#{2,6})\s*(.*?)\s*$")
NUM_PREFIX = re.compile(r"^[一二三四五六七八九十]+、\s*")
# 冒号也排进禁字集：否则「- 未取到：」这种留空的骨架行会让正则回溯，
# 把冒号本身当成缺口名（实测过一次，报出「第五节点名了「：」」这种看不懂的条）。
GAP_TOKEN = re.compile(r"未取到\s*[:：]?\s*([^\s，。；,;｜|、〔」:：]+)")
GAP_EXCUSE = ("不适用", "无此项", "无需披露")
OPINION_LINE = re.compile(r"^-\s*意见类型\s*[:：]\s*(?P<t>[^｜|「]+?)\s*[｜|]")
REDLINE = re.compile(
    "造假|舞弊|暴雷|资金链断裂|退市|评级|目标价|买入|卖出|增持|减持|"
    "建议关注|将上涨|将下跌|有望走强|下一年度|重大风险"
)
CALIBER = re.compile(r"^数据口径\s*[:：]\s*(?P<v>.+)$")


# --------------------------------------------------------------------------- 埋点
def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    为什么要有这个：平台两个下载计数器都不可信（新 listing 首 48h 会一次性播种
    50~60 的初始计数，那不是用户下载）。本地这枚文件是本件唯一能证明
    「真有人装上并跑过」的证据。

    规矩：解析参数成功之后、干正事之前调用；**任何失败都静默跳过**，
    绝不报错、绝不改退码、绝不影响主流程（家目录只读、配额满、无 HOME 都算正常情况）。
    """
    try:
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001 —— 埋点永不阻业务
        pass


# --------------------------------------------------------------------------- 工具
def outside_quotes(text: str) -> str:
    """去掉「」引文，只留卡面自己的话。红线与类型一致性都只判这一侧。"""
    return QUOTE_SPAN.sub("", text)


def sec_name(heading: str):
    t = NUM_PREFIX.sub("", heading.strip())
    for name in SECTIONS:
        if t == name:
            return name
        if t.startswith(name):
            nxt = t[len(name):len(name) + 1]
            if not (nxt.isalnum()):
                return name
    return None


def split_doc(text: str):
    """→ (head_lines, [(section_name, [lines]), ...])"""
    lines = text.splitlines()
    first = None
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            first = i
            break
    head = lines if first is None else lines[:first]
    body = [] if first is None else lines[first:]
    out, cur = [], None
    for ln in body:
        m = HEADING.match(ln)
        if m and len(m.group(1)) == 2:
            cur = sec_name(m.group(2))
            out.append([cur, []])
            continue
        if out:
            out[-1][1].append(ln)
        # 二级标题之前的散行（第一个 ## 之后理论上不会有）
    return head, [(n, ls) for n, ls in out]


def findings_of(lines):
    return [ln.strip() for ln in lines if ln.strip().startswith("- ")]


def registered_types(text: str):
    """按长度降序认类型名，认到就蒙掉，避免长短名互相吃掉。

    返回 [(类型名, 出现位置短语)]，位置短语为 'quote' 或 'plain'。
    """
    hits = []
    work = text
    for name in TYPES_BY_LEN:
        while name in work:
            i = work.index(name)
            # 判断这次命中落在引号内还是引号外
            before = work[:i]
            inside = before.count("「") > before.count("」")
            hits.append((name, "quote" if inside else "plain"))
            work = work[:i] + "　" * len(name) + work[i + len(name):]
    return hits


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
        out.append("头部缺「数据口径：…」行（这一格是本件与财报点评的分界）")
    elif not cal.startswith("审计报告"):
        out.append(f"数据口径须以「审计报告」起头，现为「{cal[:20]}」")

    names = [n for n, _ in sections]
    missing = [s for s in SECTIONS if s not in names]
    if missing:
        out.append("缺节：" + "、".join(missing))
    seen = [n for n in names if n in SECTIONS]
    if seen != [n for n in SECTIONS if n in seen]:
        out.append("节序不对：现序 " + "→".join(seen))

    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)

    for n in SECTIONS[:4]:
        got = findings_of(smap.get(n, []))
        if not got:
            out.append(f"「{n}」节没有发现行（空节等于把这一节藏起来）")

    for n in SECTIONS[:4]:
        for ln in smap.get(n, []):
            s = ln.strip()
            if s and not s.startswith("- "):
                out.append(f"「{n}」节内有非发现行：{s[:36]}")

    op = [ln for ln in findings_of(smap.get("审计意见", [])) if OPINION_LINE.match(ln)]
    if not op:
        out.append("「审计意见」节缺「- 意见类型：<在册类型>｜「原句」〔锚…〕[S#]」行")
    elif len(op) > 1:
        out.append(f"「审计意见」节意见类型行有 {len(op)} 条（应恰 1 条）")
    return out


def check_quote(sections):
    out = []
    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)

    # 只判前四节：第五节「未取到与口径」里的行本来就没有原句可挂（缺的就是那份材料），
    # 第六节「来源」自有一套登记形制。把它们塞进这一格会把设计判成缺陷。
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
        parts = [p.strip() for p in re.split(r"[｜|]", m.group("rest"))]
        sid = m.group("s")
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
    # 只判单向（引用了却未登记）。反过来的「登记了没引用」不判：那既可能是垫来源，
    # 也可能是某节结构改坏后引文被挪走——后者会由形制那一格点名，不必让两格互相溅。
    return out


def check_opinion(text, sections):
    out = []
    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)

    op = [ln for ln in findings_of(smap.get("审计意见", [])) if OPINION_LINE.match(ln)]
    declared = None
    if op:
        declared = OPINION_LINE.match(op[0]).group("t").strip()
        name_hits = registered_types(declared)
        if declared not in TYPES:
            out.append(f"意见类型「{declared}」不在册（只认六种：{'／'.join(TYPES)}）")
        elif len(name_hits) != 1 or name_hits[0][0] != declared:
            out.append(f"意见类型「{declared}」写法有歧义（须整串等于在册名之一）")

    # 「非标」只判卡面自己的话，且只判正文各节：头部「数据口径：审计报告（审计意见与非标事项…）」
    # 是这个件的题名，不是对某份报告下的结论。判据收在「非标」后面不是「事项」——
    # 「非标事项」是话题词，「非标意见」「属于非标」才是伞形归类。
    plain = outside_quotes("\n".join(
        ln for n in SECTIONS[:5] for ln in smap.get(n, [])))
    if re.search(r"非标(?:准)?(?!事项)", plain):
        out.append("引号外把「非标」当结论用——那是卡面自己的归纳，不是报告的原话")

    if declared in TYPES:
        for name, where in registered_types(text):
            if where == "plain" and name != declared:
                out.append(f"引号外出现与声明不一致的类型名「{name}」（声明为「{declared}」）")
                break
    return out


def check_gap(sections):
    out = []
    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)

    body_text = "\n".join(
        ln for n in SECTIONS[:4] for ln in smap.get(n, [])
    )
    tail_text = "\n".join(smap.get("未取到与口径", []))

    body = set(GAP_TOKEN.findall(body_text))
    tail = set(GAP_TOKEN.findall(tail_text))

    for name in ("不适用", "无此项", "无需披露"):
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


def check_line(text, sections):
    out = []
    smap = {}
    for n, ls in sections:
        if n in SECTIONS:
            smap.setdefault(n, [])
            smap[n].extend(ls)

    for n in SECTIONS[:5]:
        for ln in smap.get(n, []):
            for clause in re.split(r"[；;。，,｜|]", outside_quotes(ln)):
                hit = REDLINE.search(clause)
                if hit and "[待人工]" not in clause:
                    out.append(f"「{n}」红线命中「{hit.group(0)}」：{clause.strip()[:40]}")
    return out


def analyze(text: str):
    head, sections = split_doc(text)
    found = {
        "AU-STRUCT": check_struct(head, sections),
        "AU-QUOTE": check_quote(sections),
        "AU-OPINION": check_opinion(text, sections),
        "AU-GAP": check_gap(sections),
        "AU-LINE": check_line(text, sections),
    }
    return found


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
数据口径：审计报告（审计意见与非标事项逐项登记）

## 一、审计意见

- 意见类型：标准无保留意见｜「我们认为，后附的财务报表在所有重大方面按照企业会计准则的规定编制，公允反映了示例科技股份有限公司 2025 年 12 月 31 日的合并及母公司财务状况以及 2025 年度的合并及母公司经营成果和现金流量。」〔锚：2025 年年度报告·第 112 页·审计报告·审计意见段〕[S1]

## 二、形成意见的基础

- 意见基础：本报告未单列「形成意见的基础」一节，意见段后直接进入关键审计事项 [待人工]

## 三、关键审计事项

- 关键审计事项（一）：「收入确认」〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S1]
- 应对程序（一）：「我们了解、评估了管理层对收入确认相关的内部控制的设计，并测试了关键控制运行的有效性。」〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S1]
- 关键审计事项（二）：「应收账款减值」〔锚：2025 年年度报告·第 116 页·关键审计事项段〕[S1]
- 应对程序（二）：「我们复核了管理层预期信用损失的测算过程，并检查了期后回款情况。」〔锚：2025 年年度报告·第 116 页·关键审计事项段〕[S1]

## 四、其他信息与持续经营

- 强调事项段：审计报告未单列强调事项段 [待人工]
- 持续经营重大不确定性段落：审计报告未单列持续经营重大不确定性段落 [待人工]
- 其他信息段：「示例科技股份有限公司管理层对其他信息负责。其他信息包括年度报告中涵盖的信息，但不包括财务报表和我们的审计报告。」〔锚：2025 年年度报告·第 118 页·其他信息段〕[S2]
- 上年度对照意见：本报告仅列示 2025 年度审计意见，未取到：上年度审计意见 [待人工]

## 五、未取到与口径

- 未取到：上年度审计意见
- 口径：意见类型与各事项段均为照抄，未归纳、未排序、未改写

## 六、来源

- [S1] 示例科技股份有限公司 2025 年年度报告｜https://example.com/000001-2025-annual.pdf｜检索日 2026-11-09
- [S2] 示例科技股份有限公司 2025 年年度报告·其他信息段｜https://example.com/000001-2025-annual.pdf｜检索日 2026-11-09
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

    # 两条类型行会同时撞形制（该节应恰一行）与类型一致（引号外出现另一个类型名），
    # 两道都该发——这是设计，不是互相溅。
    case("意见类型行重复",
         _mutate(DEMO, "- 意见类型：标准无保留意见｜",
                 "- 意见类型：保留意见｜「x」〔锚：y〕[S1]\n- 意见类型：标准无保留意见｜"),
         {"AU-STRUCT", "AU-OPINION"}, 1)
    case("空节",
         _mutate(DEMO, "- 意见基础：本报告未单列「形成意见的基础」一节，意见段后直接进入关键审计事项 [待人工]",
                 "本报告未单列形成意见的基础一节，意见段后直接进入关键审计事项。"),
         {"AU-STRUCT"}, 1)
    case("节序反了", DEMO.replace("## 一、审计意见", "## 一、審計意見"), {"AU-STRUCT"}, 1)

    case("原句为空",
         _mutate(DEMO, "「收入确认」", "「」"), {"AU-QUOTE"}, 1)
    case("来源缺检索日",
         _mutate(DEMO, "｜检索日 2026-11-09\n- [S2]", "\n- [S2]"), {"AU-QUOTE"}, 1)
    case("引用未登记",
         _mutate(DEMO, "〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S1]\n- 应对程序（一）",
                 "〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S9]\n- 应对程序（一）"),
         {"AU-QUOTE"}, 1)

    case("类型不在册",
         _mutate(DEMO, "- 意见类型：标准无保留意见｜", "- 意见类型：无保留意见｜"),
         {"AU-OPINION"}, 1)
    case("非标当结论",
         _mutate(DEMO, "- 意见基础：本报告未单列", "- 意见基础：本报告属非标意见，未单列"),
         {"AU-OPINION"}, 1)
    case("类型自相矛盾",
         _mutate(DEMO, "- 口径：意见类型与各事项段均为照抄",
                 "- 口径：本报告为保留意见，意见类型与各事项段均为照抄"),
         {"AU-OPINION"}, 1)

    case("正文缺口未点名",
         _mutate(DEMO, "- 未取到：上年度审计意见\n", "- 未取到：无\n"),
         {"AU-GAP"}, 1)
    case("第五节多点了名",
         _mutate(DEMO, "- 未取到：上年度审计意见", "- 未取到：上年度审计意见\n- 未取到：内部控制审计报告"),
         {"AU-GAP"}, 1)
    case("搪塞词",
         _mutate(DEMO, "- 未取到：上年度审计意见", "- 未取到：上年度审计意见（不适用）"),
         {"AU-GAP"}, 1)

    case("红线",
         _mutate(DEMO, "- 口径：意见类型", "- 口径：公司存在财务造假迹象，意见类型"),
         {"AU-LINE"}, 1)
    case("待人工豁免只到分句",
         _mutate(DEMO, "审计报告未单列强调事项段 [待人工]",
                 "审计报告未单列强调事项段 [待人工]，建议买入"),
         {"AU-LINE"}, 1)

    bad = 0
    for name, text, want_codes, want_rc in cases:
        found = analyze(text)
        got_codes = {c for c in CODES if found[c]}
        got_rc = 0 if sum(len(v) for v in found.values()) == 0 else 1
        ok = got_codes == want_codes and got_rc == want_rc
        if not ok:
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
        description="审计意见与非标事项·逐条挂源 —— 五道机检（零网络、零凭据）",
    )
    ap.add_argument("note", nargs="?", help="审计稿 markdown 路径")
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
        print("缺入参：给一份审计稿路径，或用 --demo / --selftest", file=sys.stderr)
        return 2
    try:
        text = Path(args.note).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"读不到文件：{args.note}（{exc}）", file=sys.stderr)
        return 3
    return run(text, args.note)


if __name__ == "__main__":
    sys.exit(main())
