#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_working_capital.py — 存货与应收质量卡的机检（五道码）

用法：
    python3 -B scripts/check_working_capital.py <质量卡.md>
    python3 -B scripts/check_working_capital.py --selftest

五道码：
    WC-STRUCT  五节齐且有序 · 每节至少一项 · 申报数两向对齐
    WC-ANCHOR  原句非空 · 锚值非空（只剩 [S#] 视同空）· [S#] 能在来源索引里找到 · 来源行带 URL 与检索日
    WC-NOSELF  周转/增速/占比/账龄占比/账面价值：原句没有就必须标〔自算〕并交代分子分母；
               两个数不许自己相减（账面价值不许拿余额减准备）
    WC-GAP     未取到两向点名 · 零缺口须显式写「无」· 禁「不适用／无此项／无需披露」
    WC-LINE    红线四道：造假与暴雷 · 预测 · 评级目标价 · 建议关注

退码：0 全过（或 selftest 全合）；1 有发红；2 用法错；3 文件读不到或空稿。
零网络、纯标准库。
"""

from __future__ import annotations

import re
import sys

SECTIONS = ("存货", "应收账款", "合同资产", "计提与转回", "口径与未取到")

# 需要「原句」的项：值是抄自报表的数
ANCHORED = re.compile(r"^\s*[-*]\s*(存货账面余额|存货跌价准备期末余额|本期计提跌价准备|"
                      r"应收账款账面余额|坏账准备期末余额|本期计提坏账准备|"
                      r"合同资产账面价值|本期计提合计|本期转回或收回|账龄结构)")
# 若原句里没有，就必须是〔自算〕的项
SELFABLE = re.compile(r"(存货周转天数|应收账款周转天数|存货同比增速|应收账款同比增速|"
                      r"周转率|占比)")

CN_NUM = r"[0-9][0-9,\.]*"
PCT = re.compile(r"\d+(?:\.\d+)?\s*%")
SREF = re.compile(r"\[S(\d+)\]")
DECL = re.compile(r"共\s*(\d+)\s*项\s*[·：:|｜ 、]+\s*未取到\s*(\d+)\s*项")
GAP_NAMES = re.compile(r"^\s*[-*]\s*(?:未取到\s*\d+\s*项[:：])\s*(.+?)(?:——|—|:：|$)")
URL = re.compile(r"https?://\S+")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日")

# ── WC-LINE 的三组词形 ──
LINE_FRAUD = re.compile(r"财务造假|造假|虚增|舞弊|做假账|粉饰报表|暴雷|爆雷|业绩变脸|"
                        r"将出现大额减值|存在重大风险")
LINE_PREDICT = re.compile(r"预计(?:将|会)?|将会|有望|即将|下半年将|明年将|后续将|"
                          r"股价将|股价会|看多|看空")
LINE_RATING = re.compile(r"目标价|评级|买入评级|增持评级|强烈推荐|建议买入|建议卖出|"
                         r"投资建议")
LINE_WATCH = re.compile(r"建议关注|值得关注|重点关注|可关注")
# 「不构成投资建议」是免责句，不是评级——按整句豁免
LINE_RATING_OK = re.compile(r"不构成投资建议")

# 〔自算〕行的两个必须分句
SELF_TAG = re.compile(r"〔\s*自算\s*〕|【\s*自算\s*】|\[自算\]")
SELF_NUM = re.compile(r"分子[:：]")
SELF_DEN = re.compile(r"分母[:：]")


def zone_of(lines, head_re):
    """返回 head_re 命中的段的所有行（不含段头），遇到下一个同级或更高级段头即停。

    段头只认 `##`～`####`：`#` 是件名行，收进来会把件名当成段头。
    """
    out, started, level = [], False, None
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,4})\s+\S", ln)
        if m:
            if started and len(m.group(1)) <= (level or 99):
                break
            if not started and head_re.search(ln):
                started, level = True, len(m.group(1))
                continue
        if started:
            out.append((i, ln))
    return out


def item_rows_of(text):
    """正文项行——申报对账与 PASS 行共用同一套过滤，不许各数各的。

    口径：**五节内的一切项行**都算一项，不按「有没有挂原句」筛。
    原先只数带「」或〔自算〕或含「未取到」的行，于是裸写数字的行（自算却不标）不算项，
    申报数当场对不上——那会在 WC-NOSELF 已发红之外再造一条 WC-STRUCT 假红，
    把「少挂了原句」误报成「总数不对」。
    排除的只有：来源行 [S#]、未取到清单行、头部申报行。
    """
    lines = text.split("\n")
    out = []
    in_zone = False
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,4})\s+(?:\S+[、.．]\s*)?(.+?)\s*$", ln)
        if m:
            in_zone = any(s in m.group(2) for s in SECTIONS)
            continue
        if not in_zone:
            continue
        if not re.match(r"^\s*[-*]\s+\S", ln):
            continue
        if re.match(r"^\s*[-*]\s*\[S\d+\]", ln):
            continue
        if re.match(r"^\s*[-*]\s*未取到\s*\d+\s*项", ln):
            continue
        if re.match(r"^\s*[-*]\s*共\s*\d+\s*项", ln):
            continue
        # 「口径：」「[待人工]」是说明行与判断位，不是要素项——它们属于第五节的元信息。
        # 不排除会把好样 15 项数成 17 项。
        if re.match(r"^\s*[-*]\s*(口径[:：]|\[待人工\]|待人工[:：])", ln):
            continue
        out.append((i, ln))
    return out


def noself_scan(lines):
    """WC-NOSELF 全扫。返回 (findings, owned_lines)。

    owned_lines 是它报过/认领的行号——WC-ANCHOR 要跳过这些行。
    分工：一行既没原句又没标〔自算〕，那是「自算未标」（NOSELF），不是「原句为空」（ANCHOR）；
    「不适用」归 WC-GAP；骨架占位行「待挂」两边都不认领（它该红在缺原句上）。
    两处都报同一行就是同一缺陷两种码，fixer 会以为要改两处（实测坏样三/四各多报一条）。
    """
    findings, owned = [], set()

    # ① 周转/增速/占比行：原句含百分比或天数即认；否则必须〔自算〕+ 分子分母
    for i, ln in enumerate(lines):
        m = SELFABLE.search(ln)
        if not m or not re.match(r"^\s*[-*]\s+", ln):
            continue
        if re.search(r"不适用|无此项|无需披露", ln):
            continue          # WC-GAP 的判域
        if re.match(r"^\s*[-*]\s*未取到\s*\d+\s*项", ln):
            continue          # 缺口清单行只是点名
        if re.search(r"待挂|待填|待补", ln):
            continue          # 骨架占位行：没抄原句也没算数
        name = m.group(1)
        owned.add(i + 1)
        if SELF_TAG.search(ln):
            block = ln
            j = i + 1
            while j < len(lines) and lines[j].strip() and not re.match(r"^\s*[-*]\s+\S", lines[j]):
                block += lines[j]
                j += 1
            if not SELF_NUM.search(block):
                findings.append(("WC-NOSELF", i + 1, "%s〔自算〕缺「分子：」出处" % name))
            if not SELF_DEN.search(block):
                findings.append(("WC-NOSELF", i + 1, "%s〔自算〕缺「分母：」出处" % name))
            if not SREF.search(block):
                findings.append(("WC-NOSELF", i + 1, "%s〔自算〕缺 [S#] 出处" % name))
            continue
        q = re.search(r"「(.*?)」", ln)
        body = q.group(1) if q else ""
        if not (PCT.search(body) or re.search(r"\d+(?:\.\d+)?\s*天", body)):
            findings.append(("WC-NOSELF", i + 1,
                             "%s:原句里没有该数——须标〔自算〕并写明分子分母，或改判未取到" % name))

    # ② 账面价值不许拿余额减准备自己算。
    # 判据：项名是「…账面价值」，且该行出现减号或同时出现余额与准备两个词，
    # **而原句里没有账面价值本身**——原句里写了就是报表算的，本件照抄不算自算。
    for i, ln in enumerate(lines):
        if not re.match(r"^\s*[-*]\s+", ln):
            continue
        if "账面价值" not in ln.split("：")[0].split(":")[0]:
            continue
        q = re.search(r"「(.*?)」", ln)
        quoted = q.group(1) if q else ""
        if "账面价值" in quoted:
            continue
        if re.search(r"待挂|待填|待补", ln):
            continue
        if re.search(r"[-−–]", ln) or (re.search(r"账面余额", ln) and re.search(r"准备", ln)):
            owned.add(i + 1)
            findings.append(("WC-NOSELF", i + 1,
                             "账面价值不许拿账面余额减准备自己算——除非报表同一句写了"))
    return findings, owned


def check(text):
    findings = []
    lines = text.split("\n")
    noself_findings, noself_lines = noself_scan(lines)
    findings.extend(noself_findings)

    # ── 来源索引（第六段，但本件五节制；来源行可落在任一节尾，按 [S#] 行扫） ──
    srcs = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*[-*]\s*\[S(\d+)\]\s*(.*)$", ln)
        if m:
            srcs[m.group(1)] = (i, m.group(2))

    # ── WC-STRUCT ①五节齐且有序 ──
    heads = []
    for i, ln in enumerate(lines):
        m = re.match(r"^#{2,4}\s+(?:\S+[、.．]\s*)?(.+?)\s*$", ln)
        if m:
            heads.append((i, m.group(1).strip(), ln))
    found_order = []
    for want in SECTIONS:
        hit = [h for h in heads if want in h[1]]
        if not hit:
            findings.append(("WC-STRUCT", 0, "缺「%s」节" % want))
        else:
            found_order.append((hit[0][0], want))
    if len(found_order) == len(SECTIONS):
        idx = [x[0] for x in found_order]
        if idx != sorted(idx):
            findings.append(("WC-STRUCT", 0, "五节顺序不对：要求 存货→应收账款→合同资产→计提与转回→口径与未取到"))

    # ── WC-STRUCT ②每节至少一项 ──
    # 节整个缺失时只报一次「缺节」，不再叠报「该节没有项行」——同一缺陷报两条，
    # 排查的人会以为是两个问题（实测：坏样一曾同时报 2 条）。
    for want in SECTIONS:
        if not any(want in h[1] for h in heads):
            continue
        z = zone_of(lines, re.compile(re.escape(want)))
        items = [ln for _, ln in z if re.match(r"^\s*[-*]\s+\S", ln)]
        if not items:
            findings.append(("WC-STRUCT", 0, "「%s」节没有项行" % want))

    # ── WC-STRUCT ③申报数两向对齐 ──
    decl = None
    for i, ln in enumerate(lines):
        m = DECL.search(ln)
        if m:
            decl = (i, int(m.group(1)), int(m.group(2)))
            break
    # 正文里的「项」＝带原句或标未取到的项行。
    # 必须排除三类：来源行、未取到清单行、以及**头部申报行本身**——
    # 申报行含「未取到」三字，不排除会把自己数成一条项行（实测好样 14 项被数成 15）。
    item_rows = item_rows_of(text)
    gap_rows = [x for x in item_rows if "未取到" in x[1] and "「" not in x[1]
                and not re.match(r"^\s*[-*]\s*未取到\s*\d+\s*项", x[1])]
    if decl is None:
        findings.append(("WC-STRUCT", 0, "缺头部申报「共 N 项·未取到 M 项」"))
    else:
        i, n, m_ = decl
        # 「未取到 M 项」与正文的对账归 WC-GAP（派单把两向点名分给它）；
        # 这里只在**申报说 0 项而正文真有缺口行**时报虚报，两种方向不重复计红。
        if m_ == 0 and gap_rows:
            findings.append(("WC-STRUCT", i + 1, "申报未取到 0 项，但正文有 %d 条缺口行（虚报）" % len(gap_rows)))
        if n and len(item_rows) != n:
            findings.append(("WC-STRUCT", i + 1,
                             "申报共 %d 项，正文实有 %d 条项行（两向必对）" % (n, len(item_rows))))

    # ── WC-ANCHOR ──
    # 判据绑定**五节内的项行**，不绑定项名白名单，也不绑定「行里有没有引号」：
    #   原先按 ANCHORED 那串名字匹配，于是不在串里的项名连同空锚一起绕过检查（实测坏样二未发）；
    #   若再要求「有引号才查」，则骨架那种根本没有引号的行全被放过——判据形同虚设。
    # 项名可以新加，原句+锚+来源编号这三样不能少。
    for i, ln in item_rows:
        if "未取到" in ln:
            continue
        if (i + 1) in noself_lines:
            continue
        # 「不适用／无此项／无需披露」归 WC-GAP：它已经报过「替报表下结论」，
        # 这里再报「原句为空」是同一行两次计红（实测坏样四）。
        if re.search(r"不适用|无此项|无需披露", ln):
            continue
        label = re.sub(r"^\s*[-*]\s+", "", ln).split("：")[0].split(":")[0].strip()
        q = re.search(r"「(.*?)」", ln)
        if not q or not q.group(1).strip():
            findings.append(("WC-ANCHOR", i + 1, "%s行:原句为空（缺「」引文）" % label))
            continue
        a = re.search(r"锚[：:](.*?)(?=\[S\d+\]|$)", ln)
        if not a or not SREF.sub("", a.group(1)).strip():
            findings.append(("WC-ANCHOR", i + 1, "%s行:锚值为空（只剩来源编号，缺定位）" % label))
        refs = SREF.findall(ln)
        if not refs:
            findings.append(("WC-ANCHOR", i + 1, "%s行:缺 [S#] 来源编号" % label))
        for r in refs:
            if r not in srcs:
                findings.append(("WC-ANCHOR", i + 1, "%s行:来源 [S%s] 不在来源索引里" % (label, r)))
    for sid, (i, body) in srcs.items():
        if not URL.search(body):
            findings.append(("WC-ANCHOR", i + 1, "[S%s] 行缺 URL" % sid))
        if "检索日" not in body or not DATE.search(body):
            findings.append(("WC-ANCHOR", i + 1, "[S%s] 行缺检索日或检索日不合形" % sid))

    # ── WC-GAP ──
    for i, ln in enumerate(lines):
        if re.search(r"不适用|无此项|无需披露", ln) and re.match(r"^\s*[-*]\s+", ln):
            findings.append(("WC-GAP", i + 1, "禁写「不适用／无此项／无需披露」——那是替报表下结论"))
    gap_decl = None
    for i, ln in enumerate(lines):
        m = re.search(r"未取到\s*(\d+)\s*项[:：]\s*(.*)$", ln)
        if m:
            gap_decl = (i, int(m.group(1)), m.group(2))
            break
    if decl is not None and decl[2] == 0:
        if not re.search(r"未取到\s*0\s*项\s*[:：]\s*(?:无|无。|$)", "\n".join(lines)):
            findings.append(("WC-GAP", 0, "零缺口须显式写「未取到 0 项：无」，不能靠留空"))
    if gap_decl and decl is not None:
        if gap_decl[1] != decl[2]:
            findings.append(("WC-GAP", gap_decl[0] + 1,
                             "未取到清单写 %d 项，头部申报写 %d 项" % (gap_decl[1], decl[2])))
        # 清单点名的名目数必须等于清单自报的条数——多报是虚报、少报是漏报。
        # 只取破折号**之前**的名字串：破折号后是「为什么缺、回哪份文件核对」的说明，
        # 说明里的顿号不是名目分隔符（实测：把整段拿来切，好样「1 项」被数成 2 项）。
        names_part = re.split(r"——|—", gap_decl[2])[0]
        names = [x for x in re.split(r"[、，,；;]", names_part) if x.strip()]
        # 「未取到 0 项：无。」里的「无」是零缺口的写法，不是名目——不排除会把 0 项数成 1 项。
        names = [x for x in names if x.strip().strip("。.，,") not in ("无", "")]
        if names and len(names) != gap_decl[1]:
            findings.append(("WC-GAP", gap_decl[0] + 1,
                             "未取到清单自报 %d 项，实际点名 %d 项（两向必对）"
                             % (gap_decl[1], len(names))))
    # 正文缺口行数与申报数的对账（此前放在 WC-STRUCT，与两向点名重复计红）
    if decl is not None and gap_decl is not None:
        body_gap = [x for x in item_rows
                    if "未取到" in x[1] and "「" not in x[1]
                    and not re.match(r"^\s*[-*]\s*未取到\s*\d+\s*项", x[1])]
        if len(body_gap) != decl[2]:
            findings.append(("WC-GAP", 0,
                             "申报未取到 %d 项，正文实有 %d 条缺口行（两向必对）"
                             % (decl[2], len(body_gap))))

    # ── WC-LINE ──
    for i, ln in enumerate(lines):
        if re.match(r"^\s*[-*]?\s*>?\s*(AI 整理初稿|免责|不构成投资建议)", ln):
            continue
        body = LINE_RATING_OK.sub("", ln)
        if LINE_FRAUD.search(body):
            findings.append(("WC-LINE", i + 1, "红线·造假暴雷：%s" % LINE_FRAUD.search(body).group(0)))
        elif LINE_PREDICT.search(body):
            findings.append(("WC-LINE", i + 1, "红线·预测：%s" % LINE_PREDICT.search(body).group(0)))
        elif LINE_RATING.search(body):
            findings.append(("WC-LINE", i + 1, "红线·评级目标价：%s" % LINE_RATING.search(body).group(0)))
        elif LINE_WATCH.search(body):
            findings.append(("WC-LINE", i + 1, "红线·建议关注：%s" % LINE_WATCH.search(body).group(0)))
    return findings


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 2:
        print(__doc__)
        return 2
    p = argv[1]
    try:
        with open(p, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError) as exc:
        print("读不到输入：%s（%s）" % (p, exc))
        return 3
    if not text.strip():
        print("空稿：%s" % p)
        return 3

    findings = check(text)
    if not findings:
        # 这里的项行计数必须与 WC-STRUCT 申报对账用的是同一套过滤，否则 PASS 行报的数和申报数对不上——
        # 同一件事出两个数，正是本件禁止的读法（实测：另一套过滤会多算申报行与清单行，报 17 而申报 15）。
        n_items = len(item_rows_of(text))
        print("PASS 五道码全过｜项行 %d" % n_items)
        return 0
    for code, ln_, msg in findings:
        where = ("第%d行 " % ln_) if ln_ else ""
        print("%s %s%s" % (code, where, msg))
    print("不合 %d 条" % len(findings))
    return 1


def selftest():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    fx = os.path.join(here, "fixtures")
    cases = [("good-working-capital.md", 0, None),
             ("bad-1-struct.md", 1, "WC-STRUCT"),
             ("bad-2-anchor.md", 1, "WC-ANCHOR"),
             ("bad-3-noself.md", 1, "WC-NOSELF"),
             ("bad-4-gap.md", 1, "WC-GAP"),
             ("bad-5-line.md", 1, "WC-LINE")]
    ok = True
    for name, want_rc, want_code in cases:
        p = os.path.join(fx, name)
        try:
            text = open(p, "r", encoding="utf-8").read()
        except (IOError, OSError):
            print("✗ %s 读不到" % name)
            ok = False
            continue
        fs = check(text)
        rc = 0 if not fs else 1
        codes = sorted({c for c, _, _ in fs})
        if rc != want_rc:
            print("✗ %s 退码 %d，期望 %d" % (name, rc, want_rc))
            ok = False
            continue
        if want_code:
            if codes != [want_code]:
                print("✗ %s 应只发 %s，实发 %s" % (name, want_code, "／".join(codes) or "无"))
                ok = False
                continue
            print("✓ 坏样只发 %s（共 %d 条）" % (want_code, len(fs)))
        else:
            print("✓ 好样全过")
    print("自测：全合" if ok else "自测：不合")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
