#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析主模块 - 整合所有分析功能，提供统一的分析接口
"""

import os
import sys
from typing import Dict, List, Optional
from datetime import datetime

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from news_analyzer import NewsAnalyzer
from financial_analyzer import FinancialAnalyzer
from technical_analyzer import TechnicalAnalyzer

class AdvancedStockAnalyzer:
    def __init__(self, cache_dir: str = None):
        self.data_fetcher = DataFetcher(cache_dir)
        self.news_analyzer = NewsAnalyzer()
        self.financial_analyzer = FinancialAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
    
    def comprehensive_analysis(self, stock_query: str, days: int = 120, 
                              include_news: bool = True, 
                              include_financial: bool = True,
                              include_technical: bool = True) -> Dict:
        """
        对股票进行全面分析
        :param stock_query: 股票代码或公司名称
        :param days: 分析天数
        :param include_news: 是否包含新闻分析
        :param include_financial: 是否包含财务分析
        :param include_technical: 是否包含技术分析
        :return: 完整的分析结果
        """
        result = {
            'stock_code': stock_query,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'company_name': self._get_company_name(stock_query)
        }
        
        # 1. 新闻舆情分析
        if include_news:
            result['news_analysis'] = self._analyze_news(result['company_name'], days)
        
        # 2. 财务报表分析
        if include_financial:
            result['financial_analysis'] = self._analyze_financial(stock_query)
        
        # 3. 技术指标分析
        if include_technical:
            result['technical_analysis'] = self._analyze_technical(stock_query, days)
        
        # 4. 综合投资建议
        result['investment_recommendation'] = self._generate_recommendation(result)
        
        return result
    
    def _get_company_name(self, stock_query: str) -> str:
        """获取公司名称"""
        # 这里可以对接股票代码转名称的API，暂时简化处理
        if stock_query.isdigit():
            return f"上市公司({stock_query})"
        return stock_query
    
    def _analyze_news(self, company_name: str, days: int = 30) -> Dict:
        """分析公司新闻舆情"""
        news_list = self.data_fetcher.search_company_news(company_name, days)
        news_analysis = self.news_analyzer.analyze_news_sentiment(news_list, company_name)
        
        # 补充分析
        if news_analysis['outlook_news']:
            news_analysis['management_outlook'] = self.news_analyzer.extract_management_outlook(
                news_analysis['outlook_news']
            )
        
        if news_analysis['management_news']:
            stability, stability_desc = self.news_analyzer.analyze_management_stability(
                news_analysis['management_news']
            )
            news_analysis['management_stability'] = stability
            news_analysis['management_stability_desc'] = stability_desc
        
        if news_analysis['holder_news']:
            news_analysis['holder_changes'] = self.news_analyzer.analyze_holder_changes(
                news_analysis['holder_news']
            )
        
        # 获取股东变动数据
        holder_data = self.data_fetcher.get_holder_changes(company_name)
        news_analysis['short_selling'] = holder_data.get('short_selling', {})
        news_analysis['institutional_holding'] = holder_data.get('institutional_holding', {})
        news_analysis['management_holding'] = holder_data.get('management_holding', {})
        
        return news_analysis
    
    def _analyze_financial(self, stock_code: str) -> Dict:
        """分析财务报表"""
        financial_data = self.data_fetcher.get_financial_report(stock_code)
        return self.financial_analyzer.analyze_financial_health(financial_data)
    
    def _analyze_technical(self, stock_code: str, days: int = 120) -> Dict:
        """分析技术指标"""
        indicators = self.data_fetcher.get_technical_indicators(stock_code, days)
        analysis = self.technical_analyzer.analyze_trading_signals(indicators)
        analysis['report'] = self.technical_analyzer.generate_trading_report(analysis)
        analysis['current_price'] = indicators['price']
        return analysis
    
    def _generate_recommendation(self, analysis_result: Dict) -> Dict:
        """生成综合投资建议"""
        scores = []
        weights = {
            'news': 0.25,
            'financial': 0.40,
            'technical': 0.35
        }
        
        # 新闻舆情评分
        if 'news_analysis' in analysis_result:
            news = analysis_result['news_analysis']
            if news['overall_sentiment'] == 'positive':
                news_score = 80
            elif news['overall_sentiment'] == 'negative':
                news_score = 30
            else:
                news_score = 55
            
            # 调整评分
            if news['has_short_report']:
                news_score -= 30
            if news['management_stability'] == 'unstable':
                news_score -= 20
            if news.get('holder_changes', {}).get('has_management_reduction', False):
                news_score -= 15
            
            scores.append(news_score * weights['news'])
        
        # 财务评分
        if 'financial_analysis' in analysis_result:
            financial_score = analysis_result['financial_analysis']['overall_score']
            scores.append(financial_score * weights['financial'])
        
        # 技术评分
        if 'technical_analysis' in analysis_result:
            technical_score = analysis_result['technical_analysis']['comprehensive']['total_score']
            scores.append(technical_score * weights['technical'])
        
        total_score = round(sum(scores), 2) if scores else 50
        
        # 评级
        if total_score >= 80:
            rating = 'A+（强烈推荐）'
            action = '强烈建议买入，中长期持有'
            confidence = '95%'
        elif total_score >= 70:
            rating = 'A（推荐）'
            action = '建议买入，逢低加仓'
            confidence = '85%'
        elif total_score >= 60:
            rating = 'B+（谨慎推荐）'
            action = '建议少量建仓，波段操作'
            confidence = '70%'
        elif total_score >= 50:
            rating = 'B（中性）'
            action = '建议观望，等待明确信号'
            confidence = '50%'
        elif total_score >= 40:
            rating = 'C+（回避）'
            action = '建议逢高减持，控制仓位'
            confidence = '30%'
        else:
            rating = 'C（强烈回避）'
            action = '建议立即卖出，空仓观望'
            confidence = '10%'
        
        # 风险提示
        risk_factors = []
        if 'news_analysis' in analysis_result:
            if analysis_result['news_analysis']['has_short_report']:
                risk_factors.append("存在机构做空报告")
            if analysis_result['news_analysis']['management_stability'] == 'unstable':
                risk_factors.append("管理层动荡")
            if analysis_result['news_analysis'].get('holder_changes', {}).get('has_management_reduction', False):
                risk_factors.append("高管减持")
            if analysis_result['news_analysis']['negative_count'] > analysis_result['news_analysis']['positive_count']:
                risk_factors.append("负面新闻较多")
        
        if 'financial_analysis' in analysis_result:
            financial = analysis_result['financial_analysis']
            if financial['debt_analysis']['debt_rating'] == '较高':
                risk_factors.append("资产负债率较高")
            if financial['cash_flow_quality']['quality'] == '较差':
                risk_factors.append("现金流质量较差")
            if financial['profit_growth']['quarterly_yoy'] < 0:
                risk_factors.append("利润同比下滑")
        
        if 'technical_analysis' in analysis_result:
            technical = analysis_result['technical_analysis']['comprehensive']
            if technical['risk_level'] == '高':
                risk_factors.append("技术面走弱")
        
        return {
            'total_score': total_score,
            'rating': rating,
            'action': action,
            'confidence': confidence,
            'risk_factors': risk_factors,
            'summary': f"综合评分{total_score}分，{rating}。{action}"
        }
    
    def generate_analysis_report(self, analysis_result: Dict, output_format: str = 'text') -> str:
        """生成可读的分析报告"""
        company = analysis_result['company_name']
        code = analysis_result['stock_code']
        time = analysis_result['analysis_time']
        
        report = [
            f"📈 {company}({code}) 深度分析报告",
            f"⏰ 分析时间：{time}",
            "=" * 60,
            ""
        ]
        
        # 综合建议
        rec = analysis_result['investment_recommendation']
        report.extend([
            "🎯 综合投资建议",
            "-" * 40,
            f"综合评分：{rec['total_score']}/100",
            f"投资评级：{rec['rating']}",
            f"操作建议：{rec['action']}",
            f"信心指数：{rec['confidence']}"
        ])
        
        if rec['risk_factors']:
            report.append("\n⚠️ 风险提示：")
            for risk in rec['risk_factors']:
                report.append(f"  • {risk}")
        
        # 新闻舆情分析
        if 'news_analysis' in analysis_result:
            news = analysis_result['news_analysis']
            report.extend([
                "",
                "📰 新闻舆情分析",
                "-" * 40,
                f"舆情倾向：{self._get_sentiment_text(news['overall_sentiment'])}",
                f"新闻总数：{news['news_count']}条（利好{news['positive_count']}条，利空{news['negative_count']}条）",
                f"机构做空：{'⚠️ 存在明确做空报告' if news['has_short_report'] else '✅ 无机构做空信息'}"
            ])
            
            if 'management_stability' in news:
                report.append(f"管理层稳定性：{self._get_stability_text(news['management_stability'])}")
            
            if news.get('short_selling', {}).get('has_short_report'):
                report.append(f"做空信息：{news['short_selling'].get('short_reports', [])}")
            
            if news['positive_news'][:3]:
                report.append("\n✅ 近期利好：")
                for news_item in news['positive_news'][:3]:
                    title = news_item.get('title', '无标题')
                    report.append(f"  • {title}")
            
            if news['negative_news'][:3]:
                report.append("\n❌ 近期利空：")
                for news_item in news['negative_news'][:3]:
                    title = news_item.get('title', '无标题')
                    report.append(f"  • {title}")
            
            if 'management_outlook' in news and news['management_outlook'] != "暂无公开的管理层展望信息":
                report.append("\n🔮 管理层展望：")
                report.append(f"  {news['management_outlook']}")
        
        # 财务分析
        if 'financial_analysis' in analysis_result:
            financial = analysis_result['financial_analysis']
            report.extend([
                "",
                "💰 财务数据分析",
                "-" * 40,
                f"财务评级：{financial['overall_rating']}（{financial['overall_score']}/100）",
                f"管理层：{financial['management']['summary']}",
                f"护城河：{financial['moat']['summary']}",
                f"营收增长：{financial['revenue_growth']['summary']}",
                f"利润增长：{financial['profit_growth']['summary']}",
                f"ROE分析：{financial['roe_analysis']['summary']}",
                f"扣非ROE：{financial['deduct_roe_analysis']['summary']}",
                f"偿债能力：{financial['debt_analysis']['summary']}",
                f"现金流：{financial['cash_flow_quality']['summary']}",
                f"研发投入：{financial['rd_analysis']['summary']}",
                f"PEG估值：{financial['peg_analysis']['summary']}",
                f"自由现金流：{financial['fcf_analysis']['summary']}"
            ])
        
        # 技术分析
        if 'technical_analysis' in analysis_result:
            technical = analysis_result['technical_analysis']
            report.extend([
                "",
                "📊 技术指标分析",
                "-" * 40,
                f"当前价格：{technical['current_price']:.2f}元",
                f"技术评分：{technical['comprehensive']['total_score']}/100",
                f"技术建议：{technical['comprehensive']['recommendation']}",
                f"风险等级：{technical['comprehensive']['risk_level']}"
            ])
            
            # 各指标详情
            report.append("\n📈 各指标信号：")
            report.append(f"MACD：{technical['macd']['rating']}")
            report.append(f"KDJ：{technical['kdj']['rating']}")
            report.append(f"RSI：{technical['rsi']['rating']}")
            report.append(f"EMA：{technical['ema']['rating']}")
        
        report.extend([
            "",
            "=" * 60,
            "⚠️ 免责声明：本报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。"
        ])
        
        return "\n".join(report)
    
    def _get_sentiment_text(self, sentiment: str) -> str:
        """情感文本转换"""
        mapping = {
            'positive': '✅ 正面',
            'negative': '❌ 负面',
            'neutral': '⚪ 中性'
        }
        return mapping.get(sentiment, '⚪ 中性')
    
    def _get_stability_text(self, stability: str) -> str:
        """稳定性文本转换"""
        mapping = {
            'stable': '✅ 稳定',
            'minor_changes': '⚠️ 小幅变动',
            'unstable': '❌ 动荡'
        }
        return mapping.get(stability, '⚪ 未知')

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法: python stock_analyzer.py <股票代码或名称> [分析天数]")
        print("示例: python stock_analyzer.py 000001 120")
        return
    
    stock_query = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    
    analyzer = AdvancedStockAnalyzer()
    print(f"正在分析 {stock_query}...")
    
    result = analyzer.comprehensive_analysis(stock_query, days)
    report = analyzer.generate_analysis_report(result)
    
    print(report)
    
    # 保存报告
    output_file = f"{stock_query}_分析报告_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {output_file}")

if __name__ == "__main__":
    main()
