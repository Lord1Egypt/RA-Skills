#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_scan.py — 招采萝卜坑识别 · 批量预筛引擎（Stage B）

作用：把「招采萝卜坑识别专家」的 9 类信号标尺 + 文档类型校验 + 内部矛盾自检
      做成一个**确定性、可复跑**的启发式预筛器，对一批招标文件（本地 .txt）
      跑出「疑似萝卜坑清单」，供 LLM 在 Stage C 做深度论证。

与 SKILL.md 的关系：
  - 本脚本是「可选加速器」——它只做**机械预筛**（召回候选），不做法律论证；
  - LLM 深度分析（SKILL.md §2.3~§2.5）是 Stage C，应在本脚本标记的候选上做，
    以大幅降低长文漏扫 + 节省 token。

输入：
  python batch_scan.py --corpus <dir_of_txt> [--out <out_dir>]
  （默认 corpus=同目录 docs/，out=同目录 scan_out/）

输出（scan_out/）：
  scan_results.csv      汇总矩阵：doc, doc_type, n_sections, risk_score, top_signals
  scan_results.json     逐文档详细命中（章节 + 信号 + 原文片段 + 风险权重）
  scan_summary.md       人读概览 + 每个文档的 Top 命中

设计原则：
  - 仅用标准库；不匹配外部依赖。
  - 预筛「宁枉勿纵」：命中即标记，由 Stage C 用标尺复核去误报。
  - 硬性失败（文件缺失/空）不影响其他文档。
"""

import os
import re
import sys
import json
import argparse
import csv

# ----------------------------------------------------------------------------
# 1) 章节切分（复用 SKILL.md §2.2 思路，精简为无依赖版）
# ----------------------------------------------------------------------------
HEADING_PATTERNS = [
    (1, re.compile(r'^\s*第[一二三四五六七八九十百千0-9]+[章节目编部分]')),
    (1, re.compile(r'^\s*[0-9]+[\.、]\s*[一-龥]{2,}')),
    (2, re.compile(r'^\s*[一二三四五六七八九十百千]+、[一-龥]{2,}')),
]
RISK_MARKERS = re.compile(r'[★▲]|实质性响应|不可偏离|废标|否决|无效投标|关键条款')
APPENDIX_MARKERS = re.compile(r'附件|附录|图纸|附[图表明单]')
PAYMENT_MARKERS = re.compile(r'付款|保证金|履约担保|预付款|违约金|垫资')


def detect_heading(line):
    s = line.strip()
    if not s or len(s) > 40:
        return None
    for level, pat in HEADING_PATTERNS:
        if pat.match(s):
            return level, s
    return None


def split_sections(text):
    sections = []
    cur = None
    buf = []

    def flush():
        nonlocal cur, buf
        if cur is not None:
            t = '\n'.join(buf).strip()
            if t:
                cur['text'] = t
                cur['flags'] = {
                    'hard_marker': bool(RISK_MARKERS.search(t)),
                    'appendix': bool(APPENDIX_MARKERS.search(t)),
                    'payment': bool(PAYMENT_MARKERS.search(t)),
                }
                sections.append(cur)
        cur = None
        buf = []

    for raw in text.splitlines():
        h = detect_heading(raw)
        if h is not None:
            flush()
            cur = {'heading': h[1], 'level': h[0], 'text': ''}
            buf = []
        else:
            if cur is None:
                cur = {'heading': '__preamble__', 'level': 0, 'text': ''}
                buf = []
            buf.append(raw)
    flush()
    for i, s in enumerate(sections, 1):
        s['id'] = f'S{i:02d}'
    return sections


# ----------------------------------------------------------------------------
# 2) 信号标尺的确定性正则（对应 references/carrot-pit-signals.md 9 类）
#    每条 pattern 带 (信号号, 风险权重, 说明)。权重用于 risk_score 粗排。
#    权重取值：高危表象=3，中危表象=2，低危/软性=1。
# ----------------------------------------------------------------------------
# 信号1 品牌/型号排他（含 v1.2.0 新增「同一品牌跨子系统绑定」变体）
SIG1 = [
    (1, 3, "直接指定品牌/型号", re.compile(r'(指定|须为|要求为|仅限|限于|限定)\s*[""]?\s*[一-龥A-Za-z0-9]{2,12}\s*(品牌|型号|原厂)')),
    (1, 3, "或相当于但限家数", re.compile(r'或相当于[^\n。]*限\s*[0-9]+\s*家')),
    (1, 3, "原厂/唯一授权", re.compile(r'(原厂授权|唯一授权|独家(代理|授权))')),
    (1, 3, "指定专利/软著", re.compile(r'(指定专利|专利号\s*ZL|指定的软件著作权|特定软著|特定软件著作权)')),
    (1, 3, "须为同一品牌(排他变体·v1.2)", re.compile(r'(?<![非不同])(须为同一品牌|须为同[一二三四五六七八九十]品牌|须为同一厂家|须为同[一二三四五六七八九十]厂商)')),
    (1, 3, "多子系统须为同一品牌(拼图坑·v1.2)", re.compile(r'([一-龥]{2,10}(系统|平台|软件|产品))[^。\n]{0,12}(须为同一品牌|须为同[一-龥]{0,4}品牌)')),
    (1, 2, "须提供品牌功能截图", re.compile(r'(须|应|需)\s*(提供|上传|附)\s*[一-龥A-Za-z0-9]{1,12}\s*(平台|系统|产品|软件)\s*(功能截图|界面截图|截图)')),
]
# 信号2 资质/认证组合排他
SIG2 = [
    (2, 2, "多认证叠加", re.compile(r'(须|应|需)\s*(同时)?\s*(具备|具有|持有|提供)\s*[^。\n]{0,30}(认证|资质|证书)[^。\n]{0,20}(、|，)[^。\n]{0,20}(认证|资质|证书)')),
    (2, 2, "特定体系认证", re.compile(r'(ISO\s*9001|ISO\s*27001|ISO\s*20000|ISO\s*27017|CMMI|ITSS|CS[0-9]|信息安全服务|CCRC|DSMM)')),
    (2, 2, "协会会员/特定协会", re.compile(r'(须为|应为|加入)[^。\n]{0,20}(协会会员|学会会员|协会)')),
]
# 信号3 业绩门槛量身
SIG3 = [
    (3, 3, "业绩金额+类型+规模叠加", re.compile(r'近\s*[0-9]+\s*年[^。\n]{0,40}(单项|合同)[^。\n]{0,20}(金额|≥|大于|以上)[^。\n]{0,20}[0-9]+\s*万')),
    (3, 2, "特定甲方类型业绩(须佐证相关)", re.compile(r'(近\s*[0-9]+\s*年|须|应|需|具有|具备)[^。\n]{0,30}(业绩|案例)[^。\n]{0,30}(省级|市级|国家级|政务云|三甲|高校|央企|用户数|金额|规模)')),
    (3, 2, "用户数/规模限定", re.compile(r'(用户数|用户规模|服务人数|接入数)\s*≥\s*[0-9]+')),
]
# 信号4 人员/设备门槛
SIG4 = [
    (4, 2, "人员数量门槛", re.compile(r'(须|应|需)\s*(配|配备|具有|拥有)\s*[^。\n]{0,15}(高级|副高|中级|注册)[^。\n]{0,15}(工程师|架构师|人员|人)')),
    (4, 3, "设备写死品牌型号", re.compile(r'(设备|仪器|工具)\s*[^。\n]{0,15}(品牌|型号)\s*[:：]?\s*[一-龥A-Za-z0-9]{2,12}')),
]
# 信号5 技术参数量身（最隐蔽）
SIG5 = [
    (5, 3, "异常精确参数值", re.compile(r'[0-9]+\.[0-9]+\s*(GHz|MHz|MB|GB|nm|mm|Mbps|Gbps)')),
    (5, 3, "私有指令集/协议", re.compile(r'(私有指令集|私有协议|专有技术|私有的|独家技术)')),
    (5, 2, "非标/冗余功能堆砌", re.compile(r'(非标|定制开发\b.{0,10}仅|冗余功能|独家功能)')),
]
# 信号6 评标办法倾向
SIG6 = [
    (6, 2, "本地化加分", re.compile(r'(本地(企业|注册|纳税|办公)|在[当本]地[^。\n]{0,10}(注册|设立|服务))[^。\n]{0,20}加\s*[0-9]+\s*分')),
    (6, 2, "特定案例/荣誉加分", re.compile(r'(特定|指定|XX)[^。\n]{0,20}(案例|业绩|荣誉|奖项)[^。\n]{0,15}加\s*[0-9]+\s*分')),
    (6, 2, "主观分无量化档位", re.compile(r'(由评委|专家)\s*[^。\n]{0,20}(自主|酌情|综合)\s*(打分|评分)[^。\n]{0,20}(未细化|无档位|不明确)')),
]
# 信号7 合同条款排他
SIG7 = [
    (7, 2, "指定验收/检测机构", re.compile(r'(验收|检测|测评)\s*[^。\n]{0,15}(须|应|由)\s*[^。\n]{0,15}(机构|单位|出具)')),
    (7, 2, "管辖地异常", re.compile(r'(争议|纠纷|诉讼)\s*[^。\n]{0,20}(由[^。\n]{0,10}(法院|仲裁)|管辖)')),
]
# 信号8 地域/所有制歧视
SIG8 = [
    (8, 3, "本地注册/纳税门槛", re.compile(r'(须在?[当本]地[^。\n]{0,12}(注册|纳税|设立|办公)|本地注册满)')),
    (8, 3, "排斥特定所有制", re.compile(r'(仅限|限于)\s*[^。\n]{0,10}(国有|国企|民营|外资|内资)')),
]
# 信号9 商务/资金隐性门槛
SIG9 = [
    (9, 2, "高额保证金", re.compile(r'(履约|投标)\s*(保证金|担保)[^。\n]{0,20}[0-9]+\s*(万|元|%)')),
    (9, 2, "0预付/长账期", re.compile(r'(预付款\s*0%|无预付款|0%\s*预付|按(季度|月)后付|验收后[^。\n]{0,10}付)')),
    (9, 2, "垫资/授信证明", re.compile(r'(垫资|银行授信|授信额度|资金证明)')),
]

ALL_SIGNALS = [SIG1, SIG2, SIG3, SIG4, SIG5, SIG6, SIG7, SIG8, SIG9]

# ----------------------------------------------------------------------------
# 3) 文档类型校验（v1.2.0 新增）：识别「投标人响应文件/报价文件」被误当招标文件
#    关键点：招标文件里常含「投标文件格式」附录，里面也有「我方/投标人声明」，
#    故不能只数词频——必须用「强结构标记」区分：
#      tender_struct=0 且 bidder_struct>=2 → 判定为投标人响应/报价文件（疑似误投）
# ----------------------------------------------------------------------------
BIDDER_STRUCT = re.compile(r'(投标总价|报价一览表|已标价|我方报价|我方投标|报价文件|响应报价|投标报价)')
TENDER_STRUCT = re.compile(r'(招标公告|招标邀请|投标人须知|评标(办法|方法|标准)|采购需求|采购人[:：]|招标项目编号|采购代理机?构)')

# ----------------------------------------------------------------------------
# 4) 内部矛盾自检（v1.2.0 新增）：抓「表面合规但自我打架」的红线
# ----------------------------------------------------------------------------
def internal_contradiction_checks(full_text):
    findings = []
    accepts_consortium = bool(re.search(r'接受联合体', full_text))
    # 单一来源须用「排他性同一品牌」口径，排除「非同一品牌/同一品牌产品金额达X%」等中性/公平规则
    requires_single_source = bool(re.search(r'(?<![非不同])(须为同一品牌|同一品牌\s*(的)?\s*(电子认证|证书|平台|系统|软件|产品)\s*须|须为同一厂家|唯一(授权|代理)|原厂授权)', full_text))
    if accepts_consortium and requires_single_source:
        findings.append("✓ 接受联合体，但要求单一来源（同一品牌/原厂授权）——联合体难以满足，疑似自相矛盾或变相锁标")

    no_specific_qual = bool(re.search(r'(特定资格要求[：:]\s*无|无特定资格要求|特定资格要求[：:]\s*无特殊)', full_text))
    has_cert_stack = bool(re.search(r'(ISO\s*9001|ISO\s*27001|CMMI|ITSS|CCRC|涉密|信息安全服务)', full_text))
    if no_specific_qual and has_cert_stack:
        findings.append("✓ 声明『无特定资格要求』，却堆砌多项认证/资质——表述与实质可能矛盾，需核实是否隐性门槛")

    # 专门面向中小企业须是「本项目级」肯定决策，排除通用政策套话（如「采购人应当专门面向…」）
    sme_only = bool(re.search(r'(本项目|本采购项目|本包)[^。\n]{0,40}专门面向(中小|小微)企业', full_text)) and \
               not bool(re.search(r'(不得限制大中|□\s*专门面向|非专门面向|☑\s*无)', full_text))
    allows_large_consortium = bool(re.search(r'(大中型企业与小微企业组成联合体|大型企业可)', full_text))
    if sme_only and allows_large_consortium:
        findings.append("✓ 『专门面向中小企业』与『允许大中型组成联合体』并存——政策口径需核对")
    return findings


# ----------------------------------------------------------------------------
# 5) 扫描单文档
# ----------------------------------------------------------------------------
def scan_doc(name, text):
    sections = split_sections(text)
    # 盲区统计
    n_hard = sum(1 for s in sections if s['flags']['hard_marker'])
    n_app = sum(1 for s in sections if s['flags']['appendix'])
    n_pay = sum(1 for s in sections if s['flags']['payment'])

    # 文档类型（强结构标记区分，避免把含「投标文件格式」附录的招标文件误判）
    n_bidder = len(BIDDER_STRUCT.findall(text))
    n_tender = len(TENDER_STRUCT.findall(text))
    if n_tender == 0 and n_bidder >= 2:
        doc_type = "投标人响应/报价文件(疑似误投)"
    elif n_tender == 0 and n_bidder == 0:
        doc_type = "类型不明"
    else:
        doc_type = "招标文件"

    # 信号预筛
    hits = []  # {sig, weight, desc, sec_id, sec_head, snippet, pos}
    for si, sig_group in enumerate(ALL_SIGNALS, 1):
        for (sig_no, weight, desc, pat) in sig_group:
            for m in pat.finditer(text):
                start = max(0, m.start() - 25)
                end = min(len(text), m.end() + 25)
                snippet = text[start:end].replace('\n', ' ').strip()
                hits.append({
                    'sig': sig_no, 'weight': weight, 'desc': desc,
                    'pos': m.start(), 'snippet': snippet[:120],
                    'sec_id': '', 'sec_head': ''
                })
                if len(hits) > 400:  # 安全阀，防极端长文
                    break
        if len(hits) > 400:
            break

    # 章节归属（后处理：按 pos 二分到 section）
    sec_spans = []
    acc = 0
    for s in sections:
        sec_spans.append((acc, acc + len(s['text']), s['id'], s['heading']))
        acc += len(s['text'])
    for h in hits:
        for (a, b, sid, shead) in sec_spans:
            if a <= h['pos'] < b:
                h['sec_id'], h['sec_head'] = sid, shead
                break

    # 风险粗分：取权重和（封顶），同信号多命中不重复加倍（去重到信号级权重）
    sig_weight = {}
    for h in hits:
        sig_weight[h['sig']] = max(sig_weight.get(h['sig'], 0), h['weight'])
    risk_score = sum(sig_weight.values())

    # 信号聚合（Top）
    sig_count = {}
    for h in hits:
        sig_count[h['sig']] = sig_count.get(h['sig'], 0) + 1
    top_signals = sorted(sig_count.items(), key=lambda x: -x[1])

    # 内部矛盾
    contradictions = internal_contradiction_checks(text)

    return {
        'name': name,
        'doc_type': doc_type,
        'n_bidder_markers': n_bidder,
        'n_tender_markers': n_tender,
        'n_sections': len(sections),
        'blind_spots': {'hard_marker': n_hard, 'appendix': n_app, 'payment': n_pay},
        'n_hits': len(hits),
        'risk_score': risk_score,
        'sig_count': sig_count,
        'top_signals': top_signals,
        'contradictions': contradictions,
        'hits': hits,
    }


# ----------------------------------------------------------------------------
# 6) 主流程
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description='萝卜坑批量预筛')
    ap.add_argument('--corpus', default=os.path.join(os.path.dirname(__file__), 'docs'),
                    help='本地 .txt 招标文件目录')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(__file__), 'scan_out'),
                    help='输出目录')
    args = ap.parse_args()

    if not os.path.isdir(args.corpus):
        print(f"❌ 语料目录不存在：{args.corpus}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(args.out, exist_ok=True)

    txts = sorted(f for f in os.listdir(args.corpus) if f.lower().endswith('.txt'))
    if not txts:
        print(f"⚠️ 语料目录无 .txt：{args.corpus}")
        sys.exit(0)

    results = []
    for fn in txts:
        path = os.path.join(args.corpus, fn)
        try:
            text = open(path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception as e:
            print(f"⚠️ 读取失败 {fn}: {e}", file=sys.stderr)
            continue
        if not text.strip():
            print(f"⚠️ 空文件跳过 {fn}")
            continue
        r = scan_doc(fn, text)
        results.append(r)
        print(f"✓ {fn}  类型={r['doc_type']}  章节={r['n_sections']}  命中={r['n_hits']}  风险分={r['risk_score']}  矛盾={len(r['contradictions'])}")

    # CSV 汇总
    csv_path = os.path.join(args.out, 'scan_results.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['doc', 'doc_type', 'n_sections', 'blind_hard', 'blind_appendix',
                    'blind_payment', 'n_hits', 'risk_score', 'top_signals', 'contradictions'])
        for r in sorted(results, key=lambda x: -x['risk_score']):
            top = ';'.join(f"{k}类x{v}" for k, v in r['top_signals'])
            w.writerow([r['name'], r['doc_type'], r['n_sections'],
                        r['blind_spots']['hard_marker'], r['blind_spots']['appendix'],
                        r['blind_spots']['payment'], r['n_hits'], r['risk_score'],
                        top, len(r['contradictions'])])

    # JSON 明细
    json_path = os.path.join(args.out, 'scan_results.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Markdown 概览
    md_path = os.path.join(args.out, 'scan_summary.md')
    lines = ['# 萝卜坑批量预筛概览', '']
    lines.append(f'> 共扫描 **{len(results)}** 份文档。本结果为**机械预筛**（召回候选），'
                 '非法律定论；每个命中须由「招采萝卜坑识别专家」SKILL.md §2.3~§2.5 做深度论证去误报。')
    lines.append('')
    lines.append('## 一、风险排序矩阵')
    lines.append('')
    lines.append('| 文档 | 类型 | 章节 | 命中 | 风险分 | Top 信号 | 内部矛盾 |')
    lines.append('|---|---|---|---|---|---|---|')
    for r in sorted(results, key=lambda x: -x['risk_score']):
        top = '、'.join(f"{k}类×{v}" for k, v in r['top_signals'][:4])
        lines.append(f"| {r['name']} | {r['doc_type']} | {r['n_sections']} | {r['n_hits']} | "
                     f"**{r['risk_score']}** | {top} | {len(r['contradictions'])} |")
    lines.append('')
    lines.append('## 二、逐文档 Top 命中与矛盾自检')
    lines.append('')
    for r in sorted(results, key=lambda x: -x['risk_score']):
        lines.append(f"### {r['name']}  （类型：{r['doc_type']} / 风险分 {r['risk_score']}）")
        lines.append('')
        if r['doc_type'].startswith('投标人响应'):
            lines.append('> ⚠️ **文档类型异常**：本文档疑似「投标人响应/报价文件」而非招标文件，'
                         '套用萝卜坑扫描无意义，请确认输入是否为招标方发出的采购文件。')
            lines.append('')
        if r['contradictions']:
            lines.append('**🔍 内部矛盾自检**：')
            for c in r['contradictions']:
                lines.append(f'- {c}')
            lines.append('')
        # Top 命中（每信号取 1 条代表）
        seen = set()
        lines.append('**预筛命中（信号 → 原文片段）**：')
        for h in sorted(r['hits'], key=lambda x: -x['weight']):
            key = (h['sig'], h['desc'])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- 信号{h['sig']}【{h['desc']}】 {h['sec_id']}：…{h['snippet']}…")
        lines.append('')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n✅ 扫描完成 → {args.out}")
    print(f"   CSV : {csv_path}")
    print(f"   JSON: {json_path}")
    print(f"   MD  : {md_path}")


if __name__ == '__main__':
    main()
