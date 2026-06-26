#!/usr/bin/env python3
"""
投资研究系统 - 报告生成器
生成结构化的投资决策报告（含财务数据）
"""
from datetime import datetime
from typing import Dict, List
import os
import re

try:
    from config import REPORTS_DIR, VOTE_BUY, VOTE_CAUTION, VOTE_SELL
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import REPORTS_DIR, VOTE_BUY, VOTE_CAUTION, VOTE_SELL


def sanitize_filename(name: str) -> str:
    """
    清洗文件名，移除不安全字符
    仅保留字母、数字、中文、下划线
    """
    # 替换空格和其他不安全字符为下划线
    name = re.sub(r'[^\w\u4e00-\u9fff]', '_', name)
    # 移除连续的下划线
    name = re.sub(r'_+', '_', name)
    # 移除首尾的下划线
    name = name.strip('_')
    return name if name else "unknown"


def generate_report(
    code: str,
    name: str,
    quote: Dict,
    analyst_results: List[Dict],
    final_vote: str,
    final_score: float,
    financial: Dict = None
) -> str:
    """
    生成投资决策报告
    
    Args:
        code: 股票代码
        name: 股票名称
        quote: 行情数据
        analyst_results: 分析师结果
        final_vote: 最终投票
        final_score: 最终得分
        financial: 财务数据
        
    Returns:
        报告文本
    """
    lines = []
    
    # 标题
    lines.append("=" * 60)
    lines.append("        投资研究决策报告")
    lines.append("=" * 60)
    lines.append("")
    
    # 基本信息
    lines.append(f"【标的】：{code} {name}")
    lines.append(f"【研究时间】：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if 'error' not in quote:
        price = quote.get('现价', 'N/A')
        change = quote.get('涨跌幅', 0)
        
        # 格式化价格
        if isinstance(price, (int, float)):
            price_str = f"¥{price:.2f}"
        else:
            price_str = str(price)
        
        # 格式化涨跌幅
        if isinstance(change, (int, float)):
            change_str = f"{change:+.2f}%"
        else:
            change_str = str(change)
        
        lines.append(f"【当前价格】：{price_str} ({change_str})")
        lines.append(f"【数据来源】：{quote.get('source', 'N/A')}")
        
        # 数据来源说明
        if financial and financial.get('data_source'):
            is_estimated = financial.get('is_estimated', True)
            source_note = "⚠️ 部分数据为估算值" if is_estimated else "✅ 数据来源于AKShare真实财报"
            lines.append(f"【财务数据】：{financial.get('data_source')} | {source_note}")
    
    lines.append("")
    
    # 财务数据概览
    if financial:
        lines.append("=" * 60)
        lines.append("        财务数据概览")
        lines.append("=" * 60)
        lines.append("")
        
        fi = financial.get('财务指标', {})
        is_estimated = financial.get('is_estimated', True)
        estimated_note = " (估算)" if is_estimated else ""
        
        if 'error' not in fi:
            lines.append("📊 盈利能力：")
            lines.append(f"   ROE: {fi.get('ROE', 0):.2f}%{estimated_note}  |  毛利率: {fi.get('毛利率', 0):.2f}%{estimated_note}  |  净利率: {fi.get('净利率', 0):.2f}%{estimated_note}")
            lines.append("")
            lines.append("📈 成长能力：")
            lines.append(f"   营收增速: {fi.get('营收增速', 0):.2f}%{estimated_note}  |  利润增速: {fi.get('利润增速', 0):.2f}%{estimated_note}")
            lines.append("")
            lines.append("💰 偿债能力：")
            lines.append(f"   资产负债率: {fi.get('资产负债率', 0):.2f}%  |  流动比率: {fi.get('流动比率', 0):.2f}")
            lines.append("")
        
        ev = financial.get('估值分位', {})
        valuation = financial.get('估值', {})
        if 'error' not in ev or valuation:
            lines.append("💎 估值指标：")
            # 优先使用估值分位数据，否则使用实时估值数据
            pe_val = ev.get('PE当前', 0) or valuation.get('PE_TTM', 0)
            pb_val = ev.get('PB当前', 0) or valuation.get('PB', 0)
            pe_pct = ev.get('PE分位', 0)
            
            if pe_val or pb_val:
                if pe_pct:
                    lines.append(f"   PE: {pe_val:.2f}倍 ({pe_pct}%分位)  |  PB: {pb_val:.2f}倍")
                else:
                    lines.append(f"   PE: {pe_val:.2f}倍  |  PB: {pb_val:.2f}倍")
            
            if 'error' not in valuation:
                div = valuation.get('股息率', 0)
                if div:
                    rating = ev.get('估值评级', '-')
                    lines.append(f"   股息率: {div:.2f}%  |  估值评级: {rating}")
            lines.append("")
        
        industry = financial.get('行业', {})
        if 'error' not in industry:
            lines.append("🏭 行业信息：")
            lines.append(f"   所属行业: {industry.get('行业', '-')}  |  行业涨跌幅: {industry.get('行业涨跌幅', 0):+.2f}%")
            lines.append(f"   行业景气度: {industry.get('行业景气度', '-')}")
            lines.append("")
    
    # 分析师投票结果
    lines.append("=" * 60)
    lines.append("        8位分析师投票结果")
    lines.append("=" * 60)
    lines.append("")
    
    for i, r in enumerate(analyst_results, 1):
        weight_mark = " ⭐" if r['weight'] >= 1.2 else ""
        lines.append(f"{i}. {r['name']} → {r['vote']} 建议 (权重 {r['weight']}x){weight_mark}")
        lines.append(f"   理由：{r['reason']}")
        lines.append("")
    
    # 投票统计
    lines.append("=" * 60)
    lines.append("            投票统计")
    lines.append("=" * 60)
    lines.append("")
    
    buy_count = sum(1 for r in analyst_results if r['vote'] == VOTE_BUY)
    caution_count = sum(1 for r in analyst_results if r['vote'] == VOTE_CAUTION)
    sell_count = sum(1 for r in analyst_results if r['vote'] == VOTE_SELL)
    
    buy_weight = sum(r['weight'] for r in analyst_results if r['vote'] == VOTE_BUY)
    caution_weight = sum(r['weight'] for r in analyst_results if r['vote'] == VOTE_CAUTION)
    sell_weight = sum(r['weight'] for r in analyst_results if r['vote'] == VOTE_SELL)
    
    lines.append(f"{VOTE_BUY} 建议投资：{buy_count}票 (加权得分: {buy_weight:.1f})")
    lines.append(f"{VOTE_CAUTION} 谨慎投资：{caution_count}票 (加权得分: {caution_weight:.1f})")
    lines.append(f"{VOTE_SELL} 不建议投资：{sell_count}票 (加权得分: {sell_weight:.1f})")
    lines.append("")
    
    # 最终结论
    lines.append("=" * 60)
    lines.append("            最终结论")
    lines.append("=" * 60)
    lines.append("")
    
    final_text = {
        VOTE_BUY: "✅ 建议投资",
        VOTE_CAUTION: "⚠️ 谨慎投资",
        VOTE_SELL: "❌ 不建议投资"
    }
    
    lines.append(f"最终建议：{final_text.get(final_vote, final_vote)}")
    lines.append("")
    
    # 综合建议
    lines.append("综合建议：")
    suggestions = _generate_suggestions(final_vote, quote, analyst_results, financial)
    for i, s in enumerate(suggestions, 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    
    # 风险提示
    lines.append("风险提示：")
    risks = _extract_risks(analyst_results)
    for r in risks:
        lines.append(f"- {r}")
    
    lines.append("")
    lines.append("=" * 60)
    
    # 目标价汇总（方案B扩展）
    target_price_section = generate_target_price_summary(quote, financial)
    if target_price_section:
        lines.append(target_price_section)
    
    return "\n".join(lines)


def _generate_suggestions(
    final_vote: str,
    quote: Dict,
    analyst_results: List[Dict],
    financial: Dict = None
) -> List[str]:
    """生成具体建议"""
    suggestions = []
    
    # 获取估值信息
    ev = financial.get('估值分位', {}) if financial else {}
    valuation = financial.get('估值', {}) if financial else {}
    
    if final_vote == VOTE_BUY:
        suggestions.append("当前时点具备投资价值，可考虑建仓")
        
        # 根据估值给出建议
        if 'error' not in ev:
            pe_pct = ev.get('PE分位', 50)
            if pe_pct < 30:
                suggestions.append("估值处于历史低位，具备安全边际，可适当加大仓位")
        
        # 根据股息率给出建议
        if 'error' not in valuation:
            dv = valuation.get('股息率', 0)
            if dv > 4:
                suggestions.append(f"股息率{dv:.1f}%较高，适合长期持有获取分红收益")
        
        suggestions.append("建议分批买入，首次仓位控制在20%以内，设置10%止损线")
        
    elif final_vote == VOTE_CAUTION:
        suggestions.append("当前存在不确定性因素，建议观望")
        suggestions.append("如需参与，仓位控制在10%以内")
        suggestions.append("等待更明确的买入信号（如估值回落、业绩拐点确认）")
        
    else:
        suggestions.append("当前风险大于机会，建议规避")
        suggestions.append("如已持有，考虑减仓或止损")
        suggestions.append("等待更好的入场时机（估值回归、基本面改善）")
    
    return suggestions


def _extract_risks(analyst_results: List[Dict]) -> List[str]:
    """提取风险点"""
    risks = []
    
    for r in analyst_results:
        if r['name'] == "风险控制师":
            reason = r['reason']
            if '波动风险' in reason:
                risks.append("股价波动较大，短期风险较高")
            if '杠杆风险' in reason or '财务杠杆' in reason:
                risks.append("财务杠杆偏高，偿债压力较大")
            if '现金流风险' in reason:
                risks.append("经营现金流为负，需关注资金链安全")
            if '估值偏高' in reason:
                risks.append("估值处于历史高位，回调风险较大")
            if '系统性风险' in reason:
                risks.append("市场系统性风险不可忽视")
    
    # 默认风险提示
    if not risks:
        risks.append("投资有风险，决策需谨慎")
        risks.append("建议分散投资，控制单一标的仓位")
    
    return risks


def generate_target_price_summary(quote: Dict, financial: Dict = None) -> str:
    """
    生成目标价汇总模块（方案B扩展）
    
    Args:
        quote: 行情数据
        financial: 财务数据
        
    Returns:
        目标价汇总文本
    """
    # 获取当前价格
    price = quote.get('现价', 0)
    if isinstance(price, str):
        try:
            price = float(price.replace('¥', '').replace(',', ''))
        except:
            return ""
    
    if price <= 0:
        return ""
    
    # 导入估值分析师计算目标价
    try:
        from analysts import ValuationAnalyst
        analyst = ValuationAnalyst()
        target_info = analyst.calculate_target_prices(quote, financial)
    except Exception as e:
        return ""
    
    if not target_info:
        return ""
    
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("        🎯 目标价指导")
    lines.append("=" * 60)
    lines.append("")
    
    # 价格信息
    lines.append(f"【当前价格】：¥{price:.2f}")
    lines.append(f"【目标价方法】：{target_info.get('method', '综合评估')}")
    lines.append("")
    
    # 目标价表格
    pessimistic = target_info.get('pessimistic', 0)
    neutral = target_info.get('neutral', 0)
    optimistic = target_info.get('optimistic', 0)
    safety_margin = target_info.get('safety_margin', 0)
    
    lines.append("┌─────────────┬───────────┬───────────┐")
    lines.append("│   目标价    │   价格    │  上涨空间  │")
    lines.append("├─────────────┼───────────┼───────────┤")
    
    # 悲观目标价
    pessimistic_change = (pessimistic - price) / price * 100 if price > 0 else 0
    lines.append(f"│  悲观目标价  │ ¥{pessimistic:>7.2f} │ {pessimistic_change:>+6.1f}%  │")
    
    # 中性目标价
    neutral_change = (neutral - price) / price * 100 if price > 0 else 0
    lines.append(f"│  中性目标价  │ ¥{neutral:>7.2f} │ {neutral_change:>+6.1f}%  │")
    
    # 乐观目标价
    optimistic_change = (optimistic - price) / price * 100 if price > 0 else 0
    lines.append(f"│  乐观目标价  │ ¥{optimistic:>7.2f} │ {optimistic_change:>+6.1f}%  │")
    
    lines.append("└─────────────┴───────────┴───────────┘")
    lines.append("")
    
    # 安全边际分析
    if safety_margin > 0:
        margin_status = "✅ 价格低于目标价，具备安全边际"
        advice = "建议：可考虑建仓"
    elif safety_margin > -10:
        margin_status = "⚠️ 价格略高于目标价"
        advice = "建议：持有，等待估值回归"
    else:
        margin_status = "❌ 价格显著高于目标价"
        advice = "建议：等待更好的买入时机"
    
    lines.append(f"📊 当前安全边际：{safety_margin:+.1f}% ({margin_status})")
    lines.append(f"💡 {advice}")
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def save_report(code: str, name: str, report: str) -> str:
    """
    保存报告到文件
    
    Returns:
        保存路径
    """
    date_str = datetime.now().strftime('%Y-%m-%d')
    # 清洗文件名，防止特殊字符
    safe_name = sanitize_filename(name)
    filename = f"{date_str}_{code}_{safe_name}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filepath


if __name__ == "__main__":
    # 测试
    test_results = [
        {'name': '宏观经济分析师', 'weight': 1.0, 'vote': VOTE_BUY, 'reason': '宏观环境稳定'},
        {'name': '行业研究员', 'weight': 1.5, 'vote': VOTE_BUY, 'reason': '行业景气度高'},
        {'name': '基本面分析师', 'weight': 1.5, 'vote': VOTE_CAUTION, 'reason': '基本面一般'},
    ]
    
    report = generate_report(
        '600919',
        '江苏银行',
        {'现价': 11.40, '涨跌幅': 0.35, 'source': 'AKShare'},
        test_results,
        VOTE_BUY,
        0.6
    )
    
    print(report)


# ===========================================
# 个性化投资建议模块
# ===========================================

def generate_personalized_advice(
    code: str,
    name: str,
    quote: Dict,
    financial: Dict,
    analyst_results: List[Dict],
    final_vote: str,
    final_score: float,
    user_profile=None,
    graham_score=None
) -> str:
    """
    生成个性化投资建议（基于用户画像）
    
    Args:
        code: 股票代码
        name: 股票名称
        quote: 行情数据
        financial: 财务数据
        analyst_results: 分析师结果
        final_vote: 最终投票
        final_score: 最终得分
        user_profile: 用户画像
        graham_score: Graham 评分
    
    Returns:
        个性化投资建议文本
    """
    from user_profile import UserProfileLoader, get_user_profile
    from graham_evaluator import evaluate_with_graham
    
    # 加载用户画像
    if user_profile is None:
        loader = UserProfileLoader()
        user_profile = loader.load_profile()
    
    # 获取 Graham 评分
    if graham_score is None:
        graham_score = evaluate_with_graham(code, financial, quote, user_profile)
    
    lines = []
    lines.append("\n" + "="*60)
    lines.append("💡 个性化投资建议（基于用户画像）")
    lines.append("="*60)
    
    # 用户画像
    lines.append(f"\n👤 用户画像：{user_profile.name}")
    lines.append(f"   投资风格：{user_profile.investment_style}")
    lines.append(f"   风险偏好：{user_profile.risk_preference}")
    lines.append(f"   持仓周期：{user_profile.holding_period}")
    lines.append(f"   期望收益率：{user_profile.expected_return}%")
    
    # Graham 价值评估
    lines.append(f"\n📊 Graham 价值评估：")
    lines.append(f"   总分：{graham_score.total_score:.2f} / 1.00")
    lines.append(f"   建议：{graham_score.recommendation}")
    
    if graham_score.reasons:
        lines.append("   评估要点：")
        for reason in graham_score.reasons[:5]:
            lines.append(f"   • {reason}")
    
    # 个性化建议
    lines.append(f"\n🎯 针对 {user_profile.name} 的建议：")
    
    # 根据投资风格给出建议
    if user_profile.investment_style == "价值投资":
        if graham_score.total_score >= 0.6:
            lines.append("   ✅ 该股票符合您的价值投资标准")
            lines.append(f"   📈 建议仓位：{user_profile.max_position*100:.0f}%（{user_profile.holding_type}持有）")
            if user_profile.risk_preference == "保守":
                lines.append("   ⚠️ 建议分批建仓，首次建仓 30%，回调再加仓")
        else:
            lines.append("   ⚠️ 该股票不完全符合价值投资标准")
            lines.append("   💡 可纳入观察池，等待更好的买入时机")
    
    # 根据风险偏好调整建议
    if user_profile.risk_preference == "保守":
        lines.append(f"   🛡️ 止损线：{user_profile.stop_loss*100:.0f}%（严格执行）")
        lines.append("   📉 建议：不要追高，等回调再入")
    elif user_profile.risk_preference == "激进":
        lines.append(f"   📊 止损线：{user_profile.stop_loss*100:.0f}%")
        lines.append("   ⚡ 可以适度追涨，但需设好止损")
    
    # 基于期望收益率
    fi = financial.get('财务指标', {})
    valuation = financial.get('估值', {})
    dividend = float(valuation.get('股息率', 0) or 0)
    profit_growth = float(fi.get('利润增速', 0) or 0)
    
    # 预期收益计算
    expected_return = dividend + profit_growth
    if expected_return >= user_profile.expected_return:
        lines.append(f"\n   💰 预期收益：{expected_return:.1f}%（股息{dividend:.1f}% + 增长{profit_growth:.1f}%）")
        lines.append(f"   ✅ 可达到您的期望收益率 {user_profile.expected_return}%")
    else:
        lines.append(f"\n   ⚠️ 预期收益：{expected_return:.1f}%")
        lines.append(f"   ⚠️ 低于您的期望收益率 {user_profile.expected_return}%")
    
    # 复利建议
    if user_profile.holding_period == "长线" and dividend > 2:
        lines.append(f"\n   💎 复利机会：股息率 {dividend:.2f}%，长期持有可享受复利收益")
        lines.append("   📌 建议：持有 5 年以上，复利效应显著")
    
    lines.append("\n" + "="*60)
    
    return "\n".join(lines)
