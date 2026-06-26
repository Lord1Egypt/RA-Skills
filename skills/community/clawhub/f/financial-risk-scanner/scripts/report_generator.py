#!/usr/bin/env python3
"""
报告生成模块

生成完整的Markdown财务风险报告，保存到 ~/.openclaw/workspace/memory/financial-risk/
"""

import os
import pandas as pd
from typing import Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ReportGenerator:
    """风险报告生成器"""

    # 报告输出路径
    OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/memory/financial-risk")

    # 指标名称映射
    INDICATOR_NAMES = {
        'cash_debt_paradox': '存贷双高',
        'receivables_anomaly': '应收账款畸高',
        'inventory_anomaly': '存货异常',
        'prepayments_surge': '预付账款激增',
        'other_receivables_high': '其他应收款高企',
        'construction_suspended': '在建工程悬案',
        'cash_profit_divergence': '净现比背离',
        'gross_margin_anomaly': '毛利率异常',
        'sales_expense_anomaly': '销售费用率异常',
        'abnormal_non_recurring': '异常非经常性损益',
        'asset_impairment_bath': '资产减值洗大澡',
        'related_transaction_high': '关联交易占比高',
        'related_fund_flows': '关联方资金往来',
        'related_guarantees': '关联担保过多',
        'goodwill_high': '商誉占比过高',
        'debt_ratio_high': '资产负债率畸高',
        'short_term_liquidity': '短期偿债压力',
        'dual_debt_high': '长短期借款双高',
        'auditor_changes': '频繁更换审计机构',
        'non_standard_opinion': '非标审计意见',
        'executive_departures': '高管频繁离职',
    }

    # 指标分类
    INDICATOR_CATEGORIES = {
        '资产真实性风险': [
            'cash_debt_paradox', 'receivables_anomaly', 'inventory_anomaly',
            'prepayments_surge', 'other_receivables_high', 'construction_suspended'
        ],
        '利润质量风险': [
            'cash_profit_divergence', 'gross_margin_anomaly', 'sales_expense_anomaly',
            'abnormal_non_recurring', 'asset_impairment_bath'
        ],
        '关联交易风险': [
            'related_transaction_high', 'related_fund_flows', 'related_guarantees'
        ],
        '资本结构风险': [
            'goodwill_high', 'debt_ratio_high', 'short_term_liquidity', 'dual_debt_high'
        ],
        '审计治理风险': [
            'auditor_changes', 'non_standard_opinion', 'executive_departures'
        ],
    }

    def __init__(self):
        """初始化报告生成器"""
        # 创建输出目录
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        logger.info(f"✅ 报告生成器初始化完成，输出目录: {self.OUTPUT_DIR}")

    def generate_report(
        self,
        stock_info: Dict,
        risk_results: Dict,
        financial_data: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        生成完整的Markdown风险报告

        Args:
            stock_info: 公司基本信息
            risk_results: 风险计算结果（包含21个指标 + _summary）
            financial_data: 原始财务数据
            output_path: 自定义输出路径（默认自动生成）

        Returns:
            str: 生成的报告路径
        """
        logger.info("=" * 60)
        logger.info("📝 开始生成风险报告...")
        logger.info("=" * 60)

        company_name = stock_info.get('name', '未知公司')
        ts_code = stock_info.get('ts_code', 'N/A')
        report_date = datetime.now().strftime('%Y-%m-%d')

        # 生成报告内容
        report_content = self._build_report_content(
            stock_info, risk_results, financial_data, report_date
        )

        # 确定输出路径
        if output_path:
            report_path = output_path
        else:
            filename = f"{company_name}_{report_date}.md"
            report_path = os.path.join(self.OUTPUT_DIR, filename)

        # 写入文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"✅ 报告生成完成: {report_path}")
        logger.info(f"   公司: {company_name}")
        logger.info(f"   总分: {risk_results['_summary']['total_score']} 分")
        logger.info(f"   严重程度: {risk_results['_summary']['severity']}")

        return report_path

    def _build_report_content(
        self,
        stock_info: Dict,
        risk_results: Dict,
        financial_data: Dict,
        report_date: str
    ) -> str:
        """构建报告内容"""

        company_name = stock_info.get('name', '未知公司')
        ts_code = stock_info.get('ts_code', 'N/A')
        industry = stock_info.get('industry', 'N/A')
        market = stock_info.get('market', 'N/A')
        list_date = stock_info.get('list_date', 'N/A')
        
        summary = risk_results['_summary']
        total_score = summary['total_score']
        severity = summary['severity']

        # 构建报告
        report = []

        # === 1. 标题 ===
        report.append(f"# {company_name} ({ts_code}) 财务风险扫描报告")
        report.append("")
        report.append(f"> 报告日期: {report_date}")
        report.append(f"> 扫描工具: Financial Risk Scanner v1.0")
        report.append("")

        # === 2. 公司概况 ===
        report.append("## 一、公司概况")
        report.append("")
        report.append("| 项目 | 信息 |")
        report.append("|------|------|")
        report.append(f"| 公司名称 | {company_name} |")
        report.append(f"| 股票代码 | {ts_code} |")
        report.append(f"| 所属行业 | {industry} |")
        report.append(f"| 市场 | {market} |")
        report.append(f"| 上市日期 | {list_date} |")
        
        # 计算上市年限
        if list_date and list_date != 'N/A':
            try:
                list_dt = datetime.strptime(list_date, '%Y%m%d')
                years_listed = (datetime.now() - list_dt).days // 365
                report.append(f"| 上市年限 | {years_listed} 年 |")
            except Exception:
                report.append(f"| 上市年限 | N/A |")
        else:
            report.append(f"| 上市年限 | N/A |")
        
        report.append("")

        # === 3. 风险摘要 ===
        report.append("## 二、风险摘要")
        report.append("")
        
        # 总分和严重程度
        report.append(f"### 总体评级: {severity}")
        report.append("")
        report.append(f"- **总分**: {total_score} 分")
        report.append(f"- **严重程度**: {severity}")
        report.append("")
        
        # 分数分布
        report.append("### 风险分布")
        report.append("")
        report.append("| 级别 | 指标数 | 占比 |")
        report.append("|------|--------|------|")
        
        total_indicators = summary['indicator_count']
        if total_indicators > 0:
            critical_pct = summary['critical_count'] / total_indicators * 100
            high_pct = summary['high_count'] / total_indicators * 100
            moderate_pct = summary['moderate_count'] / total_indicators * 100
            low_pct = summary['low_count'] / total_indicators * 100
            
            report.append(f"| 🔴 严重 (3分) | {summary['critical_count']} | {critical_pct:.1f}% |")
            report.append(f"| 🟠 中等 (2分) | {summary['high_count']} | {high_pct:.1f}% |")
            report.append(f"| 🟡 轻微 (1分) | {summary['moderate_count']} | {moderate_pct:.1f}% |")
            report.append(f"| 🟢 无风险 (0分) | {summary['low_count']} | {low_pct:.1f}% |")
        
        report.append("")
        
        # 重点关注指标
        report.append("### 重点关注指标")
        report.append("")
        
        # 找出得分≥2的指标
        high_risk_indicators = [(k, v) for k, v in risk_results.items() 
                               if k != '_summary' and v.get('score', 0) >= 2]
        
        if high_risk_indicators:
            high_risk_indicators.sort(key=lambda x: x[1]['score'], reverse=True)
            
            report.append("| 指标 | 评分 | 关键数值 | 趋势 |")
            report.append("|------|------|----------|------|")
            
            for key, value in high_risk_indicators:
                name = self.INDICATOR_NAMES.get(key, key)
                score = value['score']
                key_value = self._format_key_value(key, value)
                trend = value.get('trend', 'N/A')
                
                # 标记严重程度
                severity_icon = '🔴' if score == 3 else '🟠'
                report.append(f"| {severity_icon} {name} | {score} 分 | {key_value} | {trend} |")
            
            report.append("")
        else:
            report.append("✅ 未发现高风险指标（得分≥2）。")
            report.append("")
        
        # === 4. 详细分析 ===
        report.append("## 三、详细风险分析")
        report.append("")
        
        # 按类别输出
        for category, indicators in self.INDICATOR_CATEGORIES.items():
            report.append(f"### {category}")
            report.append("")
            
            # 类别分数汇总
            category_scores = [risk_results[ind]['score'] for ind in indicators 
                             if ind in risk_results]
            category_total = sum(category_scores)
            category_max = len(indicators) * 3
            
            report.append(f"**类别得分**: {category_total}/{category_max} 分")
            report.append("")
            
            # 指标详情表
            report.append("| 指标 | 评分 | 数值 | 趋势 | 分析 |")
            report.append("|------|------|------|------|------|")
            
            for ind in indicators:
                if ind not in risk_results:
                    continue
                
                result = risk_results[ind]
                name = self.INDICATOR_NAMES.get(ind, ind)
                score = result['score']
                value = self._format_indicator_value(result)
                trend = result.get('trend', 'N/A')
                analysis = self._generate_indicator_analysis(ind, result)
                
                # 评分标记
                score_icon = {'0': '🟢', '1': '🟡', '2': '🟠', '3': '🔴'}
                score_display = score_icon.get(str(score), str(score)) + f" {score}分"
                
                report.append(f"| {name} | {score_display} | {value} | {trend} | {analysis} |")
            
            report.append("")
        
        # === 5. 交叉验证建议 ===
        report.append("## 四、交叉验证建议")
        report.append("")
        report.append("根据检测到的风险信号，建议进一步核实以下信息：")
        report.append("")
        
        # 根据高风险指标生成验证建议
        verification_items = self._generate_verification_items(risk_results)
        
        if verification_items:
            for i, item in enumerate(verification_items, 1):
                report.append(f"{i}. **{item['indicator']}**: {item['action']}")
                report.append(f"   - 查阅章节: `{item['source']}`")
                report.append(f"   - 关注要点: {item['points']}")
                report.append("")
        else:
            report.append("✅ 未发现需要重点交叉验证的风险信号。")
            report.append("")
        
        # === 6. 严重程度评级说明 ===
        report.append("## 五、严重程度评级说明")
        report.append("")
        report.append("| 级别 | 总分范围 | 含义 | 建议 |")
        report.append("|------|----------|------|------|")
        report.append("| 🔴 Critical | 31+分 | 多个严重风险信号，可能存在重大财务问题 | 建议立即深入调查，谨慎投资 |")
        report.append("| 🟠 High | 16-30分 | 存在较明显风险，需要重点关注 | 建议详细核实，降低仓位 |")
        report.append("| 🟡 Moderate | 6-15分 | 有轻微风险信号，需持续观察 | 建议关注后续财报变化 |")
        report.append("| 🟢 Low | 0-5分 | 风险较低，财务健康 | 可正常跟踪，定期复检 |")
        report.append("")
        
        # === 7. 数据局限性说明 ===
        report.append("## 六、数据局限性说明")
        report.append("")
        report.append("本次扫描基于Tushare公开财务数据，存在以下局限：")
        report.append("")
        report.append("- **关联交易数据**: Tushare无直接关联交易字段，需从年报附注手动获取")
        report.append("- **高管变动数据**: 需单独调用stk_managers接口获取高管变动记录")
        report.append("- **行业对比数据**: 未进行同行业毛利率、费用率对比验证")
        report.append("- **附注数据**: 部分风险指标需从财报附注核实（如减值明细、关联方明细）")
        report.append("")
        report.append("建议结合年报全文、公告、新闻等多源信息进行综合判断。")
        report.append("")
        
        # === 8. 附录：原始数据摘要 ===
        report.append("## 附录：原始财务数据摘要")
        report.append("")
        
        # 资产负债表摘要
        balance = financial_data.get('balance', pd.DataFrame())
        if not balance.empty:
            report.append("### 资产负债表最近2年")
            report.append("")
            latest_balance = balance.tail(2)
            for _, row in latest_balance.iterrows():
                end_date = row.get('end_date', 'N/A')
                report.append(f"**{end_date}**:")
                report.append(f"- 总资产: {self._format_amount(row.get('total_assets'))}")
                report.append(f"- 总负债: {self._format_amount(row.get('total_liab'))}")
                report.append(f"- 净资产: {self._format_amount(row.get('total_hldr_equity'))}")
                report.append(f"- 货币资金: {self._format_amount(row.get('monetary_cap'))}")
                report.append("")
        
        # 利润表摘要
        income = financial_data.get('income', pd.DataFrame())
        if not income.empty:
            report.append("### 利润表最近2年")
            report.append("")
            latest_income = income.tail(2)
            for _, row in latest_income.iterrows():
                end_date = row.get('end_date', 'N/A')
                report.append(f"**{end_date}**:")
                report.append(f"- 营业收入: {self._format_amount(row.get('revenue'))}")
                report.append(f"- 净利润: {self._format_amount(row.get('net_profit'))}")
                report.append(f"- 毛利率: {(row.get('revenue', 1) - row.get('oper_cost', 0))/row.get('revenue', 1)*100:.1f}%")
                report.append("")
        
        # 现金流量表摘要
        cashflow = financial_data.get('cashflow', pd.DataFrame())
        if not cashflow.empty:
            report.append("### 现金流量表最近2年")
            report.append("")
            latest_cashflow = cashflow.tail(2)
            for _, row in latest_cashflow.iterrows():
                end_date = row.get('end_date', 'N/A')
                report.append(f"**{end_date}**:")
                report.append(f"- 经营现金流净额: {self._format_amount(row.get('net_cash_flows_oper_act'))}")
                report.append(f"- 投资现金流净额: {self._format_amount(row.get('net_cash_flows_inv_act'))}")
                report.append(f"- 筹资现金流净额: {self._format_amount(row.get('net_cash_flows_fnc_act'))}")
                report.append("")
        
        # === 结尾 ===
        report.append("---")
        report.append("")
        report.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append(f"*Financial Risk Scanner - OpenClaw Workspace*")
        
        return '\n'.join(report)

    def _format_key_value(self, indicator: str, result: Dict) -> str:
        """格式化关键数值"""
        details = result.get('details', {})
        
        if indicator == 'cash_debt_paradox':
            cash = details.get('cash_ratio_latest', 0) * 100
            debt = details.get('debt_ratio_latest', 0) * 100
            return f"现金{cash:.1f}% / 有息负债{debt:.1f}%"
        
        elif indicator == 'receivables_anomaly':
            ratio = details.get('receiv_ratio_latest', 0) * 100
            return f"应收/收入 {ratio:.1f}%"
        
        elif indicator == 'inventory_anomaly':
            decline = details.get('turnover_decline_pct', 0) * 100
            return f"周转率下降 {decline:.1f}%"
        
        elif indicator == 'prepayments_surge':
            ratio = details.get('ratio_latest', 0) * 100
            return f"预付/资产 {ratio:.1f}%"
        
        elif indicator == 'other_receivables_high':
            ratio = details.get('ratio_latest', 0) * 100
            return f"其他应收/净资产 {ratio:.1f}%"
        
        elif indicator == 'construction_suspended':
            ratio = details.get('ratio_latest', 0) * 100
            return f"在建/资产 {ratio:.1f}%"
        
        elif indicator == 'cash_profit_divergence':
            ratio = result.get('value', 0)
            divergence = details.get('divergence_latest', False)
            return f"净现比 {ratio:.2f}" + (" (背离)" if divergence else "")
        
        elif indicator == 'gross_margin_anomaly':
            gm = details.get('gross_margin_latest', 0) * 100
            return f"毛利率 {gm:.1f}%"
        
        elif indicator == 'sales_expense_anomaly':
            ratio = details.get('ratio_latest', 0) * 100
            return f"销售费用率 {ratio:.1f}%"
        
        elif indicator == 'abnormal_non_recurring':
            ratio = details.get('ratio_latest', 0) * 100
            return f"非经常性占比 {ratio:.1f}%"
        
        elif indicator == 'asset_impairment_bath':
            ratio = details.get('ratio_latest', 0) * 100
            return f"减值/净利润 {ratio:.1f}%"
        
        elif indicator == 'goodwill_high':
            ratio = details.get('ratio_latest', 0) * 100
            return f"商誉/净资产 {ratio:.1f}%"
        
        elif indicator == 'debt_ratio_high':
            ratio = details.get('debt_ratio_latest', 0) * 100
            return f"资产负债率 {ratio:.1f}%"
        
        elif indicator == 'short_term_liquidity':
            pressure = details.get('pressure_ratio_latest', 0)
            cr = details.get('current_ratio_latest', 0)
            return f"短借/现金 {pressure:.1f}, 流动比率 {cr:.2f}"
        
        elif indicator == 'dual_debt_high':
            short = details.get('short_ratio_latest', 0) * 100
            long = details.get('long_ratio_latest', 0) * 100
            return f"短借{short:.1f}% / 长借{long:.1f}%"
        
        elif indicator == 'auditor_changes':
            count = details.get('change_count', 0)
            return f"更换 {count} 次"
        
        elif indicator == 'non_standard_opinion':
            desc = details.get('audit_result_desc', 'N/A')
            return desc
        
        else:
            value = result.get('value', 0)
            if isinstance(value, float):
                return f"{value:.2f}"
            return str(value)

    def _format_indicator_value(self, result: Dict) -> str:
        """格式化指标数值"""
        value = result.get('value', 0)
        
        if isinstance(value, float):
            if abs(value) < 0.01:
                return f"{value:.4f}"
            elif abs(value) < 1:
                return f"{value:.2f}"
            else:
                return f"{value:.1f}"
        return str(value)

    def _generate_indicator_analysis(self, indicator: str, result: Dict) -> str:
        """生成指标简要分析"""
        score = result.get('score', 0)
        trend = result.get('trend', 'N/A')
        details = result.get('details', {})
        
        if score == 0:
            return "指标正常，无明显风险信号"
        
        elif indicator == 'cash_debt_paradox':
            years = details.get('dual_high_years', 0)
            return f"双高持续{years}年，需验证资金真实性"
        
        elif indicator == 'receivables_anomaly':
            years = details.get('growth_abnormal_years', 0)
            return f"应收增速异常{years}年，需核实客户质量"
        
        elif indicator == 'inventory_anomaly':
            if details.get('turnover_declining', False):
                return "存货周转率下降，需核实存货质量"
            return "存货增速异常，需核实存货真实性"
        
        elif indicator == 'cash_profit_divergence':
            divergence = details.get('divergence_latest', False)
            if divergence:
                return "利润为正但现金流为负，利润质量存疑"
            return "净现比偏低，利润含金量不足"
        
        elif indicator == 'gross_margin_anomaly':
            return "毛利率偏高，需行业对比验证合理性"
        
        elif indicator == 'abnormal_non_recurring':
            return "利润依赖非经常性损益，可持续性存疑"
        
        elif indicator == 'asset_impairment_bath':
            count = details.get('bath_years_count', 0)
            if count > 0:
                return f"存在{count}年大额减值，疑似洗大澡"
            return "减值比例偏高，需核实减值合理性"
        
        elif indicator == 'goodwill_high':
            years = details.get('abnormal_years', 0)
            return f"商誉占比高企{years}年，减值风险较大"
        
        elif indicator == 'debt_ratio_high':
            return "负债率偏高，财务杠杆风险较大"
        
        elif indicator == 'short_term_liquidity':
            cr = details.get('current_ratio_latest', 0)
            if cr < 1:
                return "流动比率<1，短期偿债压力大"
            return "短期借款/现金偏高，需关注偿债能力"
        
        elif indicator == 'non_standard_opinion':
            desc = details.get('audit_result_desc', 'N/A')
            return f"审计意见: {desc}"
        
        else:
            if score >= 2:
                return "达到风险阈值，需深入核实"
            return "接近风险阈值，建议关注"

    def _generate_verification_items(self, risk_results: Dict) -> list:
        """生成交叉验证建议"""
        items = []
        
        for key, result in risk_results.items():
            if key == '_summary':
                continue
            
            score = result.get('score', 0)
            
            if score >= 2:
                name = self.INDICATOR_NAMES.get(key, key)
                
                # 根据指标类型生成验证建议
                if key == 'cash_debt_paradox':
                    items.append({
                        'indicator': name,
                        'action': '核实货币资金真实性和有息负债必要性',
                        'source': '年报附注"货币资金"、"银行借款"章节',
                        'points': '利息收入与现金余额匹配度、借款利率合理性',
                    })
                
                elif key == 'receivables_anomaly':
                    items.append({
                        'indicator': name,
                        'action': '核实应收账款客户质量和回收情况',
                        'source': '年报附注"应收账款"、"主要客户"章节',
                        'points': '前5大应收客户、账龄结构、坏账计提比例',
                    })
                
                elif key == 'inventory_anomaly':
                    items.append({
                        'indicator': name,
                        'action': '核实存货构成和跌价准备',
                        'source': '年报附注"存货"、"存货跌价准备"章节',
                        'points': '存货构成（原材料/在产品/产成品）、存货周转天数',
                    })
                
                elif key == 'cash_profit_divergence':
                    items.append({
                        'indicator': name,
                        'action': '核实利润来源和现金回收情况',
                        'source': '年报附注"收入确认政策"、"应收账款"章节',
                        'points': '收入确认时点、应收账款回收周期、预收款项',
                    })
                
                elif key == 'gross_margin_anomaly':
                    items.append({
                        'indicator': name,
                        'action': '对比同行业毛利率水平',
                        'source': '行业研究报告、竞争对手年报',
                        'points': '成本结构差异、定价策略、产品竞争力',
                    })
                
                elif key == 'abnormal_non_recurring':
                    items.append({
                        'indicator': name,
                        'action': '核实非经常性损益构成',
                        'source': '年报附注"非经常性损益"章节',
                        'points': '政府补助持续性、资产处置背景、投资收益来源',
                    })
                
                elif key == 'asset_impairment_bath':
                    items.append({
                        'indicator': name,
                        'action': '核实减值资产构成和减值合理性',
                        'source': '年报附注"资产减值损失"章节',
                        'points': '减值资产类型、减值测试方法、历史减值反转情况',
                    })
                
                elif key == 'goodwill_high':
                    items.append({
                        'indicator': name,
                        'action': '核实商誉来源和减值测试',
                        'source': '年报附注"商誉"、"商誉减值测试"章节',
                        'points': '收购标的业绩、减值测试假设、历史减值情况',
                    })
                
                elif key == 'debt_ratio_high':
                    items.append({
                        'indicator': name,
                        'action': '核实债务结构和偿债能力',
                        'source': '年报附注"银行借款"、"财务费用"章节',
                        'points': '借款期限结构、利率水平、抵押担保情况',
                    })
                
                elif key == 'short_term_liquidity':
                    items.append({
                        'indicator': name,
                        'action': '核实短期偿债安排和银行授信',
                        'source': '年报附注"短期借款"、"银行授信"章节',
                        'points': '到期借款安排、银行授信额度、还款计划',
                    })
                
                elif key == 'non_standard_opinion':
                    items.append({
                        'indicator': name,
                        'action': '阅读审计报告强调事项',
                        'source': '年报审计报告全文',
                        'points': '审计意见强调事项、管理层回复、后续整改',
                    })
        
        return items

    def _format_amount(self, amount: Optional[float]) -> str:
        """格式化金额"""
        if amount is None or amount == 0:
            return "N/A"
        
        if abs(amount) >= 1e9:
            return f"{amount/1e9:.2f} 亿元"
        elif abs(amount) >= 1e6:
            return f"{amount/1e6:.2f} 万元"
        else:
            return f"{amount:.2f} 元"


if __name__ == "__main__":
    # 测试用例
    print("=" * 60)
    print("报告生成器测试")
    print("=" * 60)
    
    generator = ReportGenerator()
    
    # 模拟数据
    mock_stock_info = {
        'ts_code': '000001.SZ',
        'name': '平安银行',
        'industry': '银行',
        'market': '主板',
        'list_date': '19910403',
    }
    
    mock_risk_results = {
        'cash_debt_paradox': {'score': 0, 'value': 0, 'trend': '稳定', 'details': {}},
        'receivables_anomaly': {'score': 1, 'value': 0.25, 'trend': '上升', 'details': {}},
        'cash_profit_divergence': {'score': 2, 'value': 0.3, 'trend': '下降', 
                                   'details': {'divergence_latest': True}},
        '_summary': {
            'total_score': 3,
            'severity': '🟡 Moderate',
            'indicator_count': 21,
            'critical_count': 0,
            'high_count': 1,
            'moderate_count': 1,
            'low_count': 19,
        }
    }
    
    mock_financial_data = {
        'balance': pd.DataFrame([
            {'end_date': '20221231', 'total_assets': 1e9, 'total_liab': 0.7e9, 
             'total_hldr_equity': 0.3e9, 'monetary_cap': 0.1e9},
            {'end_date': '20231231', 'total_assets': 1.1e9, 'total_liab': 0.8e9,
             'total_hldr_equity': 0.3e9, 'monetary_cap': 0.12e9},
        ]),
        'income': pd.DataFrame([
            {'end_date': '20221231', 'revenue': 0.5e9, 'net_profit': 0.05e9, 'oper_cost': 0.4e9},
            {'end_date': '20231231', 'revenue': 0.6e9, 'net_profit': 0.06e9, 'oper_cost': 0.45e9},
        ]),
        'cashflow': pd.DataFrame([
            {'end_date': '20221231', 'net_cash_flows_oper_act': 0.02e9},
            {'end_date': '20231231', 'net_cash_flows_oper_act': 0.03e9},
        ]),
    }
    
    report_path = generator.generate_report(
        mock_stock_info,
        mock_risk_results,
        mock_financial_data
    )
    
    print(f"\n测试报告已生成: {report_path}")