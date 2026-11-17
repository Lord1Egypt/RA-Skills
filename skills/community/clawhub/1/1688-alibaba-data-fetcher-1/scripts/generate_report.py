#!/usr/bin/env python3
"""
1688 日报生成脚本
读取插件采集的原始JSON数据，按 Excel 模板字段映射生成 Markdown 日报。
包含数据小结（经营概况/流量诊断/客户运营/履约诊断/次日行动建议）。

用法：
  python3 generate_report.py <raw_data.json> [output.md]
  
  默认输出到 workspace 目录下的 1688_daily_report.md
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 默认输出目录：skill 所在目录
SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = str(SKILL_DIR / '1688_daily_report.md')

# ============================================================
# 字段映射：Excel 模板  ↔  插件数据路径
# ============================================================
FIELD_MAP = {
    # 一、店铺基础信息
    "店铺名称":       ("companyName", "sycm", "str"),
    "统计日期":       ("flowStats.statDate", "sycm", "str"),
    "主营类目":       ("category + subCategory", "sycm", "cat"),
    "店铺层级排名":   ("rankTrend.rank + rankTrend.layer", "sycm", "rank"),
    "新灯塔综合总分": ("nlhScore.score", "work", "str"),
    "当前店铺星级":   ("starScore.score", "work", "str"),
    "在线商品数":     ("itemOverview.itemCnt", "sycm", "int"),
    "动销商品数":     ("itemOverview.pullSalesItemCnt", "sycm", "int"),
    "动销率":         ("itemOverview", "sycm", "ratio"),

    # 二、流量数据
    "展现次数":       ("flowStats.revealCnt", "sycm", "int"),
    "浏览量(PV)":     ("flowStats.pv", "sycm", "int"),
    "访客数(UV)":     ("flowStats.uv", "sycm", "int"),
    "点击转化率":     ("flowStats.clickRate", "sycm", "pct_str"),
    "询盘人数":       ("inquiry.effectiveInQUsers", "sycm", "int"),
    "询盘率":         ("inquiry / flowStats", "sycm", "ratio"),
    "无线端访客占比": ("flowStats.mobileShare", "sycm", "pct"),
    "跳失率":         ("flowStats.bounceRate", "sycm", "pct"),
    "人均浏览量":     ("flowStats.avgPvs", "sycm", "float"),

    # 三、交易数据
    "支付金额":       ("trade.payAmt", "sycm", "rmb"),
    "支付订单数":     ("trade.payMordCnt", "sycm", "int"),
    "支付买家数":     ("trade.payByrCnt", "sycm", "int"),
    "支付商品件数":   ("trade.payItemQty", "sycm", "int"),
    "支付转化率":     ("trade.payRate", "sycm", "pct"),
    "客单价":         ("trade.perByrAmt", "sycm", "rmb"),
    "退款金额":       ("trade.rfdSucAmt", "sycm", "rmb"),
    "整体退款率":     ("trade.refundRate", "sycm", "pct"),

    # 四、客户结构
    "支付新买家数":   ("trade.payNewByrCnt", "sycm", "int"),
    "新买家支付金额": ("trade.newBuyerAmt", "sycm", "rmb"),
    "新客成交占比":   ("trade.newBuyerShare", "sycm", "pct"),
    "支付老买家数":   ("trade.payOldByrCnt", "sycm", "int"),
    "老客复购率":     ("trade.oldBuyerShare", "sycm", "pct"),
    "老客客单价":     ("trade.oldBuyerPerAmt", "sycm", "rmb"),

    # 六、新灯塔履约
    "3分钟响应率":    ("wwResponse.display", "work", "pct_val"),
    "咨询满意度":     ("wwSatisfaction.display", "work", "pct_val"),
    "48H揽收率":      ("lgt48hGotRate.display", "work", "pct_val"),
    "履约率":         ("lgtFulfillRate.display", "work", "pct_val"),
    "物流时效达成率": ("lgtPlanAccRate.display", "work", "pct_val"),
    "72H支签率":      ("lgt72hReceiveRate.display", "work", "pct_val"),
    "品质退款率":     ("qualityRfdRate.display", "work", "pct_val"),
}

# ============================================================
# 工具函数
# ============================================================

def s(v, default='—'):
    if v is None: return default
    return str(v)

def pct(v):
    if v is None: return '—'
    try: return f'{round(float(v) * 100, 2)}%'
    except: return str(v)

def rmb(v):
    if v is None: return '—'
    try: return f'¥{round(float(v), 2)}'
    except: return f'¥{v}'

def num(v):
    if v is None: return '—'
    return str(v)

def get_nested(d, path):
    """从嵌套字典中按点分隔路径取值"""
    keys = path.split('.')
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d

# ============================================================
# 数据小节生成
# ============================================================

def build_summary(sycm, work):
    """生成十、数据小结"""
    sections = []

    nlh = work.get('nlhScore', {})
    star = work.get('starScore', {})
    wr = work.get('wwResponse', {})
    qs = work.get('qualityScore', {})
    rs = work.get('refundScore', {})
    ls = work.get('lgtScore', {})
    ws = work.get('wwScore', {})
    item = sycm.get('itemOverview', {})
    fs = sycm.get('flowStats', {})
    inv = sycm.get('inquiry', {})
    trade = sycm.get('trade', {})
    rt = sycm.get('rankTrend', {})

    pay_amt = trade.get('payAmt')
    recent_no_trade = (pay_amt is None or float(pay_amt) == 0)
    ic = item.get('itemCnt')
    ps = item.get('pullSalesItemCnt')
    rank_up = rt.get('rawRanks') and len(rt.get('rawRanks', [])) >= 2 and rt['rawRanks'][-1] < rt['rawRanks'][0]
    nlh_s = float(nlh.get('score', 0)) if nlh.get('score') else 0

    # 1. 经营概况
    overview = f"""**总体评价：** {'⚠️ 店铺近期无成交，处于起步阶段' if recent_no_trade else '店铺运营平稳'}

**核心指标：**

| 指标 | 数值 | 简评 |
|------|------|------|
| 在线商品数 | {num(ic)} | {'⚠️ 商品数极少，建议上新' if ic and int(ic) < 5 else '✅ 正常'} |
| 动销率 | {pct(ps/ic) if ic and ps is not None and float(ic) > 0 else '0%'} | {'⚠️ 无动销商品' if not ps or int(ps) == 0 else '✅ 正常'} |
| 店铺排名 | 第{num(rt.get('rank'))}名 | {'✅ 排名上升中' if rank_up else '保持关注'} |
| 新灯塔分 | {s(nlh.get('score'))} | {'⚠️ ' + nlh.get('copyWriting', '') if nlh.get('copyWriting') else '—'} |
"""
    sections.append(("经营概况", overview))

    # 2. 流量诊断
    uv = fs.get('uv')
    reveal = fs.get('revealCnt')
    bounce = fs.get('bounceRate')
    inquiry_count = inv.get('effectiveInQUsers')
    mobile_share = fs.get('mobileShare')

    flow_diag = ""
    if reveal and int(reveal) <= 1:
        flow_diag += "- **⚠️ 展现极少（仅1次）**：店铺几乎无搜索曝光，需优化商品标题/关键词，或参与平台活动提升曝光。\n"
    if bounce and float(bounce) > 0.4:
        flow_diag += f"- **⚠️ 跳失率偏高（{pct(bounce)}）**：{pct(bounce)}的访客进入后仅浏览1页就离开，建议优化商品详情页和店铺首页引导。\n"
    if mobile_share and float(mobile_share) == 0:
        flow_diag += "- **⚠️ 无线端流量为0**：检查是否有无线端适配问题，目前流量完全来自PC端。\n"
    if inquiry_count and int(inquiry_count) >= 20:
        flow_diag += f"- **✅ 询盘活跃（{int(inquiry_count)}人）**：咨询意愿强，但需关注转化率。\n"
    if uv and int(uv) > 0:
        flow_diag += f"- 访客数 {int(uv)}，人均浏览 {s(fs.get('avgPvs'))} 页。\n"
    if not flow_diag:
        flow_diag = "- 暂无足够流量数据进行分析。\n"
    sections.append(("流量诊断", flow_diag))

    # 3. 客户运营
    customer_diag = ""
    if recent_no_trade:
        customer_diag += "- **⚠️ 近期无成交**：无新老买家数据，建议从询盘转化入手，优化客服响应和成交话术。\n"
    else:
        new_share = trade.get('newBuyerShare')
        old_share = trade.get('oldBuyerShare')
        if new_share is not None:
            customer_diag += f"- 新客成交占比 {pct(new_share)}，老客复购率 {pct(old_share)}。\n"

    if inv.get('effectiveInQUsers') and inv.get('bEffectiveInQUsers'):
        eff = int(inv['effectiveInQUsers'])
        beff = int(inv['bEffectiveInQUsers'])
        conv_rate = beff / eff if eff > 0 else 0
        customer_diag += f"- **询盘转化率 {pct(conv_rate)}**：{eff}人询盘，仅{beff}人转化。\n"
    if not customer_diag:
        customer_diag = "- 暂无足够客户数据进行分析。\n"
    sections.append(("客户运营", customer_diag))

    # 4. 付费投放
    ad_diag = "- 当前插件未采集数字营销数据，无法提供付费投放诊断。\n"
    ad_diag += "- 建议：如已开通数字营销，可在生意参谋→营销分析模块查看广告ROI；如未开通，建议先优化自然流量和商品基建后再考虑付费推广。\n"
    sections.append(("付费投放诊断", ad_diag))

    # 5. 履约诊断
    fulfill_diag = ""
    if nlh_s < 3.0:
        fulfill_diag += f"- **⚠️ 新灯塔综合分 {nlh_s}（{nlh.get('title', '差')}）**：严重落后同行，需全面改进。\n"

    dims = [
        (qs, '商品体验', '增加商品详情描述和实拍图', '15%'),
        (rs, '售后体验', '优化退货退款流程，主动联系买家', '30%'),
        (ls, '物流体验', '提升发货速度，使用优质物流', '35%'),
        (ws, '咨询体验', '保证客服在线，提升响应速度', '20%'),
    ]
    for sc, name, suggestion, weight in dims:
        sc_val = float(sc.get('score', 0)) if sc.get('score') else 0
        if sc_val < 4.0:
            fulfill_diag += f"- **{name} {sc_val}分（{sc.get('title', '差')}，权重{weight}）**：{sc.get('copyWriting', '')} → {suggestion}\n"

    if wr.get('display') is not None and float(wr.get('display', 0)) < 50:
        fulfill_diag += f"- **3分钟响应率 {s(wr.get('display'))}%**（同行平均 {s(wr.get('averageScore'))}）：⚠️ 严重偏低，确保工作时间旺旺在线\n"

    if not fulfill_diag:
        fulfill_diag = "- 履约数据正常，继续保持。\n"
    sections.append(("履约诊断", fulfill_diag))

    # 6. 次日行动建议
    actions = []
    if recent_no_trade:
        actions.append("【优先级最高】推动首单成交：从询盘客户中筛选意向强的，主动跟进促单")
    if inv.get('effectiveInQUsers') and int(inv['effectiveInQUsers']) >= 20 and inv.get('bEffectiveInQUsers'):
        eff = int(inv['effectiveInQUsers'])
        beff = int(inv['bEffectiveInQUsers'])
        if beff < eff * 0.3:
            actions.append(f"【客户跟进】{eff}人询盘仅{beff}人转化，建议复盘聊天记录，优化话术模板")
    if ic and int(ic) <= 5:
        actions.append("【商品上新】当前商品数极少，建议尽快上架新品扩充SKU")
    if nlh_s < 3.0:
        actions.append("【服务提分】新灯塔分数偏低，建议从权重最高的物流体验和售后体验入手改进")
    if wr.get('display') is not None and float(wr.get('display', 0)) < 10:
        actions.append("【客服响应】3分钟响应率严重偏低，确保工作时间旺旺在线，可设置自动回复")
    if reveal and int(reveal) <= 1:
        actions.append("【搜索曝光】展现极少，检查商品标题是否包含买家搜索关键词，优化主图")
    actions.append("【数据监控】建议每日同一时间查看数据，建立趋势对比")

    action_text = "\n".join(f"{i+1}. {a}" for i, a in enumerate(actions))
    sections.append(("次日运营行动建议", action_text))

    return sections

# ============================================================
# 主报告生成
# ============================================================

def generate_report(raw_data, output_path):
    """从 raw_data JSON 生成完整日报"""
    data = raw_data.get('data', {})
    sycm_list = data.get('sycm', [])
    work_list = data.get('work', [])

    sycm = sycm_list[-1] if sycm_list else {}
    work = work_list[-1] if work_list else {}

    today = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
    now_str = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

    item = sycm.get('itemOverview', {})
    fs = sycm.get('flowStats', {})
    inv = sycm.get('inquiry', {})
    trade = sycm.get('trade', {})
    rt = sycm.get('rankTrend', {})
    fs7 = sycm.get('flowSourceRecent7', {})

    nlh = work.get('nlhScore', {})
    star = work.get('starScore', {})
    wr = work.get('wwResponse', {})
    wsf = work.get('wwSatisfaction', {})
    l48 = work.get('lgt48hGotRate', {})
    lpa = work.get('lgtPlanAccRate', {})
    qr = work.get('qualityRfdRate', {})
    lfr = work.get('lgtFulfillRate', {})
    l72 = work.get('lgt72hReceiveRate', {})

    ic = item.get('itemCnt')
    ps = item.get('pullSalesItemCnt')
    pay_amt = trade.get('payAmt')
    new_amt = trade.get('newBuyerAmt')
    old_amt = (float(pay_amt) - float(new_amt)) if pay_amt is not None and new_amt is not None else None

    # 统计日期
    stat_date = s(fs.get('statDate'))

    report = f"""# 1688 日报 - {today}

**店铺：** {s(sycm.get('companyName'))}
**生成时间：** {now_str}

---

## 一、店铺基础信息

| 字段 | 值 |
|------|-----|
| 店铺名称 | {s(sycm.get('companyName'))} |
| 统计日期 | {stat_date} |
| 主营类目 | {s(sycm.get('category'))} > {s(sycm.get('subCategory'))} |
| 店铺层级排名 | {'第' + s(rt.get('layer')) + '层级 ' + s(rt.get('rank')) + '名' if rt.get('rank') else '—'} |
| 新灯塔综合总分 | {s(nlh.get('score'))} |
| 当前店铺星级 | {s(star.get('score'))}星 |
| 在线商品数 | {num(ic)} |
| 动销商品数 | {num(ps)} |
| 动销率 | {pct(ps/ic) if ic and ps is not None and float(ic) > 0 else '—'} |

---

## 二、流量数据

| 字段 | 值 |
|------|-----|
| 展现次数 | {num(fs.get('revealCnt'))} |
| 浏览量(PV) | {num(fs.get('pv'))} |
| 访客数(UV) | {num(fs.get('uv'))} |
| 点击转化率 | {s(fs.get('clickRate', '—'))}% |
| 询盘人数 | {num(inv.get('effectiveInQUsers'))} |
| 询盘率 | {pct(inv.get('effectiveInQUsers')/fs.get('uv')) if fs.get('uv') and inv.get('effectiveInQUsers') is not None and float(fs.get('uv', 0)) > 0 else '—'} |
| 无线端访客占比 | {pct(fs.get('mobileShare'))} |
| 跳失率 | {pct(fs.get('bounceRate'))} |
| 人均浏览量 | {s(fs.get('avgPvs'))} |

---

## 三、交易数据

| 字段 | 值 |
|------|-----|
| 支付金额 | {rmb(pay_amt)} |
| 支付订单数 | {num(trade.get('payMordCnt'))} |
| 支付买家数 | {num(trade.get('payByrCnt'))} |
| 支付商品件数 | {num(trade.get('payItemQty'))} |
| 支付转化率 | {pct(trade.get('payRate'))} |
| 客单价 | {rmb(trade.get('perByrAmt'))} |
| 退款金额 | {rmb(trade.get('rfdSucAmt'))} |
| 退款订单数 | —（插件未采集） |
| 整体退款率 | {pct(trade.get('refundRate'))} |

---

## 四、客户结构数据

| 字段 | 值 |
|------|-----|
| 支付新买家数 | {num(trade.get('payNewByrCnt'))} |
| 新买家支付金额 | {rmb(new_amt)} |
| 新客成交占比 | {pct(trade.get('newBuyerShare'))} |
| 老买家支付金额 | {rmb(old_amt)} |
| 支付老买家数 | {num(trade.get('payOldByrCnt'))} |
| 老客复购率 | {pct(trade.get('oldBuyerShare'))} |
| 老客客单价 | {rmb(trade.get('oldBuyerPerAmt'))} |

---

## 五、付费投放数据

| 字段 | 值 |
|------|-----|
| 广告总消耗 | —（插件未采集数字营销数据） |
| 广告引导GMV | — |
| 推广ROI | — |
| 付费成交占比 | — |

---

## 六、新灯塔履约表现

| 字段 | 值 | 同行平均 | 同行优秀 |
|------|-----|----------|----------|
| 新灯塔综合总分 | {s(nlh.get('score'))}（{s(nlh.get('title'))}） | — | — |
| 3分钟响应率 | {s(wr.get('display'))}% | {s(wr.get('averageScore'))} | {s(wr.get('excellentScore'))} |
| 咨询满意度 | {s(wsf.get('display'))}% | {s(wsf.get('averageScore'))} | {s(wsf.get('excellentScore'))} |
| 48H揽收率 | {s(l48.get('display'))}% | {s(l48.get('averageScore'))} | {s(l48.get('excellentScore'))} |
| 履约率 | {s(lfr.get('display'))}% | {s(lfr.get('averageScore'))} | {s(lfr.get('excellentScore'))} |
| 物流时效达成率 | {s(lpa.get('display'))}% | {s(lpa.get('averageScore'))} | {s(lpa.get('excellentScore'))} |
| 72H支签率 | {s(l72.get('display'))}% | {s(l72.get('averageScore'))} | {s(l72.get('excellentScore'))} |
| 品质退款率 | {s(qr.get('display'))}% | {s(qr.get('averageScore'))} | {s(qr.get('excellentScore'))} |

---

## 七、入店来源（近7天：{s(fs7.get('dateRange'))}）

"""

    sources = fs7.get('sources', [])
    if sources:
        report += "| 渠道名称 | 访客数 | 引导下单数 | 引导支付金额 |\n|----------|--------|-----------|-------------|\n"
        for src in sources:
            report += f"| {s(src.get('name'))} | {s(src.get('myUv', 0))} | — | — |\n"
    else:
        if fs7.get('dateRange'):
            report += "1688数据为空（该店铺近7天无流量来源数据）。\n"
        else:
            report += "插件未采集到近7天流量来源数据。\n"

    report += f"""
---

## 八、入店关键词（近7天）

"""
    kw7 = sycm.get('keywordsRecent7')
    if kw7 and kw7.get('keywords'):
        report += "| 关键词 | 展现数 | 访客数 | 引导支付金额 |\n|--------|--------|--------|-------------|\n"
        for kw in kw7['keywords'][:10]:
            report += f"| {s(kw.get('keyword'))} | {s(kw.get('keywordRevealCnt', 0))} | {s(kw.get('uv', 0))} | ¥{rmb(kw.get('leadPayAmt'))} |\n"
    elif kw7:
        report += "1688数据为空（该店铺近7天无入店关键词数据）。\n"
    else:
        report += "插件未采集到入店关键词数据（该店铺可能无足够流量数据）。\n"

    report += f"""
---

## 九、排名趋势（30天）

**当前排名：** 第{s(rt.get('rank'))}名 | **层级：** 第{s(rt.get('layer'))}层
**类目：** {s(rt.get('cateLevel1'))} > {s(rt.get('cateLevel2'))}

"""

    raw_ranks = rt.get('rawRanks', [])
    if raw_ranks and len(raw_ranks) > 0:
        report += f"**30天排名：** {raw_ranks[0]} → {raw_ranks[-1]}"
        if raw_ranks[-1] < raw_ranks[0]:
            report += "（↑ 上升）\n"
        elif raw_ranks[-1] > raw_ranks[0]:
            report += "（↓ 下降）\n"
        else:
            report += "（→ 持平）\n"

    # 数据小结
    summary_sections = build_summary(sycm, work)
    report += "\n---\n\n## 十、数据小结\n\n"
    for title, content in summary_sections:
        report += f"### 🏷️ {title}\n\n{content}\n\n"

    report += f"""---

*数据来源：1688 Data Claw 插件 v1.0.0 | 生成时间：{now_str}*
*注：标注"插件未采集"的数据项需通过其他渠道获取（如数字营销后台、生意参谋其他模块）。*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return report


# ============================================================
# CLI 入口
# ============================================================

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_report.py <raw_data.json> [output.md]", file=sys.stderr)
        print("  默认输出: <skill_dir>/../1688_daily_report.md", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    with open(input_path, encoding='utf-8') as f:
        raw_data = json.load(f)

    report = generate_report(raw_data, output_path)
    print(f"✅ 日报已生成: {output_path} ({len(report)} bytes)")