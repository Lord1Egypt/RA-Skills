"""
Markdown 报告生成器
"""

from typing import Dict, Any
from datetime import datetime


class MarkdownReporter:
    """Markdown 报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate(self, symbol: str, results: Dict[str, Any], full: bool = False) -> str:
        """
        生成 Markdown 格式报告

        Args:
            symbol: 股票代码
            results: 分析结果字典
            full: 是否生成完整报告

        Returns:
            Markdown 格式报告
        """
        lines = []

        # 标题
        lines.append(f"# 📊 股票分析报告 - {symbol}")
        lines.append("")
        lines.append(f"**生成时间**: {self.timestamp}")
        lines.append("")

        # 如果有结论，先显示结论
        if 'conclusion' in results:
            lines.extend(self._render_conclusion(results['conclusion']))
            lines.append("")

        # 各维度分析结果
        dimension_names = {
            'data': '数据收集与验证',
            'fundamental': '基本面分析',
            'valuation': '估值分析',
            'industry': '行业与竞争分析',
            'technical': '技术面分析',
            'risk': '风险识别'
        }

        for key, name in dimension_names.items():
            if key in results and results[key]:
                lines.extend(self._render_dimension(name, results[key]))
                lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append("## ⚠️ 风险提示")
        lines.append("")
        lines.append("- 本分析仅供参考，不构成投资建议")
        lines.append("- 投资有风险，入市需谨慎")
        lines.append("- 请结合市场情况和自身判断做出决策")
        lines.append("- 数据可能存在延迟，请以实时数据为准")

        return "\n".join(lines)

    def _render_conclusion(self, conclusion: Dict[str, Any]) -> list:
        """渲染结论部分"""
        lines = []

        lines.append("## 🎯 综合评价")
        lines.append("")

        # 评级
        rating = conclusion.get('rating', '⭐⭐⭐ 中性')
        score = conclusion.get('overall_score', 50)
        lines.append(f"**综合评分**: {score}/100")
        lines.append(f"**投资评级**: {rating}")
        lines.append("")

        # 投资建议
        recommendation = conclusion.get('recommendation', '')
        if recommendation:
            lines.append(f"**投资建议**: {recommendation}")
            lines.append("")

        # 投资论点
        thesis = conclusion.get('investment_thesis', '')
        if thesis:
            lines.append("### 💡 投资论点")
            lines.append("")
            lines.append(thesis)
            lines.append("")

        # 行动计划
        action_plan = conclusion.get('action_plan', [])
        if action_plan:
            lines.append("### 📋 行动计划")
            lines.append("")
            for i, action in enumerate(action_plan, 1):
                lines.append(f"{i}. {action}")
            lines.append("")

        # 监控要点
        monitoring_points = conclusion.get('monitoring_points', [])
        if monitoring_points:
            lines.append("### 🔍 监控要点")
            lines.append("")
            for point in monitoring_points:
                lines.append(f"- {point}")
            lines.append("")

        return lines

    def _render_dimension(self, name: str, result: Dict[str, Any]) -> list:
        """渲染单个维度"""
        lines = []

        lines.append(f"## {name}")
        lines.append("")

        # 显示评分
        if 'score' in result:
            score = result['score']
            lines.append(f"**评分**: {score}/100")
            lines.append("")

        # 显示详情 - 对技术面分析做特殊处理
        if name == '技术面分析' and 'details' in result:
            details = result['details']
            lines.extend(self._render_technical_details(details))
        elif 'details' in result:
            details = result['details']
            for section_name, section_data in details.items():
                lines.append(f"### {section_name.replace('_', ' ').title()}")
                lines.append("")
                lines.append(f"```json")
                lines.append(self._format_json(section_data))
                lines.append(f"```")
                lines.append("")

        # 显示错误
        if result.get('errors'):
            lines.append("### ⚠️ 错误提示")
            lines.append("")
            for error in result['errors']:
                lines.append(f"- {error}")
            lines.append("")

        return lines

    def _render_technical_details(self, details: Dict[str, Any]) -> list:
        """渲染技术面分析详情"""
        lines = []

        # 趋势分析
        if 'trend' in details:
            trend = details['trend']
            lines.append("### 📈 趋势分析")
            lines.append("")
            lines.append(f"- **趋势方向**: {trend.get('direction', '未知')}")
            lines.append(f"- **趋势强度**: {trend.get('strength', '未知')}")
            lines.append(f"- **评级**: {trend.get('rating', '未知')}")
            if trend.get('change_5d') is not None:
                lines.append(f"- **5日涨跌幅**: {'+' if trend['change_5d'] > 0 else ''}{trend['change_5d']}%")
            if trend.get('change_20d') is not None:
                lines.append(f"- **20日涨跌幅**: {'+' if trend['change_20d'] > 0 else ''}{trend['change_20d']}%")
            if trend.get('change_60d') is not None:
                lines.append(f"- **60日涨跌幅**: {'+' if trend['change_60d'] > 0 else ''}{trend['change_60d']}%")
            lines.append("")

        # 均线系统
        if 'moving_average' in details:
            ma = details['moving_average']
            lines.append("### 🎯 均线系统 (5/10/20/60)")
            lines.append("")
            lines.append(f"- **当前价格**: {ma.get('current_price', 'N/A'):.2f}")
            lines.append(f"- **MA5**: {ma.get('MA5', 'N/A'):.2f}")
            lines.append(f"- **MA10**: {ma.get('MA10', 'N/A'):.2f}")
            lines.append(f"- **MA20**: {ma.get('MA20', 'N/A'):.2f}")
            lines.append(f"- **MA60**: {ma.get('MA60', 'N/A'):.2f}")
            lines.append(f"- **排列形态**: {ma.get('arrangement', '未知')}")
            lines.append(f"- **趋势强度**: {ma.get('trend_strength', '未知')}")
            lines.append("")

        # 支撑压力位
        if 'support_resistance' in details:
            sr = details['support_resistance']
            lines.append("### 🧱 支撑位与压力位")
            lines.append("")
            supports = sr.get('support_levels', [])
            resistances = sr.get('resistance_levels', [])
            if supports:
                lines.append(f"- **支撑位**: {', '.join([f'{s:.2f}' for s in supports])}")
            if resistances:
                lines.append(f"- **压力位**: {', '.join([f'{r:.2f}' for r in resistances])}")
            lines.append(f"- **近期低点**: {sr.get('recent_low', 'N/A'):.2f}")
            lines.append(f"- **近期高点**: {sr.get('recent_high', 'N/A'):.2f}")
            lines.append("")

        # 技术指标
        lines.append("### 📊 技术指标")
        lines.append("")
        
        if 'kdj' in details:
            kdj = details['kdj']
            lines.append(f"**KDJ (9,3,3):**")
            lines.append(f"- K: {kdj.get('K', 'N/A'):.2f}  D: {kdj.get('D', 'N/A'):.2f}  J: {kdj.get('J', 'N/A'):.2f}")
            lines.append("")
        
        if 'rsi' in details:
            rsi = details['rsi']
            lines.append(f"**RSI (14):**")
            lines.append(f"- RSI(14): {rsi.get('RSI14', 'N/A'):.2f}")
            lines.append("")
        
        if 'macd' in details:
            macd = details['macd']
            lines.append(f"**MACD (12,26,9):**")
            lines.append(f"- DIF: {macd.get('DIF', 'N/A'):.3f}  DEA: {macd.get('DEA', 'N/A'):.3f}  MACD: {macd.get('MACD', 'N/A'):.3f}")
            lines.append("")

        # 指标信号
        if 'indicators' in details:
            indicators = details['indicators']
            lines.append("### 📶 指标综合信号")
            lines.append("")
            lines.append(f"- **KDJ信号**: {indicators.get('kdj_signal', '未知')}")
            lines.append(f"- **RSI信号**: {indicators.get('rsi_signal', '未知')}")
            lines.append(f"- **MACD信号**: {indicators.get('macd_signal', '未知')}")
            lines.append(f"- **整体研判**: {indicators.get('overall', '未知')}")
            lines.append("")

        # 资金流向
        if 'fund_flow' in details:
            ff = details['fund_flow']
            lines.append("### 💸 资金流向")
            lines.append(f"- {ff.get('rating', '暂无数据')}")
            lines.append("")

        return lines

    def _format_json(self, data: Any, indent: int = 2) -> str:
        """格式化 JSON 数据"""
        import json
        return json.dumps(data, ensure_ascii=False, indent=indent)
