#!/usr/bin/env python3
"""
多维度情报搜索服务
系统化搜索 16 个维度的金融情报：

公司层面（5个维度）：
1. 最新消息：公司公告、重大事件
2. 风险排查：减持、处罚、调查、诉讼、业绩下滑
3. 业绩预期：年报预告、业绩快报
4. 行业热点：政策、趋势、竞争格局
5. 技术突破：创新、专利、产品

宏观与国际层面（5个维度）：
6. 宏观经济：货币政策、财政政策、经济数据
7. 国际局势：地缘政治、贸易摩擦、国际制裁
8. 全球市场：美股/欧股走势、全球风险偏好
9. 大宗商品：原油/黄金/铜等与行业关联的商品价格
10. 汇率与资金：人民币汇率、北向资金、外资流向

时政与政策层面（6个维度）：
11. 国内重大政策：国务院、两会、改革政策
12. 央行与监管动态：央行操作、金融监管、IPO/退市
13. 地缘冲突实时：台海、中东、俄乌等热点追踪
14. 中美博弈动态：关税、科技制裁、出口管制
15. 产业链与供应链：供应链风险、关键技术自主化
16. 社会民生与消费：消费趋势、人口、就业、社会事件

功能特性：
- 数据源质量分级：每个搜索维度标注推荐的优质/官方数据源
- 内容时效性校验指令：Agent 必须核验搜索结果所述数据的所属时期
- 搜索结果验证规则：过滤转载旧闻、过时财报、过期季度数据
- 严格时效性校验：基于"当前应关注的财务时期"精确判断
- 与 fetch_trending.py 协同：脚本热点直接映射到搜索维度，避免重复搜索
- 支持热点关键词动态注入：接收 macro_analysis.py 提取的热点实体关键词，
  动态补充到地缘/宏观搜索查询中
- 新增 generate_dynamic_searches() 方法：基于热点关键词生成额外搜索指令

依赖：需要配置搜索引擎 API（Tavily/SerpAPI/Bocha/Brave）或使用 web_search
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SearchService:
    """多维度情报搜索服务（严格时效性 + 脚本热点协同 + 动态关键词注入）"""

    # 优质/官方数据源推荐（按优先级排序）
    # Agent 应优先从这些源搜索，而非泛网搜索
    PREFERRED_SOURCES = {
        'company_news': [
            '上交所公告（sse.com.cn）',
            '深交所公告（szse.cn）',
            '巨潮资讯网（cninfo.com.cn）',
            '东方财富（eastmoney.com）',
            '同花顺（10jqka.com.cn）',
        ],
        'financial_report': [
            '巨潮资讯网（cninfo.com.cn）— 上市公司年报/季报/公告原文',
            '上交所/深交所披露平台 — 官方财务报告',
            '东方财富Choice — 财务数据终端',
            'Wind资讯 — 专业金融数据',
        ],
        'macro_policy': [
            '中国政府网（gov.cn）— 国务院政策原文',
            '中国人民银行（pbc.gov.cn）— 货币政策、利率公告',
            '国家统计局（stats.gov.cn）— GDP/CPI/PPI/PMI 官方数据',
            '中国证监会（csrc.gov.cn）— 证券监管政策',
            '中国银保监会 — 银行保险监管',
        ],
        'industry_policy': [
            '工信部（miit.gov.cn）— 行业产业政策',
            '发改委（ndrc.gov.cn）— 产业发展规划',
            '商务部（mofcom.gov.cn）— 贸易数据与政策',
            '海关总署（customs.gov.cn）— 进出口数据',
        ],
        'international': [
            '新华社（xinhuanet.com）— 国际新闻权威报道',
            '外交部（mfa.gov.cn）— 外交声明与立场',
            'Reuters（reuters.com）— 全球财经与政治',
            'Bloomberg（bloomberg.com）— 全球金融市场',
            'BBC News — 国际时政综合',
        ],
        'market_data': [
            '东方财富（eastmoney.com）— A股/港股行情',
            '雪球（xueqiu.com）— 投资社区与行情',
            '同花顺（10jqka.com.cn）— 行情数据',
            'Wind资讯 — 专业行情终端',
        ],
        'commodities_forex': [
            '上海期货交易所（shfe.com.cn）— 期货行情',
            '中国外汇交易中心（chinamoney.com.cn）— 汇率官方数据',
            '世界银行商品价格 — 大宗商品基准',
            'Investing.com — 全球商品行情',
        ],
    }

    # 内容时效性校验指令（附加到每个搜索结果中）
    CONTENT_FRESHNESS_RULES = (
        '【内容时效性校验规则（严格版）】搜索结果必须通过以下全部检查才能纳入分析：'
        '(1) 发布日期在有效期内（{max_age}天内）；'
        '(2) 内容所述数据的所属时期必须属于"当前应关注的财务时期" — '
        '当前为{ref_date}，应关注{relevant_fiscal}；'
        '任何更早季度/年度的财报数据均视为过时，绝对禁止作为"最新数据"引用；'
        '(3) 转载/回顾/盘点类文章需检查原始数据时期，旧数据的转载仍视为过时；'
        '(4) 政策/事件类新闻需确认是否仍在生效/持续中，已结束的事件仅作背景参考；'
        '(5) 标题含旧年份（距今超2年）+ 数据关键词的文章一律过滤。'
    )

    def __init__(self, engine: str = 'web_search', max_results: int = 5,
                 news_max_age_days: int = 30, reference_date: str = ''):
        """
        初始化搜索服务

        Args:
            engine: 搜索引擎（web_search/tavily/serpapi/bocha/brave）
            max_results: 每次搜索的最大结果数
            news_max_age_days: 新闻时效性（天），超过此天数的新闻不纳入
            reference_date: 参考日期（YYYY-MM-DD 格式），留空则使用当前日期
        """
        self.engine = engine
        self.max_results = max_results
        self.news_max_age_days = news_max_age_days

        # 使用对话实时日期而非固定当前日期
        if reference_date:
            try:
                self.reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
            except ValueError:
                self.reference_date = datetime.now()
        else:
            self.reference_date = datetime.now()

        self.current_year = self.reference_date.year
        self.current_month = self.reference_date.month
        self.cutoff_date = self.reference_date - timedelta(days=self.news_max_age_days)
        self.date_hint = self.reference_date.strftime('%Y年%m月')

        # 计算与当前分析时点相关的财务时期
        # 用于内容时效性校验：告诉 Agent 当前应关注哪个季度/年度的财务数据
        self.relevant_fiscal = self._compute_relevant_fiscal_period()

        # 生成内容时效性校验规则文本
        self.content_freshness_instruction = self.CONTENT_FRESHNESS_RULES.format(
            ref_date=self.reference_date.strftime('%Y年%m月%d日'),
            relevant_fiscal=self.relevant_fiscal,
            max_age=self.news_max_age_days,
        )

        logger.info(
            f"SearchService 初始化完成，引擎: {engine}, "
            f"参考日期: {self.reference_date.strftime('%Y-%m-%d')}, "
            f"新闻截止: {self.cutoff_date.strftime('%Y-%m-%d')}（{news_max_age_days}天内），"
            f"当前关注财务时期: {self.relevant_fiscal}"
        )

    def _compute_relevant_fiscal_period(self) -> str:
        """
        根据参考日期计算当前应关注的财务时期。

        逻辑：
        - 1-4月：上一年年报 + 当年Q1预期
        - 5-8月：当年Q1/半年报
        - 9-10月：当年半年报/三季报
        - 11-12月：当年三季报 + 全年预期
        """
        y = self.current_year
        m = self.current_month
        if m <= 4:
            return f'{y - 1}年年报和{y}年Q1业绩'
        elif m <= 8:
            return f'{y}年Q1和{y}年半年报业绩'
        elif m <= 10:
            return f'{y}年半年报和{y}年三季报业绩'
        else:
            return f'{y}年三季报和{y}年全年预期'

    def search_comprehensive_intel(self, stock_name: str, stock_code: str,
                                   industry: str = '', hot_keywords: Optional[Dict] = None) -> Dict:
        """
        执行多维度情报搜索（公司层面 + 宏观层面 + 时政层面 + 动态热点补充）

        Args:
            stock_name: 股票名称（如"贵州茅台"）
            stock_code: 股票代码（如"600519"）
            industry: 所属行业（可选，如"白酒"、"半导体"）
            hot_keywords: extract_hot_keywords() 的输出（可选，用于生成动态补充搜索）

        Returns:
            包含16+N个维度搜索结果的字典
        """
        logger.info(f"开始多维度情报搜索: {stock_name}({stock_code})")

        intel = {
            'stock_name': stock_name,
            'stock_code': stock_code,
            'industry': industry,
            'search_time': datetime.now().isoformat(),
            'reference_date': self.reference_date.strftime('%Y-%m-%d'),
            'news_cutoff_date': self.cutoff_date.strftime('%Y-%m-%d'),
            'news_max_age_days': self.news_max_age_days,
            'relevant_fiscal_period': self.relevant_fiscal,
            'content_freshness_instruction': self.content_freshness_instruction,
            'preferred_sources': self.PREFERRED_SOURCES,
            # 公司层面（5个维度）
            'latest_news': self._search_latest_news(stock_name),
            'risk_alerts': self._search_risk_alerts(stock_name),
            'performance_outlook': self._search_performance(stock_name),
            'industry_trends': self._search_industry(stock_name, industry),
            'tech_breakthroughs': self._search_technology(stock_name),
            # 宏观与国际层面（5个维度）
            'macro_policy': self._search_macro_policy(),
            'geopolitical': self._search_geopolitical(stock_name, industry),
            'global_markets': self._search_global_markets(),
            'commodities': self._search_commodities(industry),
            'forex_capital_flow': self._search_forex_capital_flow(),
            # 时政与政策层面（6个维度）
            'domestic_policy': self._search_domestic_policy(),
            'regulatory_actions': self._search_regulatory_actions(),
            'geopolitical_realtime': self._search_geopolitical_realtime(),
            'us_china_dynamics': self._search_us_china_dynamics(stock_name, industry),
            'supply_chain': self._search_supply_chain(industry),
            'consumer_society': self._search_consumer_society(),
        }

        # 动态热点补充搜索
        if hot_keywords:
            dynamic_searches = self.generate_dynamic_searches(hot_keywords)
            intel['dynamic_searches'] = dynamic_searches
            logger.info(f'已附加 {len(dynamic_searches)} 条动态补充搜索')

        logger.info(f"多维度情报搜索完成（16个维度 + 动态补充）")
        return intel
    
    def _search_latest_news(self, stock_name: str) -> Dict:
        """搜索最新消息（限定时间范围，优先官方数据源）"""
        query = f"site:cninfo.com.cn OR site:sse.com.cn OR site:szse.cn {stock_name} 公告 {self.date_hint}"
        fallback_query = f"{stock_name} 最新消息 公告 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '最新消息',
            'preferred_sources': self.PREFERRED_SOURCES['company_news'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的新闻',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（官方公告源）；'
                f'若结果不足，补充搜索: "{fallback_query}"。'
                f'必须验证每条结果的内容时期，忽略{self.news_max_age_days}天前的旧闻和过时数据的转载。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'从官方披露平台获取{stock_name}近{self.news_max_age_days}天内的最新公告和动态'
            }
        }

    def _search_risk_alerts(self, stock_name: str) -> Dict:
        """搜索风险排查（限定时间范围，优先官方数据源）"""
        query = f"site:cninfo.com.cn OR site:csrc.gov.cn {stock_name} 处罚 调查 {self.date_hint}"
        fallback_query = f"{stock_name} 减持 处罚 调查 诉讼 业绩下滑 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '风险排查',
            'preferred_sources': self.PREFERRED_SOURCES['company_news'] + ['中国证监会（csrc.gov.cn）'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的新闻',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（证监会/巨潮资讯）；'
                f'补充搜索: "{fallback_query}"。'
                f'必须验证风险事件是否仍在进行中，已结案的旧事件仅作背景参考。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'从监管平台排查{stock_name}近期风险事件（处罚/调查/减持）'
            }
        }

    def _search_performance(self, stock_name: str) -> Dict:
        """搜索业绩预期（限定时间范围，优先官方财报数据源）"""
        last_year = self.current_year - 1
        query = f"site:cninfo.com.cn {stock_name} {last_year}年报 {self.current_year}业绩"
        fallback_query = f"{stock_name} {last_year}年报 {self.current_year}业绩快报 业绩预告"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '业绩预期',
            'preferred_sources': self.PREFERRED_SOURCES['financial_report'],
            'time_filter': f'关注{last_year}年报和{self.current_year}最新业绩',
            'relevant_fiscal_period': self.relevant_fiscal,
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（巨潮资讯原始公告）；'
                f'补充搜索: "{fallback_query}"。'
                f'当前应重点关注：{self.relevant_fiscal}。'
                f'严格规则：更早季度的财报数据（如{last_year}年Q1/Q2/Q3，以及{last_year - 1}年及更早的所有数据）'
                f'已过时，绝对不得作为"最新业绩"引用，如需提及只能标注为"历史参考"。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'从巨潮资讯获取{stock_name}的最新官方财报和业绩信息（关注{self.relevant_fiscal}）'
            }
        }

    def _search_industry(self, stock_name: str, industry: str = '') -> Dict:
        """搜索行业热点（限定时间范围，优先行业主管部门数据源）"""
        industry_term = industry if industry else stock_name
        query = f"site:miit.gov.cn OR site:ndrc.gov.cn {industry_term} 政策 {self.date_hint}"
        fallback_query = f"{industry_term} 行业 热点 政策 {self.date_hint}"

        result = {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '行业热点',
            'preferred_sources': self.PREFERRED_SOURCES['industry_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的新闻',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（工信部/发改委官方政策）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'从工信部/发改委获取{industry_term}行业的最新官方政策和趋势'
            }
        }

        if industry and stock_name:
            result['supplementary_query'] = f'{stock_name} {industry} 竞争格局 市场份额 {self.current_year}'
            result['supplementary_explanation'] = f'了解{stock_name}在{industry}行业的竞争地位'

        return result

    def _search_technology(self, stock_name: str) -> Dict:
        """搜索技术突破（限定时间范围）"""
        query = f"site:cninfo.com.cn {stock_name} 专利 研发 {self.date_hint}"
        fallback_query = f"{stock_name} 技术突破 创新 专利 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '技术突破',
            'preferred_sources': self.PREFERRED_SOURCES['company_news'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的新闻',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（官方公告中的研发/专利信息）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'了解{stock_name}近期的技术创新和研发进展（优先官方公告）'
            }
        }

    # ========================================================================
    # 宏观与国际层面搜索
    # ========================================================================

    def _search_macro_policy(self) -> Dict:
        """搜索宏观经济政策（限定时间范围，优先官方数据源）"""
        query = f"site:gov.cn OR site:pbc.gov.cn 宏观经济 货币政策 财政政策 {self.date_hint}"
        fallback_query = f"中国 宏观经济 货币政策 财政政策 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '宏观经济政策',
            'preferred_sources': self.PREFERRED_SOURCES['macro_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的政策',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（中国政府网/央行官网）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻，注意区分政策发布日与生效日。'
            ),
            'supplementary_query': f'site:pbc.gov.cn 利率 降准 降息 {self.date_hint}',
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从中国政府网/央行获取当前宏观经济政策方向（货币政策、财政政策）'
            }
        }

    def _search_geopolitical(self, stock_name: str = '', industry: str = '') -> Dict:
        """搜索国际局势与地缘政治（限定时间范围，优先权威新闻源）"""
        query = f"site:xinhuanet.com OR site:reuters.com 国际局势 地缘政治 {self.date_hint}"
        fallback_query = f"国际局势 地缘政治 贸易摩擦 冲突 {self.date_hint}"

        result = {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '国际局势与地缘政治',
            'preferred_sources': self.PREFERRED_SOURCES['international'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的事件',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（新华社/Reuters 权威报道）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻，注意区分正在进行的事件与已结束的历史事件。'
                f'必须覆盖当前全球重大地缘热点（中东/伊朗/俄乌/台海/红海等），不能遗漏。'
            ),
            'supplementary_queries': [
                f'伊朗 以色列 中东局势 最新 {self.date_hint}',
                f'俄乌冲突 最新进展 {self.date_hint}',
            ],
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从新华社/Reuters获取影响市场的国际地缘政治事件'
            }
        }

        if stock_name or industry:
            target = stock_name or industry
            result['supplementary_queries'].append(
                f'{target} 海外业务 出口管制 制裁 地缘风险 {self.date_hint}'
            )
            result['supplementary_explanation'] = f'排查{target}面临的地缘政治风险'

        return result

    def _search_global_markets(self) -> Dict:
        """搜索全球市场走势（限定时间范围，优先专业财经数据源）"""
        query = f"site:eastmoney.com OR site:xueqiu.com 美股 全球市场 走势 {self.date_hint}"
        fallback_query = f"美股 欧股 全球市场 走势 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '全球市场联动',
            'preferred_sources': self.PREFERRED_SOURCES['market_data'],
            'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的市场走势',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（东方财富/雪球专业行情）；'
                f'补充搜索: "{fallback_query}"。'
                f'市场行情数据时效性要求高，只关注最近一周内的走势。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从专业财经平台获取全球主要市场走势及联动效应'
            }
        }

    def _search_commodities(self, industry: str = '') -> Dict:
        """搜索大宗商品价格（限定时间范围，优先官方交易所数据）"""
        base_query = f"site:shfe.com.cn OR site:investing.com 大宗商品 价格 {self.date_hint}"
        fallback_query = f"原油 黄金 铜 大宗商品 价格 {self.date_hint}"

        result = {
            'query': base_query,
            'fallback_query': fallback_query,
            'dimension': '大宗商品',
            'preferred_sources': self.PREFERRED_SOURCES['commodities_forex'],
            'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的价格走势',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{base_query}"（上期所/Investing 权威行情）；'
                f'补充搜索: "{fallback_query}"。'
                f'商品价格数据需要最新行情，忽略一周前的价格分析。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': fallback_query,
                'explanation': '获取大宗商品最新价格走势及对相关行业的影响'
            }
        }

        commodity_map = {
            '石油': '原油价格 OPEC',
            '能源': '原油 天然气 煤炭 价格',
            '钢铁': '铁矿石 钢材 价格',
            '有色': '铜 铝 锂 价格',
            '化工': '化工品 原油 价格',
            '农业': '粮食 猪肉 大豆 价格',
            '黄金': '黄金 白银 贵金属 价格',
            '新能源': '锂 钴 碳酸锂 价格',
            '半导体': '芯片 晶圆 硅片 价格',
            '汽车': '锂 钢材 原油 价格',
        }

        if industry:
            for key, commodity_query in commodity_map.items():
                if key in industry:
                    result['supplementary_query'] = f'{commodity_query} {self.date_hint}'
                    result['supplementary_explanation'] = f'获取与{industry}密切相关的商品价格走势'
                    break

        return result

    def _search_forex_capital_flow(self) -> Dict:
        """搜索汇率与资金流向（限定时间范围，优先官方外汇数据）"""
        query = f"site:chinamoney.com.cn OR site:eastmoney.com 人民币汇率 北向资金 {self.date_hint}"
        fallback_query = f"人民币汇率 北向资金 外资流向 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '汇率与资金流向',
            'preferred_sources': self.PREFERRED_SOURCES['commodities_forex'] + self.PREFERRED_SOURCES['market_data'],
            'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的数据',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（中国外汇交易中心/东方财富）；'
                f'补充搜索: "{fallback_query}"。'
                f'资金流向数据时效性要求高，只关注最近一周内的数据。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从外汇交易中心/东方财富获取汇率变化和外资流向数据'
            }
        }

    # ========================================================================
    # 时政与政策层面搜索（6个维度）
    # ========================================================================

    def _search_domestic_policy(self) -> Dict:
        """搜索国内重大政策（国务院、两会、改革等，优先政府官网）"""
        query = f"site:gov.cn 国务院 政策 改革 重大决策 {self.date_hint}"
        fallback_query = f"国务院 政策 改革 两会 重大决策 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '国内重大政策',
            'preferred_sources': self.PREFERRED_SOURCES['macro_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的政策',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（中国政府网官方政策原文）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻，注意政策是否仍在执行期。'
            ),
            'supplementary_query': f'site:ndrc.gov.cn 产业政策 补贴 {self.date_hint}',
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从中国政府网获取国务院近期发布的重大政策原文'
            }
        }

    def _search_regulatory_actions(self) -> Dict:
        """搜索央行与监管动态（优先央行/证监会官网）"""
        query = f"site:pbc.gov.cn OR site:csrc.gov.cn 降息 降准 金融监管 {self.date_hint}"
        fallback_query = f"央行 降息 降准 MLF 金融监管 证监会 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '央行与监管动态',
            'preferred_sources': self.PREFERRED_SOURCES['macro_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的消息',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（央行/证监会官方公告）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻。'
            ),
            'supplementary_query': f'site:csrc.gov.cn IPO 退市 注册制 {self.date_hint}',
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从央行/证监会官网获取最新货币政策操作和金融监管动态'
            }
        }

    def _search_geopolitical_realtime(self) -> Dict:
        """搜索地缘冲突实时动态（台海、中东、伊朗、俄乌、红海等，优先权威新闻源）"""
        query = f"site:xinhuanet.com OR site:mfa.gov.cn 台海 中东 伊朗 地缘冲突 {self.date_hint}"
        fallback_query = f"台海 中东 伊朗 俄乌 红海 地缘冲突 最新 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '地缘冲突实时',
            'preferred_sources': self.PREFERRED_SOURCES['international'],
            'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的动态',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（新华社/外交部权威报道）；'
                f'补充搜索: "{fallback_query}"。'
                f'只关注最近一周的冲突动态，区分正在进行的事件与已平息的历史事件。'
                f'特别关注：伊朗/以色列局势、红海/胡塞航运、俄乌冲突、台海形势。'
            ),
            'supplementary_queries': [
                f'site:mfa.gov.cn 外交 声明 {self.date_hint}',
                f'伊朗 以色列 军事 冲突 {self.date_hint}',
                f'红海 航运 胡塞 {self.date_hint}',
            ],
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从新华社/外交部追踪当前热点地缘冲突的最新官方报道'
            }
        }

    def _search_us_china_dynamics(self, stock_name: str = '', industry: str = '') -> Dict:
        """搜索中美博弈动态（优先官方/权威国际新闻源）"""
        query = f"site:mofcom.gov.cn OR site:reuters.com 中美关系 关税 科技制裁 {self.date_hint}"
        fallback_query = f"中美关系 关税 科技制裁 出口管制 {self.date_hint}"

        result = {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '中美博弈动态',
            'preferred_sources': self.PREFERRED_SOURCES['international'] + ['商务部（mofcom.gov.cn）'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的消息',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（商务部/Reuters 权威报道）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻，区分正在执行的制裁与已解除的措施。'
            ),
            'supplementary_queries': [
                f'中美 芯片禁令 出口管制 最新 {self.date_hint}',
            ],
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从商务部/Reuters获取中美博弈最新动态及对市场的影响'
            }
        }

        if stock_name or industry:
            target = stock_name or industry
            result['supplementary_queries'].append(
                f'{target} 中美 制裁 出口管制 {self.date_hint}'
            )
            result['supplementary_explanation'] = f'评估中美博弈对{target}的直接影响'

        return result

    def _search_supply_chain(self, industry: str = '') -> Dict:
        """搜索产业链与供应链动态（优先行业主管部门）"""
        industry_term = industry if industry else '产业链'
        query = f"site:miit.gov.cn {industry_term} 供应链 关键技术 自主可控 {self.date_hint}"
        fallback_query = f"{industry_term} 供应链 关键技术 自主可控 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '产业链与供应链',
            'preferred_sources': self.PREFERRED_SOURCES['industry_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的消息',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（工信部官方政策）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻。'
            ),
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': f'从工信部获取{industry_term}供应链风险和自主化进展的官方信息'
            }
        }

    # ========================================================================
    # 动态搜索生成（基于热点关键词）
    # ========================================================================

    def generate_dynamic_searches(self, hot_keywords_data: Dict) -> List[Dict]:
        """
        基于 macro_analysis.py extract_hot_keywords() 输出的热点关键词，
        生成额外的动态搜索指令，补充 16 维度搜索的覆盖盲区。

        Args:
            hot_keywords_data: extract_hot_keywords() 的输出，包含：
                - hot_entities: 高频实体关键词
                - dynamic_search_queries: 动态搜索建议
                - impact_chains: 事件→行业传导链
                - coverage_gaps: 覆盖盲区

        Returns:
            list[dict]: 每个包含 dimension/query/fallback_query/instruction/agent_call
        """
        if not hot_keywords_data:
            return []

        dynamic_results = []
        seen_keywords = set()

        # 1. 基于 coverage_gaps 生成补充搜索
        for gap in hot_keywords_data.get('coverage_gaps', []):
            kw = gap.get('keyword', '')
            if not kw or kw in seen_keywords:
                continue
            seen_keywords.add(kw)

            query = f'{kw} 最新动态 影响 {self.date_hint}'
            fallback_query = f'{kw} 局势 进展 {self.date_hint}'
            dynamic_results.append({
                'query': query,
                'fallback_query': fallback_query,
                'dimension': f'热点补充：{kw}',
                'preferred_sources': self.PREFERRED_SOURCES['international'],
                'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的动态',
                'content_freshness': self.content_freshness_instruction,
                'instruction': (
                    f'搜索: "{query}"。该关键词在当前热搜中多次出现但未被常规搜索覆盖，'
                    f'需了解其最新进展及对金融市场的潜在影响。'
                ),
                'source': 'dynamic_hot_keyword',
                'agent_call': {
                    'tool': 'web_search',
                    'searchTerm': query,
                    'explanation': f'追踪热点关键词"{kw}"的最新动态（动态补充搜索）',
                },
            })

        # 2. 基于 impact_chains 中 relevance=high 的生成关联搜索
        for chain in hot_keywords_data.get('impact_chains', []):
            if chain.get('relevance_to_target') != 'high':
                continue
            trigger = chain.get('trigger_event', '')
            if not trigger or trigger in seen_keywords:
                continue
            seen_keywords.add(trigger)

            sectors = chain.get('affected_sectors', [])
            matched = chain.get('matched_sectors', sectors[:2])
            query = f'{trigger} {" ".join(matched)} 影响 市场 {self.date_hint}'
            dynamic_results.append({
                'query': query,
                'fallback_query': f'{trigger} 金融市场 影响 {self.date_hint}',
                'dimension': f'影响传导：{trigger}→{"/".join(matched)}',
                'preferred_sources': self.PREFERRED_SOURCES['international'],
                'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的动态',
                'content_freshness': self.content_freshness_instruction,
                'instruction': (
                    f'搜索: "{query}"。热点事件"{trigger}"可能通过'
                    f'{"/".join(sectors[:3])}等链条影响分析标的，需评估具体影响程度。'
                ),
                'source': 'dynamic_impact_chain',
                'agent_call': {
                    'tool': 'web_search',
                    'searchTerm': query,
                    'explanation': f'评估"{trigger}"事件通过{"/".join(matched)}对分析标的的影响',
                },
            })

        # 3. 基于 dynamic_search_queries 中 priority=high 的生成搜索
        for dq in hot_keywords_data.get('dynamic_search_queries', []):
            if dq.get('priority') != 'high':
                continue
            kw = dq.get('keyword', '')
            if kw in seen_keywords:
                continue
            seen_keywords.add(kw)

            query = dq.get('query', '')
            if not query:
                continue
            dynamic_results.append({
                'query': query,
                'fallback_query': f'{kw} 最新 {self.date_hint}',
                'dimension': f'热点追踪：{kw}',
                'preferred_sources': self.PREFERRED_SOURCES['international'],
                'time_filter': f'仅关注最近{min(self.news_max_age_days, 7)}天的动态',
                'content_freshness': self.content_freshness_instruction,
                'instruction': dq.get('explanation', f'追踪热点关键词"{kw}"'),
                'source': 'dynamic_query',
                'agent_call': {
                    'tool': 'web_search',
                    'searchTerm': query,
                    'explanation': dq.get('explanation', f'追踪热点关键词"{kw}"的最新动态'),
                },
            })

        logger.info(f'生成 {len(dynamic_results)} 条动态补充搜索指令')
        return dynamic_results

    def _search_consumer_society(self) -> Dict:
        """搜索社会民生与消费趋势（优先统计局/商务部数据）"""
        query = f"site:stats.gov.cn OR site:mofcom.gov.cn 消费 就业 人口 {self.date_hint}"
        fallback_query = f"消费趋势 就业 人口 社会热点 {self.date_hint}"

        return {
            'query': query,
            'fallback_query': fallback_query,
            'dimension': '社会民生与消费',
            'preferred_sources': self.PREFERRED_SOURCES['macro_policy'] + self.PREFERRED_SOURCES['industry_policy'],
            'time_filter': f'仅关注{self.cutoff_date.strftime("%Y-%m-%d")}之后的消息',
            'content_freshness': self.content_freshness_instruction,
            'instruction': (
                f'优先搜索: "{query}"（统计局/商务部官方数据）；'
                f'补充搜索: "{fallback_query}"。'
                f'忽略{self.news_max_age_days}天前的旧闻，注意统计数据的所属时期。'
            ),
            'supplementary_query': f'site:stats.gov.cn 居民收入 消费支出 内需 {self.date_hint}',
            'agent_call': {
                'tool': 'web_search',
                'searchTerm': query,
                'explanation': '从统计局/商务部获取消费趋势和社会民生变化的官方数据'
            }
        }


def main():
    parser = argparse.ArgumentParser(description='多维度情报搜索工具（严格时效性 + 官方数据源 + 脚本热点协同 + 动态关键词注入）')
    parser.add_argument('--stock-name', required=True, help='股票名称（如"贵州茅台"）')
    parser.add_argument('--stock-code', required=True, help='股票代码（如"600519"）')
    parser.add_argument('--industry', default='', help='所属行业（如"白酒"、"半导体"，用于定制搜索）')
    parser.add_argument('--output', required=True, help='输出文件路径（JSON）')
    parser.add_argument('--engine', default='web_search', help='搜索引擎')
    parser.add_argument('--news-max-age-days', type=int, default=30, help='新闻时效（天），超过此天数的新闻不纳入分析（默认30天）')
    parser.add_argument('--reference-date', default='', help='参考日期（YYYY-MM-DD），用于时效性过滤，默认为当前日期')
    parser.add_argument('--hot-keywords-json', default='', help='macro_analysis.py 输出的热点关键词 JSON 路径（可选，用于动态搜索补充）')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 加载热点关键词数据（可选）
    hot_keywords = None
    if args.hot_keywords_json:
        try:
            with open(args.hot_keywords_json, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                hot_keywords = macro_data.get('hot_keywords', None)
                if hot_keywords:
                    logger.info(f'已加载热点关键词数据: {args.hot_keywords_json}')
                else:
                    logger.warning(f'热点关键词文件中未找到 hot_keywords 字段')
        except Exception as e:
            logger.warning(f'加载热点关键词失败: {e}')

    # 创建搜索服务
    service = SearchService(
        engine=args.engine,
        news_max_age_days=args.news_max_age_days,
        reference_date=args.reference_date,
    )

    # 执行多维度搜索
    intel = service.search_comprehensive_intel(
        args.stock_name, args.stock_code, args.industry,
        hot_keywords=hot_keywords,
    )

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(intel, f, ensure_ascii=False, indent=2)

    logger.info(f"=" * 60)
    logger.info(f"搜索策略已生成: {output_path}")
    logger.info(f"参考日期: {service.reference_date.strftime('%Y-%m-%d')}, 新闻截止: {service.cutoff_date.strftime('%Y-%m-%d')}")
    logger.info(f"当前关注财务时期: {service.relevant_fiscal}")
    logger.info(f"=" * 60)

    # 打印搜索执行指令（给 Agent 参考）
    print(f"\n搜索执行指令（16个维度 + 动态补充，仅纳入{args.news_max_age_days}天内新闻）：")
    print(f"当前关注财务时期: {service.relevant_fiscal}")
    print(f"内容时效性校验: {service.content_freshness_instruction}\n")

    def _print_dimension(dimension_data):
        """打印单个搜索维度"""
        if not isinstance(dimension_data, dict) or 'agent_call' not in dimension_data:
            return
        print(f"## {dimension_data['dimension']}")
        print(f"  搜索: {dimension_data['agent_call'].get('searchTerm', '')}")
        if dimension_data.get('preferred_sources'):
            print(f"  推荐数据源: {', '.join(dimension_data['preferred_sources'][:3])}")
        if dimension_data.get('fallback_query'):
            print(f"  备选搜索: {dimension_data['fallback_query']}")
        if dimension_data.get('supplementary_queries'):
            for sq in dimension_data['supplementary_queries']:
                print(f"  补充搜索: {sq}")
        elif dimension_data.get('supplementary_query'):
            print(f"  补充搜索: {dimension_data['supplementary_query']}")
        if dimension_data.get('time_filter'):
            print(f"  {dimension_data['time_filter']}")
        print()

    print("=== 公司层面（5个维度）===\n")
    for key in ['latest_news', 'risk_alerts', 'performance_outlook', 'industry_trends', 'tech_breakthroughs']:
        _print_dimension(intel.get(key, {}))

    print("=== 宏观与国际层面（5个维度）===\n")
    for key in ['macro_policy', 'geopolitical', 'global_markets', 'commodities', 'forex_capital_flow']:
        _print_dimension(intel.get(key, {}))

    print("=== 时政与政策层面（6个维度）===\n")
    for key in ['domestic_policy', 'regulatory_actions', 'geopolitical_realtime', 'us_china_dynamics', 'supply_chain', 'consumer_society']:
        _print_dimension(intel.get(key, {}))

    # 打印动态补充搜索
    dynamic = intel.get('dynamic_searches', [])
    if dynamic:
        print(f"=== 动态热点补充搜索（{len(dynamic)}条，基于热点关键词）===\n")
        for ds in dynamic:
            _print_dimension(ds)

    print(f"\n搜索策略已保存到: {output_path}")
    print(f"Agent 应根据以上指令依次调用 web_search 工具，并将结果整合到投资分析中。")
    print(f"注意：请忽略 {service.cutoff_date.strftime('%Y-%m-%d')} 之前的旧闻。")
    print(f"优先使用官方/权威数据源（如 cninfo.com.cn、gov.cn、pbc.gov.cn、stats.gov.cn）。")
    print(f"每条搜索结果必须校验内容所属时期，过时的转载/回顾文章不应作为最新数据引用。")


if __name__ == '__main__':
    main()
