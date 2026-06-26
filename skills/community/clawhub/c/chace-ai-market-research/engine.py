#!/usr/bin/env python3
"""
ai-market-research 核心编排引擎

职责:
1. 接收任务参数 (JSON via stdin)
2. 调用 crawl4ai 抓取指定 or 自动发现来源
3. 调用 trendradar 获取关联热点
4. 调用 product-research 分析框架
5. 整合结果并生成报告
6. 保存到 agentmemory
"""

import sys
import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ai-market-research')

# 工作目录
WORKSPACE = Path('/Users/tom/.openclaw/workspace')
OUTPUT_DIR = WORKSPACE / 'output' / 'ai-market-research'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class MarketResearchEngine:
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.topic = params['topic']
        self.depth = params.get('depth', 'standard')
        self.sources = params.get('sources', [])
        self.output_format = params.get('output_format', 'markdown')
        self.compare_previous = params.get('compare_previous', True)

        self.artifacts = {}
        self.report_data = {}

        logger.info(f"启动研究: topic='{self.topic}', depth={self.depth}")

    async def run(self) -> str:
        """执行完整研究流程，返回报告路径"""
        try:
            # 阶段 1: 数据采集
            await self._collect_data()

            # 阶段 2: 历史对比
            if self.compare_previous:
                await self._compare_with_history()

            # 阶段 3: 分析与整合
            await self._analyze()

            # 阶段 4: 生成报告
            report_path = await self._generate_report()

            # 阶段 5: 记忆存储
            await self._store_memory()

            return report_path
        except Exception as e:
            logger.error(f"执行失败: {e}", exc_info=True)
            raise

    async def _collect_data(self):
        """调用 crawl4ai 和 trendradar 采集数据"""
        logger.info("📡 开始数据采集...")

        # 1. 获取热点舆情
        try:
            # 实际实现应调用 trendradar MCP 工具，这里使用模拟数据确保 standalone 可运行
            trend_data = await self._simulate_trendradar_search()
            self.artifacts['trendradar'] = trend_data
            logger.info(f"✅ TrendRadar: 获取 {len(trend_data.get('news', []))} 条新闻")
        except Exception as e:
            logger.warning(f"TrendRadar 调用失败: {e}")
            self.artifacts['trendradar'] = {'news': [], 'error': str(e)}

        # 2. 深度网页抓取
        try:
            crawl_results = await self._run_crawl4ai()
            self.artifacts['crawl4ai'] = crawl_results
            logger.info(f"✅ Crawl4AI: 抓取 {len(crawl_results)} 个页面")
        except Exception as e:
            logger.warning(f"Crawl4AI 调用失败: {e}")
            self.artifacts['crawl4ai'] = {'pages': [], 'error': str(e)}

    async def _simulate_trendradar_search(self) -> Dict:
        """模拟 trendradar 搜索 (实际需通过 MCP 调用)"""
        # 实际实现应调用 OpenClaw MCP 工具:
        # await call_mcp_tool('trendradar', 'search_news', {'query': self.topic, ...})
        # 返回模拟数据供 standalone 测试使用
        mock_news = [
            {'title': f'{self.topic} 市场爆发式增长', 'platform': 'weibo', 'rank': 1},
            {'title': f'{self.topic} 行业分析报告', 'platform': 'zhihu', 'rank': 2},
            {'title': f'{self.topic} 最新动态：政策支持', 'platform': 'baidu', 'rank': 3},
            {'title': f'{self.topic} 技术突破引关注', 'platform': 'toutiao', 'rank': 4},
            {'title': f'{self.topic} 投资热潮持续', 'platform': 'wallstreetcn-hot', 'rank': 5},
        ]
        return {
            'query': self.topic,
            'timestamp': datetime.now().isoformat(),
            'news': mock_news
        }

    async def _run_crawl4ai(self) -> List[Dict]:
        """执行 crawl4ai 抓取"""
        pages = []
        # 如果未指定 sources，根据 topic 自动发现 (需要 google 搜索 + 筛选)
        urls = self.sources or await self._discover_sources()

        # 限制数量基于 depth
        limits = {'quick': 5, 'standard': 20, 'deep': 50}
        max_urls = limits.get(self.depth, 20)
        urls = urls[:max_urls]

        for url in urls:
            try:
                # 实际调用 crawl4ai MCP 工具
                result = await self._crawl_page(url)
                if result:
                    pages.append(result)
            except Exception as e:
                logger.debug(f"抓取失败 {url}: {e}")
                continue

        return pages

    async def _discover_sources(self) -> List[str]:
        """自动发现相关来源 (简化版)"""
        # 实际实现可结合 Google 搜索 + site: 筛选
        # 这里返回空列表让用户指定 sources
        logger.warning("未指定 sources，自动发现功能待实现")
        return []

    async def _crawl_page(self, url: str) -> Dict:
        """抓取单个页面 (模拟)"""
        # 实际实现应调用 OpenClaw MCP:
        # await call_mcp_tool('crawl4ai', 'crawl', {'url': url, 'extract_mode': 'markdown'})
        # 这里返回模拟数据用于测试
        return {
            'url': url,
            'title': f'{self.topic} - {url.split("//")[1].split("/")[0]}',
            'content': f"{self.topic} 的详细分析内容（来自 {url}）...",
            'timestamp': datetime.now().isoformat()
        }

    async def _compare_with_history(self):
        """与历史研究对比"""
        logger.info("📊 历史对比中...")
        try:
            try:
                from agentmemory import memory_search
                results = memory_search(query=self.topic, limit=5, corpus='memory')
                # 确保 historical 是 dict 格式，report_data 期望 {'results': [...]}
                if isinstance(results, dict):
                    self.report_data['historical'] = results
                    count = len(results.get('results', []))
                else:
                    self.report_data['historical'] = {'results': results}
                    count = len(results)
                logger.info(f"✅ 找到 {count} 条历史记录")
            except ImportError:
                logger.warning("agentmemory 未安装，跳过历史对比")
                self.report_data['historical'] = {'results': []}
        except Exception as e:
            logger.warning(f"历史检索失败: {e}")
            self.report_data['historical'] = {'results': []}

    async def _analyze(self):
        """调用 product-research 分析框架生成结论"""
        logger.info("🧠 执行分析...")
        # 融合 crawl4ai 内容 + trendradar 热点 + 历史对比
        # 调用 product-research 技能的分析器
        # 简化: 这里生成一个雏形
        # 从抓取内容中简单提取竞品信息（实际应使用 NLP/LLM 归纳）
        pages = self.artifacts.get('crawl4ai', [])
        competitors = list(set([p.get('title', '').split('-')[0].strip() for p in pages if p.get('title')]))[:5]

        analysis = {
            'topic': self.topic,
            'summary': f'{self.topic} 的市场研究摘要（{self.depth} 深度）',
            'trends': self.artifacts.get('trendradar', {}).get('news', [])[:5],
            'competitors': competitors,
            'opportunities': [
                f'{self.topic} 领域热度上升',
                '政策支持力度加大',
                '技术迭代加速带来新机会'
            ],
            'risks': [
                '市场竞争加剧',
                '技术路线不确定性',
                '法规变化风险'
            ],
            'recommendations': [
                '持续监控竞品动态',
                '关注政策导向',
                '建立技术护城河'
            ],
        }
        self.report_data['analysis'] = analysis

    async def _generate_report(self) -> Path:
        """生成最终报告文件"""
        logger.info("📝 生成报告中...")
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        filename = f"{self.topic.replace(' ', '_')}_{self.depth}_{now.strftime('%Y%m%d_%H%M')}.{self.output_format}"
        report_path = OUTPUT_DIR / filename

        # 渲染模板
        template = self._load_template()
        content = self._render_report(template)

        report_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 报告已生成: {report_path}")
        return report_path

    def _load_template(self) -> str:
        """加载报告模板"""
        if self.output_format == 'markdown':
            return """# {topic} 市场研究报告

**生成时间**: {timestamp}
**研究深度**: {depth}

## 📰 热点追踪

{trends_section}

## 🔍 深度分析

{analysis_section}

## 📈 历史对比

{historical_section}

## 💡 关键洞察

{insights_section}

---

*报告由 OpenClaw ai-market-research 技能自动生成*
"""
        return "# {topic}\n\n{content}"

    def _render_report(self, template: str) -> str:
        """填充模板"""
        analysis = self.report_data.get('analysis', {})

        trends = analysis.get('trends', [])
        trends_md = "\n".join([f"- **{t['title']}** ({t['platform']} 第{t['rank']}名)" for t in trends[:10]]) if trends else "_暂无热点数据_"

        analysis_md = f"""
### 研究摘要
{analysis.get('summary', 'N/A')}

### 主要机会 ✅
{chr(10).join([f'✅ {o}' for o in analysis.get('opportunities', [])])}

### 关键风险 ⚠️
{chr(10).join([f'⚠️ {r}' for r in analysis.get('risks', [])])}

### 行动建议 💡
{chr(10).join([f'💡 {r}' for r in analysis.get('recommendations', [])])}

### 识别竞品
{chr(10).join(['- ' + c for c in analysis.get('competitors', [])]) if analysis.get('competitors') else '暂无'}
"""

        historical = self.report_data.get('historical', {}).get('results', [])
        if historical:
            hist_md = "\n".join([f"- {h.get('path', '未知')} (时间: {h.get('timestamp', 'N/A')})" for h in historical[:3]])
        else:
            hist_md = "_无历史研究记录_"

        return template.format(
            topic=self.topic,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'),
            depth=self.depth,
            trends_section=trends_md,
            analysis_section=analysis_md,
            historical_section=hist_md,
            insights_section="_AI 洞察待后续集成_"
        )

    async def _store_memory(self):
        """保存关键结论到 agentmemory"""
        logger.info("💾 存储记忆中...")
        try:
            try:
                from agentmemory import memory_save
                memory_save(
                    content=f"市场研究: {self.topic} - {self.report_data.get('analysis', {}).get('summary', 'N/A')}",
                    type='fact',
                    concepts='market-research,' + self.topic,
                    files=str(self.artifacts.keys())
                )
                logger.info("✅ 记忆存储完成")
            except ImportError:
                logger.warning("agentmemory 未安装，跳过记忆存储")
        except Exception as e:
            logger.warning(f"记忆存储失败: {e}")

def main():
    """入口: 从 stdin 读取 JSON 参数"""
    try:
        raw = sys.stdin.read()
        params = json.loads(raw)
    except Exception as e:
        logger.error(f"参数解析失败: {e}")
        sys.exit(1)

    engine = MarketResearchEngine(params)
    try:
        report_path = asyncio.run(engine.run())
        print(f"✅ 研究完成\n📄 报告: {report_path}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()