#!/usr/bin/env python3
"""
1688 日报生成脚本 v3 — Markdown 表格格式
参考 example.md 模板：emoji 标题 + markdown 表格

用法：
  python3 generate_report_v3.py <raw_data.json> [output.md]
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
DEFAULT_OUTPUT = str(SKILL_DIR / '1688_daily_report_v3.md')
DEFAULT_FEISHU_OUTPUT = str(SKILL_DIR / '1688_daily_report_v3_feishu.txt')


# ===================== 工具函数 =====================

def s(v, default='—'):
    if v is None:
        return default
    return str(v)


def pct(v):
    """小数(0~1) → 百分数"""
    if v is None:
        return '—'
    try:
        return f'{round(float(v) * 100, 1)}%'
    except Exception:
        return str(v)


def pct_raw(v):
    """百分数(已经是百分数值) → 百分数字符串"""
    if v is None:
        return '—'
    try:
        return f'{round(float(v), 1)}%'
    except Exception:
        return str(v)


def rmb(v):
    if v is None:
        return '—'
    try:
        f = float(v)
        if f == int(f):
            return f'¥{int(f):,}'
        return f'¥{f:,.2f}'
    except Exception:
        return f'¥{v}'


def num(v):
    if v is None:
        return '—'
    return str(v)


def trend_str(raw_ranks):
    """根据 rawRanks 列表首尾值生成趋势箭头字符串
    排名数字变小 = 排名提升 → ⬆
    排名数字变大 = 排名下降 → ⬇
    持平 → →
    """
    if not raw_ranks or len(raw_ranks) < 2:
        return ''
    try:
        first, last = int(raw_ranks[0]), int(raw_ranks[-1])
    except Exception:
        return ''
    delta = abs(last - first)
    if delta == 0:
        return ' →持平'
    if last < first:
        return f' ⬆{delta}'
    return f' ⬇{delta}'


def md_to_feishu_text(md_text):
    """将 markdown 报告转换为飞书友好的纯文本格式。
    飞书 text 消息不支持 markdown 表格语法 (`|...|...|`)，会被当代码块渲染。
    转换规则：
      - 2 列表格（key-value 结构）→  • key：value
      - 多列表格（排名/列表结构）  →  1. col1｜col2｜col3
      - 其余内容（标题/段落/列表）保留原样
    """
    lines = md_text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 检测表格起始：行首和行中均含 |
        if stripped.startswith('|') and stripped.endswith('|') and stripped.count('|') >= 3:
            # 收集整张表
            tbl = []
            while i < len(lines):
                t = lines[i].strip()
                if t.startswith('|') and t.endswith('|') and t.count('|') >= 3:
                    tbl.append(t)
                    i += 1
                else:
                    break
            # 解析表格
            parsed = []
            for row in tbl:
                cells = [c.strip() for c in row.strip('|').split('|')]
                parsed.append(cells)
            if len(parsed) < 2:
                continue
            # 跳过表头分隔行（|---|---|...）
            header = parsed[0]
            data_rows = parsed[1:]
            if data_rows and all(set(c) <= set('-:') for c in data_rows[0]):
                data_rows = data_rows[1:]
            # 转换
            if len(header) == 2:
                # key-value 表格
                for row in data_rows:
                    if len(row) >= 2 and (row[0] or row[1]):
                        out.append(f'• {row[0]}：{row[1] if row[1] else "—"}')
            else:
                # 多列排名/列表表格：不加额外序号（表头首列通常已是排名）
                for row in data_rows:
                    cells = [c for c in row if c]
                    if cells:
                        out.append('｜'.join(cells))
            out.append('')
            continue

        out.append(line)
        i += 1

    # 清理连续空行（>2 个合并为 1 个）
    cleaned = []
    blank_count = 0
    for ln in out:
        if ln == '':
            blank_count += 1
            if blank_count <= 1:
                cleaned.append(ln)
        else:
            blank_count = 0
            cleaned.append(ln)
    return '\n'.join(cleaned).strip() + '\n'


# ===================== 主函数 =====================

def build_report(raw_data):
    data = raw_data.get('data', {})
    sycm_list = data.get('sycm', [])
    work_list = data.get('work', [])

    sycm = sycm_list[-1] if sycm_list else {}
    work = work_list[-1] if work_list else {}

    today = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
    now = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

    # ----- 字段提取 -----
    item = sycm.get('itemOverview', {})
    fs = sycm.get('flowStats', {})
    inv = sycm.get('inquiry', {})
    trade = sycm.get('trade', {})
    rt = sycm.get('rankTrend', {})
    fs7 = sycm.get('flowSourceRecent7', {})
    kw7 = sycm.get('keywordsRecent7', {})
    trade7 = sycm.get('tradeRecent7', {})

    nlh = work.get('nlhScore', {})
    wr = work.get('wwResponse', {})
    l48 = work.get('lgt48hGotRate', {})
    lpa = work.get('lgtPlanAccRate', {})
    qr = work.get('qualityRfdRate', {})

    # ----- 基础数值 -----
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
    pay_rate = trade.get('payRate')
    per_byr_amt = trade.get('perByrAmt')
    rfd_amt = trade.get('rfdSucAmt')
    refund_rate = trade.get('refundRate')

    new_byr = trade.get('payNewByrCnt')
    new_amt = trade.get('newBuyerAmt')
    new_share = trade.get('newBuyerShare')
    old_byr = trade.get('payOldByrCnt')
    old_per_amt_raw = trade.get('oldBuyerPerAmt')
    old_share = trade.get('oldBuyerShare')

    # ----- 派生 -----
    # 老客成交金额 = 支付GMV - 新客成交金额
    old_amt = None
    if pay_amt is not None and new_amt is not None:
        try:
            old_amt = float(pay_amt) - float(new_amt)
        except Exception:
            old_amt = None

    # 复购率 = 老客成交占比（trade.oldBuyerShare，0~1 小数，与 v2 一致）
    # 注：v2 用 oldBuyerShare（金额占比），v3 之前误用 old_byr/pay_byr（买家数占比），
    # 两个数数学上不等；按运营语义"复购率"= 老客金额占比更稳
    if old_share is not None:
        repurchase_rate = pct(float(old_share))
    else:
        repurchase_rate = '—'

    # 新客客单价 = 新客金额 / 新客买家数
    if new_amt is not None and new_byr is not None and float(new_byr) > 0:
        new_per_amt = rmb(float(new_amt) / float(new_byr))
    else:
        new_per_amt = '—'

    # 老客客单价：优先用 trade.oldBuyerPerAmt；否则 old_amt / old_byr
    if old_per_amt_raw is not None:
        old_per_amt = rmb(old_per_amt_raw)
    elif old_amt is not None and old_byr is not None and float(old_byr) > 0:
        old_per_amt = rmb(old_amt / float(old_byr))
    else:
        old_per_amt = '—'

    # ----- 排名 -----
    rank = rt.get('rank')
    layer = rt.get('layer')
    rank_str = f'{layer}层级{rank}名' if (rank is not None and layer is not None) else '—'
    rank_trend = trend_str(rt.get('rawRanks', []))

    # ----- 类目 -----
    cate1 = rt.get('cateLevel1') or sycm.get('category') or work.get('cateLvl1Name', '—')
    cate2 = rt.get('cateLevel2') or sycm.get('subCategory', '—')

    # ----- 动销率 -----
    if ic and ps is not None and float(ic) > 0:
        dongxiao = pct(float(ps) / float(ic))
    else:
        dongxiao = '0%'

    # ----- 流量 -----
    raw_click_rate = fs.get('clickRate')
    click_rate_display = pct(raw_click_rate)
    avg_pvs = s(fs.get('avgPvs'))

    if inquiry_count is not None and uv and float(uv) > 0:
        inquiry_rate = pct(float(inquiry_count) / float(uv))
    else:
        inquiry_rate = '—'
    inquiry_pct_display = f'{inquiry_count}人/{inquiry_rate}'

    bounce_display = pct(bounce)

    if mobile_share is None:
        mobile_pct = '—'
    else:
        try:
            # mobileShare 是 0~1 小数（与 clickRate / bounceRate / payRate 等口径一致），
            # 必须用 pct() ×100，绝不能用 pct_raw()，否则会被缩小 100 倍
            mobile_pct = pct(float(mobile_share))
        except Exception:
            mobile_pct = str(mobile_share)

    # ----- 交易 -----
    pay_amt_str = rmb(pay_amt)
    pay_rate_str = pct(pay_rate)
    unit_price = rmb(per_byr_amt)
    refund_pct = pct(refund_rate)
    if pay_amt and rfd_amt is not None and float(pay_amt) > 0:
        refund_ratio = pct(float(rfd_amt) / float(pay_amt))
    else:
        refund_ratio = '0%'

    # ----- 新老客字段 -----
    new_amt_str = rmb(new_amt)
    new_byr_str = num(new_byr)
    if new_share is not None:
        new_share_str = pct(new_share)
    elif pay_amt and new_amt is not None and float(pay_amt) > 0:
        new_share_str = pct(float(new_amt) / float(pay_amt))
    else:
        new_share_str = '—'

    old_amt_str = rmb(old_amt) if old_amt is not None else '—'
    old_byr_str = num(old_byr)
    old_share_str = pct(old_share) if old_share is not None else '—'

    # ----- 新灯塔 -----
    nlh_score = nlh.get('score', '—')
    nlh_title = nlh.get('title', '')
    nlh_line = f'{nlh_score}（{nlh_title}）' if nlh_title else f'{nlh_score}'

    wr_display = s(wr.get('display'))
    l48_display = s(l48.get('display'))
    lpa_display = s(lpa.get('display'))
    qr_display = s(qr.get('display'))

    # ----- TOP8 流量渠道 -----
    sources = fs7.get('sources', [])
    # 占比分母：与 v2 一致用 trade7.payAmt（7天支付 GMV），
    # 而不是 fs7.totalFleadPayAmt（SKILL.md 未定义该字段，插件可能没采到）
    near7_total_pay = trade7.get('payAmt', 0) or 0

    sources_table_rows = []
    if sources:
        # 与 v2 一致：只取二级渠道（outerLevel == '2'），按访客降序，
        # uv 字段缺失时 fallback 到 myUv
        l2 = [src for src in sources if src.get('outerLevel') == '2' or src.get('outerLevel') == 2]
        sorted_sources = sorted(
            l2,
            key=lambda x: x.get('uv', x.get('myUv', 0)),
            reverse=True,
        )
        for i, src in enumerate(sorted_sources[:8]):
            uv_val = src.get('uv', 0) or 0
            pay_amt_src = src.get('fleadPayAmt', 0) or 0
            if near7_total_pay and float(near7_total_pay) > 0:
                pay_ratio = pct(float(pay_amt_src) / float(near7_total_pay))
            else:
                pay_ratio = '—'
            sources_table_rows.append(
                f'|{i+1}|{src.get("name", "—")}|{uv_val}|{rmb(pay_amt_src)}|{pay_ratio}|'
            )
    sources_table = '\n'.join(sources_table_rows) if sources_table_rows else '|—|无数据|—|—|—|'

    # ----- TOP10 关键词 -----
    keywords = kw7.get('keywords', [])
    keywords_table_rows = []
    if keywords:
        sorted_kw = sorted(
            keywords,
            key=lambda x: (x.get('keywordRevealCnt', 0) or 0),
            reverse=True,
        )
        for i, kw in enumerate(sorted_kw[:10]):
            reveal_cnt = kw.get('keywordRevealCnt', 0) or 0
            uv_val = kw.get('uv', 0) or 0
            click_rate = kw.get('clickRate', 0) or 0
            keywords_table_rows.append(
                f'|{i+1}|{kw.get("keyword", "—")}|{reveal_cnt}|{uv_val}|{pct(click_rate)}|'
            )
    keywords_table = '\n'.join(keywords_table_rows) if keywords_table_rows else '插件未采集到该字段'

    # ----- 数据诊断占位符（由模型填充：覆盖 数据诊断 + 明日工作清单 两段） -----
    diagnostics_placeholder = '[模型生成]'

    # ===================== 组装报告 =====================
    report = f"""# 📊1688运营日报｜{today}
店铺：{s(sycm.get('companyName'))}｜{s(cate1)}>{s(cate2)}
层级：{rank_str}{rank_trend}

## 📦商品基础
|指标|数据|
|----|----|
|在线商品|{num(ic)}款|
|动销商品|{num(ps)}款|
|动销率|{dongxiao}|

## 📈流量数据
|指标|数据|
|----|----|
|总展现|{num(reveal)}|
|访客UV|{num(uv)}|
|浏览PV|{num(pv)}|
|人均浏览|{avg_pvs}页|
|点击转化|{click_rate_display}|
|询盘|{inquiry_pct_display}|
|跳失率|{bounce_display}|
|无线访客占比|{mobile_pct}|

## 💰交易售后
|指标|数据|
|----|----|
|支付GMV|{pay_amt_str}|
|支付订单|{num(pay_mord)}单|
|支付买家|{num(pay_byr)}人|
|支付转化|{pay_rate_str}|
|客单价|{unit_price}|
|退款|{rmb(rfd_amt)}/{refund_pct}|
|退款占比|{refund_ratio}|

## 👥新老客结构
|类型|成交金额|买家数|成交占比|复购率|客单价|
|----|----|----|----|----|----|
|新客|{new_amt_str}|{new_byr_str}人|{new_share_str}|—|{new_per_amt}|
|老客|{old_amt_str}|{old_byr_str}人|{old_share_str}|{repurchase_rate}|{old_per_amt}|

## ⭐新灯塔履约
|指标|数据|
|----|----|
|综合分|{nlh_line}|
|3分钟响应|{wr_display}%|
|48H揽收|{l48_display}%|
|物流时效|{lpa_display}%|
|品质退款率|{qr_display}%|

## 🛤TOP8流量渠道
|排名|渠道|访客|成交金额|支付占比|
|----|----|----|----|----|
{sources_table}

## 🔎TOP10关键词
|排名|关键词|展现|访客|点击率|
|----|----|----|----|----|
{keywords_table}

## ⚠数据诊断
{diagnostics_placeholder}

## ✅今日工作清单
{diagnostics_placeholder}

---
*1688 Data Claw v1.0.0 | {now}*
"""
    return report


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='1688 日报生成 v3（Markdown 表格 + 飞书文本）')
    ap.add_argument('input', help='原始数据 JSON 路径')
    ap.add_argument('output', nargs='?', default=DEFAULT_OUTPUT, help='Markdown 报告输出路径')
    ap.add_argument('--feishu', default=DEFAULT_FEISHU_OUTPUT, help='飞书文本版输出路径（默认同目录下 _feishu.txt）')
    ap.add_argument('--no-feishu', action='store_true', help='不生成飞书文本版')
    args = ap.parse_args()

    with open(args.input, encoding='utf-8') as f:
        raw_data = json.load(f)

    report = build_report(raw_data)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ Markdown 版: {args.output} ({len(report)} bytes)")

    if not args.no_feishu:
        feishu_text = md_to_feishu_text(report)
        with open(args.feishu, 'w', encoding='utf-8') as f:
            f.write(feishu_text)
        print(f"✅ 飞书文本版: {args.feishu} ({len(feishu_text)} bytes)")
