#!/usr/bin/env python3
"""
1688 日报生成脚本 v2 — 紧凑文本格式
按运营日报模板：▌分段 + 单行关键指标 + 数据诊断

用法：
  python3 generate_report_v2.py <raw_data.json> [output.md]
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Windows 嵌入式 Python 默认 GBK 编码，强制 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = str(SKILL_DIR / '1688_daily_report.md')

def s(v, default='—'):
    if v is None: return default
    return str(v)

def pct(v):
    if v is None: return '—'
    try: return f'{round(float(v) * 100, 1)}%'
    except: return str(v)

def pct_raw(v):
    """百分比——已经是百分数值（如 46.39）的直接格式化"""
    if v is None: return '—'
    try: return f'{round(float(v), 1)}%'
    except: return str(v)

def rmb(v):
    if v is None: return '—'
    try: return f'¥{round(float(v)):,}'
    except: return f'¥{v}'

def num(v):
    if v is None: return '—'
    return str(v)

def build_report(raw_data):
    data = raw_data.get('data', {})
    sycm_list = data.get('sycm', [])
    work_list = data.get('work', [])

    sycm = sycm_list[-1] if sycm_list else {}
    work = work_list[-1] if work_list else {}

    today = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
    now = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

    item = sycm.get('itemOverview', {})
    fs = sycm.get('flowStats', {})
    inv = sycm.get('inquiry', {})
    trade = sycm.get('trade', {})
    rt = sycm.get('rankTrend', {})
    fs7 = sycm.get('flowSourceRecent7', {})
    kw7 = sycm.get('keywordsRecent7', {})
    trade7 = sycm.get('tradeRecent7', {})

    nlh = work.get('nlhScore', {})
    star = work.get('starScore', {})
    wr = work.get('wwResponse', {})
    l48 = work.get('lgt48hGotRate', {})
    lpa = work.get('lgtPlanAccRate', {})
    qr = work.get('qualityRfdRate', {})

    ic = item.get('itemCnt')
    ps = item.get('pullSalesItemCnt')
    uv = fs.get('uv')
    pv = fs.get('pv')
    reveal = fs.get('revealCnt')
    bounce = fs.get('bounceRate')
    mobile_share = fs.get('mobileShare')
    inquiry_count = inv.get('effectiveInQUsers')
    pay_amt = trade.get('payAmt')
    pay_byr = trade.get('payByrCnt')
    pay_mord = trade.get('payMordCnt')
    pay_item_qty = trade.get('payItemQty')
    pay_rate = trade.get('payRate')
    per_byr_amt = trade.get('perByrAmt')
    rfd_amt = trade.get('rfdSucAmt')
    refund_rate = trade.get('refundRate')
    new_byr = trade.get('payNewByrCnt')
    new_amt = trade.get('newBuyerAmt')
    new_share = trade.get('newBuyerShare')
    old_byr = trade.get('payOldByrCnt')
    old_amt = (float(pay_amt) - float(new_amt)) if pay_amt is not None and new_amt is not None else None
    old_share = trade.get('oldBuyerShare')
    old_per_amt = trade.get('oldBuyerPerAmt')

    nlh_score = nlh.get('score', '—')
    star_score = star.get('score', '—')

    rank_str = ''
    if rt.get('rank') and rt.get('layer'):
        rank_str = f'第{rt["layer"]}层级{rt["rank"]}名'
    
    # 类目兼容：rankTrend.cateLevel1 → sycm.category → work.cateLvl1Name
    cate1 = rt.get('cateLevel1') or sycm.get('category') or work.get('cateLvl1Name', '—')
    cate2 = rt.get('cateLevel2') or sycm.get('subCategory', '—')
    
    # 新灯塔补充文案
    nlh_writing = nlh.get('copyWriting', '')

    # ---- 动销率 ----
    dongxiao = pct(ps/ic) if ic and ps is not None and float(ic) > 0 else '0%'

    # ---- 点击转化率 ----
    raw_click_rate = fs.get('clickRate')
    # 点击转化率：原始数据为小数(0~1)，需要 ×100
    click_rate_display = pct(raw_click_rate) if raw_click_rate is not None else '—'
    
    # ---- 人均浏览量 ----
    avg_pvs = s(fs.get('avgPvs'))

    # ---- 询盘率 ----
    inquiry_rate = pct(inquiry_count/uv) if uv and inquiry_count is not None and float(uv) > 0 else '—'

    # ---- 询盘转化率 ----
    conv_rate = '—'
    if inv.get('effectiveInQUsers') and inv.get('bEffectiveInQUsers'):
        eff = int(inv['effectiveInQUsers'])
        beff = int(inv['bEffectiveInQUsers'])
        if eff > 0:
            conv_rate = pct(beff/eff)

    # ---- 无线访客占比 ----
    mobile_pct = pct(mobile_share)

    # ---- 支付转化率 ----
    pay_rate_str = pct(pay_rate)

    # ---- 客单价 ----
    unit_price = rmb(per_byr_amt)

    # ---- 整体退款率 ----
    refund_pct = pct(refund_rate)

    # ---- 退款占比：退款金额 ÷ 支付GMV ----
    refund_ratio = pct(rfd_amt/pay_amt) if pay_amt and rfd_amt is not None and float(pay_amt) > 0 else '0.0%'

    # ---- 新客 ----
    # 成交占比：优先用newBuyerShare，缺失时用newBuyerAmt/payAmt计算
    new_share_str = pct(new_share) if new_share is not None else (pct(new_amt / pay_amt) if pay_amt and new_amt is not None and float(pay_amt) > 0 else '—')
    new_amt_str = rmb(new_amt)
    old_share_str = pct(old_share)
    old_amt_str = rmb(old_amt)
    old_per_str = rmb(old_per_amt)

    # ---- 排名走势 ----
    raw_ranks = rt.get('rawRanks', [])
    rank_trend = ''
    if raw_ranks and len(raw_ranks) >= 2:
        if raw_ranks[-1] < raw_ranks[0]:
            rank_trend = f' ↑{raw_ranks[0] - raw_ranks[-1]}名'
        elif raw_ranks[-1] > raw_ranks[0]:
            rank_trend = f' ↓{raw_ranks[-1] - raw_ranks[0]}名'
        else:
            rank_trend = ' →持平'

    # ---- 新灯塔履约 ----
    wr_display = s(wr.get('display'))
    l48_display = s(l48.get('display'))
    lpa_display = s(lpa.get('display'))
    qr_display = s(qr.get('display'))

    # ---- 流量来源（只展示二级渠道TOP8，按访客降序） ----
    sources = fs7.get('sources', [])
    near7_total_pay = trade7.get('payAmt', 0) or 0
    top_sources = ''
    if sources:
        # 只取二级渠道
        l2 = [src for src in sources if src.get('outerLevel') == '2' or src.get('outerLevel') == 2]
        # 按访客降序排序
        sorted_l2 = sorted(l2, key=lambda x: x.get('uv', x.get('myUv', 0)), reverse=True)
        # 取TOP8
        for i, src in enumerate(sorted_l2[:8]):
            uv_val = src.get('uv', src.get('myUv', 0))
            crt_byr = src.get('fleadCrtByrCnt', 0) or 0
            crt_amt = src.get('fleadCrtOrdAmt', 0) or 0
            pay_amt_src = src.get('fleadPayAmt', 0) or 0
            pay_ratio = '—'
            if near7_total_pay and float(near7_total_pay) > 0:
                pay_ratio = pct(float(pay_amt_src) / float(near7_total_pay))
            top_sources += f'{i+1}.{src.get("name", "—")}：访客{uv_val} | 引导下单{int(crt_byr)}人/¥{round(float(crt_amt)):,} | 支付占比{pay_ratio}'
            if i < min(7, len(sorted_l2) - 1):
                top_sources += '\n'
    else:
        top_sources = '无数据'

    # ---- 关键词 ----
    keywords = kw7.get('keywords', [])
    near7_total_pay_kw = trade7.get('payAmt', 0) or 0
    top_keywords = ''
    if keywords:
        sorted_kw = sorted(keywords, key=lambda x: x.get('keywordRevealCnt', 0), reverse=True)
        for i, kw in enumerate(sorted_kw[:10]):
            reveal_cnt = kw.get('keywordRevealCnt', 0) or 0
            uv_val = kw.get('uv', 0) or 0
            click_rate = kw.get('clickRate', 0) or 0
            lead_amt = kw.get('leadPayAmt', 0) or 0
            lead_byr = kw.get('leadPayByrCnt', 0) or 0
            pay_ratio = '—'
            if near7_total_pay_kw and float(near7_total_pay_kw) > 0:
                pay_ratio = pct(float(lead_amt) / float(near7_total_pay_kw))
            top_keywords += f'{i+1}.{kw.get("keyword", "—")}：展现{int(reveal_cnt)} | 访客{uv_val} | 点击率{pct(click_rate)} | 引导支付{int(lead_byr)}人/¥{round(float(lead_amt)):,} | 支付占比{pay_ratio}'
            if i < min(9, len(sorted_kw) - 1):
                top_keywords += '\n'
    elif kw7:
        top_keywords = '无数据'
    else:
        top_keywords = '插件未采集到该字段'

    # ---- 数据诊断 - 由模型生成，脚本只输出占位符 ----
    diagnostics = '''[模型生成]

请基于以上数据生成数据诊断&执行计划，包含：
1. 数据异常点：指出哪些指标异常，分析可能原因
2. 渠道优化方向：根据流量来源数据，给出优化建议
3. 关键词优化动作：根据入店关键词，给出标题和关键词优化建议
4. 明日重点工作：按优先级列出3-5条具体可执行的行动项

要求：语言简洁务实，每条建议可落地执行，避免空泛。总结不超过150字。'''

    # ============ 组装报告 ============
    report = f"""【1688运营日报 | {today}】

▌一、店铺基础信息
店铺：{s(sycm.get('companyName'))} | 店铺层级：{rank_str}{rank_trend} | 类目：{s(cate1)}>{s(cate2)}
在线商品：{num(ic)}款 | 动销商品：{num(ps)}款 | 动销率：{dongxiao}

▌二、流量数据
总展现：{num(reveal)} | 总访客(UV)：{num(uv)} | 总浏览(PV)：{num(pv)}
人均浏览：{avg_pvs}页 | 点击转化率：{click_rate_display} | 询盘人数：{num(inquiry_count)}人 | 询盘率：{inquiry_rate} | 跳失率：{pct(bounce)} | 无线访客占比：{mobile_pct}

▌三、交易&售后数据
支付GMV：{rmb(pay_amt)} | 支付订单：{num(pay_mord)}单 | 支付买家数：{num(pay_byr)}人
支付转化率：{pay_rate_str} | 客单价：{unit_price}
退款金额：{rmb(rfd_amt)} | 退款率：{refund_pct} | 退款占比：{refund_ratio}

▌四、新老客结构
新客：成交{new_amt_str} / 买家{num(new_byr)}人 / 成交占比{new_share_str}
老客：成交{old_amt_str} / 买家{num(old_byr)}人 / 复购率{old_share_str} / 客单价{old_per_str}

▌五、新灯塔履约表现
综合分：{s(nlh_score)}分（{s(nlh.get('title'))}）{nlh_writing} | 3分钟响应率：{wr_display}% | 48H揽收率：{l48_display}%
物流时效达成率：{lpa_display}% | 品质退款率：{qr_display}%

▌六、TOP8流量渠道（访客排序）
{top_sources}

▌七、TOP10进店核心关键词
{top_keywords}

▌八、数据诊断
{diagnostics}

---
*1688 Data Claw v1.0.0 | {now}*
"""

    return report


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_report_v2.py <raw_data.json> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    with open(input_path, encoding='utf-8') as f:
        raw_data = json.load(f)

    report = build_report(raw_data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 日报已生成: {output_path} ({len(report)} bytes)")