#!/usr/bin/env python3
"""
A股智能看板 - 专业分析师版
整合 a-share-stock-dossier 专业分析框架
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import subprocess
import json

# ============ 页面配置 ============
st.set_page_config(
    page_title="A股智能看板",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ 数据获取 ============

SNAPSHOT_SCRIPT = "/home/c1/.openclaw/workspace/skills/a-share-stock-dossier/scripts/a_share_snapshot.py"

def fetch_via_script(codes, with_indices=True, with_kline=True):
    cmd = ["python3", SNAPSHOT_SCRIPT, "--codes", ",".join(codes)]
    if with_kline:
        cmd.extend(["--with-kline", "--kline-days", "60"])
    if with_indices:
        cmd.append("--with-indices")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def get_stock_pool():
    """预设股票池"""
    codes = [
        "600519", "000858", "000001", "600036", "601318",
        "600276", "000333", "002415", "300750", "603259",
        "002149", "603618", "002475", "002714", "600887",
        "601166", "601398", "601288", "600030", "601211",
        "000002", "600048", "001979", "600585", "601668",
    ]
    return fetch_via_script(codes)

# ============ 专业分析报告生成 ============

def generate_professional_report(stock, kline_data=None, indices=None, sector_data=None):
    """
    生成专业分析师级别报告
    整合 a-share-stock-dossier 分析框架
    """
    name = stock.get("name", "")
    code = stock.get("code", "")
    price = stock.get("last", 0)
    change_pct = stock.get("pct", 0)
    turnover = stock.get("turnover", 0)
    pe = stock.get("pe_ttm", 0)
    volume_ratio = stock.get("volume_ratio", 0)
    amplitude = stock.get("amplitude", 0)
    volume = stock.get("volume", 0)
    amount = stock.get("amount", 0)
    high = stock.get("high", 0)
    low = stock.get("low", 0)
    open_price = stock.get("open", 0)
    prev_close = stock.get("prev_close", 0)
    
    market_drop = indices[0].get("pct", 0) if indices else 0
    market_name = indices[0].get("name", "") if indices else "大盘"
    
    report = {
        "检索纪要": [],
        "公司定位": "",
        "市场叙事": "",
        "板块阶段": "",
        "技术面": [],
        "舆情事件": [],
        "产业逻辑": {"状态": "待判断", "理由": []},
        "交易逻辑": {"状态": "待判断", "理由": []},
        "明日情景": [],
        "证据绑定": [],
        "置信度": 0,
        "组合评级": "C",
        "操作建议": "",
    }
    
    # ===== 检索纪要 S1 =====
    report["检索纪要"].append({
        "步骤": "S1",
        "目标": "获取结构化行情数据",
        "来源": "东方财富API",
        "摘要": f"{name} 现价{price:.2f}, 涨跌{change_pct:+.2f}%, 换手{turnover:.2f}%, PE{pe:.1f}",
        "等级": "官方数据",
    })
    
    # ===== 公司业务定位 =====
    # 基于股票代码/名称推断行业
    industry_map = {
        "贵州茅台": "白酒龙头，高端消费，品牌护城河极深",
        "五粮液": "白酒次龙头，千元价格带，浓香型代表",
        "平安银行": "股份制银行，零售转型，财富管理",
        "招商银行": "股份制银行龙头，零售之王，资产质量优",
        "中国平安": "综合金融集团，保险+银行+投资",
        "恒瑞医药": "创新药龙头，肿瘤药领先，研发投入高",
        "美的集团": "家电龙头，白电+小家电，全球化布局",
        "海康威视": "安防龙头，AI视觉，全球份额第一",
        "宁德时代": "动力电池全球龙头，储能第二曲线",
        "药明康德": "CXO龙头，医药外包，全球化",
        "西部材料": "钛材龙头，军工+航空航天材料",
        "杭电股份": "电线电缆，电网投资受益",
        "立讯精密": "消费电子代工，苹果链龙头",
        "牧原股份": "生猪养殖龙头，成本优势明显",
        "伊利股份": "乳制品龙头，常温奶市占率第一",
        "兴业银行": "股份制银行，绿色金融特色",
        "工商银行": "国有大行龙头，规模最大",
        "农业银行": "国有大行，县域网络优势",
        "中信证券": "券商龙头，投行+资管",
        "国泰君安": "大型券商，综合金融服务",
    }
    report["公司定位"] = industry_map.get(name, f"A股上市公司，需进一步研究业务结构")
    
    # ===== 市场叙事阶段 =====
    if change_pct > 5:
        report["市场叙事"] = "🔥 强势上涨阶段，市场关注度高"
    elif change_pct > 0:
        report["市场叙事"] = "📊 温和上涨，趋势向好"
    elif change_pct > market_drop:
        report["市场叙事"] = "🛡️ 抗跌阶段，资金有承接"
    elif change_pct < -5:
        report["市场叙事"] = "📉 大跌阶段，情绪恐慌"
    else:
        report["市场叙事"] = "📊 震荡整理，方向不明"
    
    # ===== 技术面分析 =====
    report["技术面"].append(f"━━━ 价格结构 ━━━")
    report["技术面"].append(f"今开 {open_price:.2f} | 最高 {high:.2f} | 最低 {low:.2f} | 昨收 {prev_close:.2f}")
    report["技术面"].append(f"振幅 {amplitude:.2f}% | 成交额 {amount/100000000:.2f}亿")
    
    # 量价分析
    if volume_ratio > 2:
        report["技术面"].append(f"🔥 量比 {volume_ratio:.2f}，显著放量，资金活跃")
    elif volume_ratio > 1:
        report["技术面"].append(f"✅ 量比 {volume_ratio:.2f}，温和放量")
    else:
        report["技术面"].append(f"⚠️ 量比 {volume_ratio:.2f}，成交萎缩")
    
    # 均线分析
    if kline_data and len(kline_data) >= 20:
        closes = [float(k[2]) for k in kline_data[-60:]]
        ma5 = sum(closes[-5:]) / 5
        ma10 = sum(closes[-10:]) / 10
        ma20 = sum(closes[-20:]) / 20
        ma60 = sum(closes[-40:]) / 40 if len(closes) >= 40 else ma20
        
        report["技术面"].append(f"━━─ 均线系统 ─━━")
        report["技术面"].append(f"MA5: {ma5:.2f} | MA10: {ma10:.2f} | MA20: {ma20:.2f} | MA60: {ma60:.2f}")
        
        if price > ma5 > ma10 > ma20:
            report["技术面"].append(f"✅ 完美多头排列，趋势向上")
        elif price > ma5 and price > ma10:
            report["技术面"].append(f"📊 站上短期均线，偏强")
        elif price < ma5 < ma10 < ma20:
            report["技术面"].append(f"❌ 空头排列，趋势向下")
        else:
            report["技术面"].append(f"📊 均线交织，震荡格局")
        
        # 关键位
        high_20 = max(closes[-20:])
        low_20 = min(closes[-20:])
        report["技术面"].append(f"━━─ 关键位 ─━━")
        report["技术面"].append(f"上方压力: {high_20:.2f} (20日高点)")
        report["技术面"].append(f"下方支撑: {low_20:.2f} (20日低点)")
        report["技术面"].append(f"失效位: {low_20 * 0.97:.2f} (跌破则止损)")
    
    # ===== 产业逻辑判断 =====
    industry_score = 50
    industry_reasons = []
    
    # PE估值
    if pe > 0:
        if pe < 15:
            industry_score += 20
            industry_reasons.append(f"✅ PE {pe:.1f}倍，估值低，安全边际高")
        elif pe < 25:
            industry_score += 10
            industry_reasons.append(f"✅ PE {pe:.1f}倍，估值合理")
        elif pe < 40:
            industry_reasons.append(f"⚠️ PE {pe:.1f}倍，估值偏高")
            industry_score -= 5
        else:
            industry_reasons.append(f"❌ PE {pe:.1f}倍，估值过高")
            industry_score -= 15
    
    # 换手率（流动性）
    if turnover > 2:
        industry_reasons.append(f"✅ 换手率 {turnover:.1f}%，流动性充足")
    else:
        industry_reasons.append(f"⚠️ 换手率 {turnover:.1f}%，流动性偏低")
    
    report["产业逻辑"]["理由"] = industry_reasons
    if industry_score >= 60:
        report["产业逻辑"]["状态"] = "✅ 在"
    elif industry_score >= 40:
        report["产业逻辑"]["状态"] = "⚠️ 弱化"
    else:
        report["产业逻辑"]["状态"] = "❌ 失效"
    
    # ===== 交易逻辑判断 =====
    trade_score = 50
    trade_reasons = []
    
    # 相对大盘表现
    if change_pct > 0 and market_drop < 0:
        trade_score += 20
        trade_reasons.append(f"✅ 逆势上涨 {change_pct:+.1f}%，强于大盘")
    elif change_pct > market_drop:
        trade_score += 10
        trade_reasons.append(f"✅ 相对抗跌，跑赢大盘 {change_pct - market_drop:.1f}%")
    elif change_pct < market_drop:
        trade_score -= 10
        trade_reasons.append(f"❌ 弱于大盘 {change_pct - market_drop:.1f}%")
    
    # 量价配合
    if change_pct > 0 and volume_ratio > 1:
        trade_score += 10
        trade_reasons.append(f"✅ 放量上涨，量价配合")
    elif change_pct < 0 and volume_ratio > 2:
        trade_score -= 10
        trade_reasons.append(f"⚠️ 放量下跌，可能有资金出逃")
    
    report["交易逻辑"]["理由"] = trade_reasons
    if trade_score >= 60:
        report["交易逻辑"]["状态"] = "✅ 在"
    elif trade_score >= 40:
        report["交易逻辑"]["状态"] = "⚠️ 弱化"
    else:
        report["交易逻辑"]["状态"] = "❌ 失效"
    
    # ===== 明日三情景 =====
    strong_trigger = high * 1.02
    weak_trigger = low * 0.98
    
    report["明日情景"] = [
        {
            "情景": "强势",
            "触发": f"放量突破 {strong_trigger:.2f}",
            "动作": "持有/加仓",
        },
        {
            "情景": "中性",
            "触发": f"区间震荡 {low_20:.2f} - {high_20:.2f}",
            "动作": "持有观望",
        },
        {
            "情景": "弱势",
            "触发": f"跌破 {weak_trigger:.2f}",
            "动作": "止损离场",
        },
    ]
    
    # ===== 证据绑定 =====
    report["证据绑定"].append({
        "编号": "E1",
        "内容": f"东方财富行情: {name} 现价{price:.2f}，涨跌{change_pct:+.2f}%",
        "来源": "官方",
        "可信度": "高",
    })
    report["证据绑定"].append({
        "编号": "E2",
        "内容": f"估值数据: PE {pe:.1f}倍",
        "来源": "东财TTM",
        "可信度": "高",
    })
    if kline_data:
        report["证据绑定"].append({
            "编号": "E3",
            "内容": f"K线数据: 20日高点{high_20:.2f}, 低点{low_20:.2f}",
            "来源": "腾讯行情",
            "可信度": "高",
        })
    
    # ===== 置信度 =====
    confidence = 50
    if pe > 0: confidence += 15
    if kline_data: confidence += 15
    if turnover > 1: confidence += 10
    report["置信度"] = min(100, confidence)
    
    # ===== 组合评级 =====
    if industry_score >= 60 and trade_score >= 60:
        report["组合评级"] = "A"
        report["操作建议"] = "产业逻辑与交易逻辑同向，可重点配置"
    elif industry_score >= 40 and trade_score >= 40:
        report["组合评级"] = "B"
        report["操作建议"] = "逻辑尚在但偏弱，轻仓观察"
    else:
        report["组合评级"] = "C"
        report["操作建议"] = "逻辑受损，建议规避"
    
    return report

# ============ 缓存 ============

@st.cache_data(ttl=300)
def get_data():
    return get_stock_pool()

# ============ 侧边栏 ============

st.sidebar.title("📈 A股智能看板")
st.sidebar.caption(f"更新: {datetime.now().strftime('%H:%M')}")

tab = st.sidebar.radio("功能", [
    "📊 组合分析",
    "📉 大跌选股", 
    "🎣 抄底候选",
    "🔍 单股深挖",
], label_visibility="collapsed")

# ============ 主内容 ============

st.title(tab)

# Tab 1: 组合分析
if tab == "📊 组合分析":
    if st.button("🔄 刷新数据", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    with st.spinner("正在获取数据..."):
        data = get_data()
    
    if data:
        # 市场底色
        st.subheader("📈 市场底色")
        indices = data.get("indices", [])
        if indices:
            cols = st.columns(len(indices))
            for i, idx in enumerate(indices):
                with cols[i]:
                    pct = idx.get("pct", 0)
                    icon = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
                    st.metric(
                        idx.get("name", ""),
                        f"{idx.get('last', 0):.2f}",
                        f"{icon} {pct:+.2f}%"
                    )
            
            # 市场强度
            up_count = indices[0].get("up_count", 0) if indices else 0
            down_count = indices[0].get("down_count", 0) if indices else 0
            if up_count + down_count > 0:
                st.caption(f"上涨 {up_count} 家 vs 下跌 {down_count} 家")
        
        st.divider()
        
        quotes = data.get("quotes", [])
        if quotes:
            # 生成报告
            reports = []
            for q in quotes:
                kline = data.get("kline", {}).get(q.get("code", ""), {}).get("klines", [])
                report = generate_professional_report(q, kline, indices)
                report["原始数据"] = q
                reports.append(report)
            
            # 按评级排序
            order = {"A": 0, "B": 1, "C": 2}
            reports.sort(key=lambda x: order.get(x["组合评级"], 3))
            
            # 分组显示
            st.subheader("📋 组合分层")
            
            for grade in ["A", "B", "C"]:
                grade_reports = [r for r in reports if r["组合评级"] == grade]
                if grade_reports:
                    grade_icon = "🟢" if grade == "A" else "🟡" if grade == "B" else "🔴"
                    st.markdown(f"### {grade_icon} {grade}级 ({len(grade_reports)} 只)")
                    
                    if grade == "A":
                        st.success("产业逻辑 + 交易逻辑 同向")
                    elif grade == "B":
                        st.warning("逻辑在但偏弱")
                    else:
                        st.error("逻辑受损")
                    
                    for r in grade_reports:
                        q = r["原始数据"]
                        with st.expander(f"**{q.get('name')}** ({q.get('code')}) - {r['组合评级']}级"):
                            # 基本信息
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("现价", f"{q.get('last', 0):.2f}", f"{q.get('pct', 0):+.2f}%")
                            with col2:
                                st.metric("PE", f"{q.get('pe_ttm', 0):.1f}" if q.get('pe_ttm') else "N/A")
                            with col3:
                                st.metric("置信度", f"{r['置信度']}/100")
                            
                            st.divider()
                            
                            # 公司定位
                            st.markdown(f"**📌 公司定位**: {r['公司定位']}")
                            st.markdown(f"**📊 市场叙事**: {r['市场叙事']}")
                            
                            # 双逻辑
                            st.markdown("**── 双逻辑判断 ──**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**产业逻辑**: {r['产业逻辑']['状态']}")
                                for reason in r['产业逻辑']['理由']:
                                    st.write(f"  {reason}")
                            with col2:
                                st.markdown(f"**交易逻辑**: {r['交易逻辑']['状态']}")
                                for reason in r['交易逻辑']['理由']:
                                    st.write(f"  {reason}")
                            
                            # 明日情景
                            st.markdown("**── 明日三情景 ──**")
                            for scene in r['明日情景']:
                                st.write(f"- **{scene['情景']}**: {scene['触发']} → {scene['动作']}")
                            
                            # 操作建议
                            st.divider()
                            st.info(f"💡 **操作建议**: {r['操作建议']}")
                    
                    st.divider()
            
            # 检索纪要汇总
            st.subheader("📝 检索纪要")
            for r in reports[:5]:
                q = r["原始数据"]
                with st.expander(f"{q.get('name')} - 检索过程"):
                    for step in r["检索纪要"]:
                        st.write(f"**{step['步骤']}**: {step['目标']}")
                        st.write(f"  来源: {step['来源']} | 摘要: {step['摘要']}")
        else:
            st.warning("无股票数据")
    else:
        st.error("数据获取失败，请刷新重试")

# Tab 2: 大跌选股
elif tab == "📉 大跌选股":
    if st.button("🔄 刷新数据", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    with st.spinner("正在获取数据..."):
        data = get_data()
    
    if data:
        indices = data.get("indices", [])
        market_drop = indices[0].get("pct", 0) if indices else 0
        
        st.subheader("📊 今日市场")
        if indices:
            cols = st.columns(len(indices))
            for i, idx in enumerate(indices):
                with cols[i]:
                    st.metric(idx.get("name", ""), f"{idx.get('last', 0):.2f}", f"{idx.get('pct', 0):.2f}%")
        
        st.warning(f"📉 {indices[0].get('name', '大盘')}跌幅: {market_drop:.2f}%")
        st.divider()
        
        quotes = data.get("quotes", [])
        if quotes:
            # 逆势上涨
            up_stocks = sorted([q for q in quotes if q.get("pct", 0) > 0], 
                              key=lambda x: x.get("pct", 0), reverse=True)
            if up_stocks:
                st.subheader(f"🔥 逆势上涨 ({len(up_stocks)} 只)")
                for q in up_stocks:
                    kline = data.get("kline", {}).get(q.get("code", ""), {}).get("klines", [])
                    report = generate_professional_report(q, kline, indices)
                    
                    with st.expander(f"**{q.get('name')}** ({q.get('code')}) | 🔴 +{q.get('pct', 0):.1f}% | {report['组合评级']}级"):
                        st.markdown(f"**产业逻辑**: {report['产业逻辑']['状态']}")
                        st.markdown(f"**交易逻辑**: {report['交易逻辑']['状态']}")
                        st.markdown(f"**操作建议**: {report['操作建议']}")
            
            # 抗跌
            resist_stocks = sorted([q for q in quotes if 0 >= q.get("pct", 0) > market_drop],
                                   key=lambda x: x.get("pct", 0), reverse=True)
            if resist_stocks:
                st.subheader(f"🛡️ 抗跌股 ({len(resist_stocks)} 只)")
                for q in resist_stocks[:10]:
                    kline = data.get("kline", {}).get(q.get("code", ""), {}).get("klines", [])
                    report = generate_professional_report(q, kline, indices)
                    
                    with st.expander(f"**{q.get('name')}** ({q.get('code')}) | {q.get('pct', 0):+.1f}% | {report['组合评级']}级"):
                        st.markdown(f"**产业逻辑**: {report['产业逻辑']['状态']}")
                        st.markdown(f"**交易逻辑**: {report['交易逻辑']['状态']}")
                        st.markdown(f"**操作建议**: {report['操作建议']}")
    else:
        st.error("数据获取失败")

# Tab 3: 抄底候选
elif tab == "🎣 抄底候选":
    if st.button("🔄 刷新数据", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    with st.spinner("正在获取数据..."):
        data = get_data()
    
    if data:
        quotes = data.get("quotes", [])
        if quotes:
            # PE合理 + 今日下跌
            bottom_stocks = [q for q in quotes if q.get("pct", 0) < 0 and (q.get("pe_ttm", 0) or 0) > 0 and (q.get("pe_ttm", 0) or 0) < 30]
            bottom_stocks = sorted(bottom_stocks, key=lambda x: x.get("pct", 0))
            
            st.subheader(f"🎣 错杀候选 ({len(bottom_stocks)} 只)")
            st.info("💡 PE<30 + 今日下跌 = 可能被错杀")
            
            for q in bottom_stocks[:15]:
                kline = data.get("kline", {}).get(q.get("code", ""), {}).get("klines", [])
                report = generate_professional_report(q, kline, data.get("indices", []))
                
                with st.expander(f"**{q.get('name')}** ({q.get('code')}) | {q.get('pct', 0):+.1f}% | PE {q.get('pe_ttm', 0):.1f}"):
                    st.markdown(f"**产业逻辑**: {report['产业逻辑']['状态']}")
                    for reason in report['产业逻辑']['理由']:
                        st.write(f"  {reason}")
                    st.markdown(f"**交易逻辑**: {report['交易逻辑']['状态']}")
                    for reason in report['交易逻辑']['理由']:
                        st.write(f"  {reason}")
                    st.divider()
                    st.markdown(f"**操作建议**: {report['操作建议']}")
    else:
        st.error("数据获取失败")

# Tab 4: 单股深挖
elif tab == "🔍 单股深挖":
    code = st.text_input("输入股票代码", placeholder="例如: 600519")
    
    if st.button("生成专业报告", type="primary") and code:
        with st.spinner("正在生成专业分析报告..."):
            data = fetch_via_script([code])
        
        if data and data.get("quotes"):
            q = data["quotes"][0]
            kline_data = data.get("kline", {}).get(code, {}).get("klines", [])
            
            report = generate_professional_report(q, kline_data, data.get("indices", []))
            
            # 标题
            st.markdown(f"# 📊 {q.get('name')} ({q.get('code')}) 专业分析报告")
            st.caption(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 置信度: {report['置信度']}/100")
            
            # 评级
            grade_color = "green" if report['组合评级'] == "A" else "orange" if report['组合评级'] == "B" else "red"
            st.markdown(f"### 组合评级: :{grade_color}[{report['组合评级']}级]")
            st.info(f"💡 {report['操作建议']}")
            
            st.divider()
            
            # 检索纪要
            st.markdown("## 📝 一、检索纪要")
            for step in report["检索纪要"]:
                st.markdown(f"**{step['步骤']}**: {step['目标']}")
                st.caption(f"来源: {step['来源']} | 可信度: {step['等级']}")
            
            st.divider()
            
            # 公司定位
            st.markdown("## 🏢 二、公司定位")
            st.write(report['公司定位'])
            st.markdown(f"**市场叙事**: {report['市场叙事']}")
            
            st.divider()
            
            # 技术面
            st.markdown("## 📈 三、技术面分析")
            for line in report['技术面']:
                st.write(line)
            
            # K线图
            if kline_data:
                df = pd.DataFrame(kline_data[-60:], columns=["日期", "开", "收", "高", "低", "量"])
                for col in ["收", "高", "低", "开"]:
                    df[col] = pd.to_numeric(df[col])
                
                fig = go.Figure(data=[
                    go.Candlestick(x=df["日期"], open=df["开"], high=df["高"], low=df["低"], close=df["收"])
                ])
                fig.update_layout(height=400, xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # 双逻辑
            st.markdown("## ⚖️ 四、双逻辑判断")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 产业逻辑: {report['产业逻辑']['状态']}")
                for reason in report['产业逻辑']['理由']:
                    st.write(f"- {reason}")
            with col2:
                st.markdown(f"### 交易逻辑: {report['交易逻辑']['状态']}")
                for reason in report['交易逻辑']['理由']:
                    st.write(f"- {reason}")
            
            st.divider()
            
            # 明日情景
            st.markdown("## 🎯 五、明日三情景")
            for scene in report['明日情景']:
                st.markdown(f"- **{scene['情景']}**: 触发条件 `{scene['触发']}` → {scene['动作']}")
            
            st.divider()
            
            # 证据绑定
            st.markdown("## 🔗 六、证据绑定")
            for ev in report['证据绑定']:
                st.markdown(f"**{ev['编号']}**: {ev['内容']}")
                st.caption(f"来源: {ev['来源']} | 可信度: {ev['可信度']}")
            
            st.divider()
            st.warning("⚠️ 以上分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。")
        else:
            st.error("未找到该股票")

# 页脚
st.sidebar.markdown("---")
st.sidebar.caption("数据: 东方财富")
st.sidebar.caption("框架: a-share-stock-dossier")
st.sidebar.caption("⚠️ 仅供参考")