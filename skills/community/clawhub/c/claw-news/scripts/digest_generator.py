"""
Claw-News Digest Generator
简报生成模块
"""

import json
from typing import List, Dict
from datetime import datetime, timedelta
from search_engine import SearchResult
from result_aggregator import ResultAggregator


class DigestGenerator:
    """简报生成器"""
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path or self._get_default_template_path()
    
    def _get_default_template_path(self) -> str:
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "assets", "digest_template.md")
    
    def generate(self, categorized_results: Dict[str, List[SearchResult]], 
                 interests_data: Dict, settings: Dict = None) -> str:
        """
        生成 Markdown 简报
        
        Args:
            categorized_results: 分类后的搜索结果
            interests_data: 关注列表数据
            settings: 设置信息
        """
        settings = settings or {}
        
        # 获取时间范围
        lookback_hours = settings.get('search_lookback_hours', 24)
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=lookback_hours)
        
        # 构建统计信息
        stats = ResultAggregator().get_statistics(categorized_results)
        
        # 构建 interests 映射
        interests_map = {
            i['id']: i for i in interests_data.get('interests', [])
        }
        
        # 开始生成简报
        lines = []
        
        # 标题
        lines.append("# 📰 Claw-News 每日简报\n")
        lines.append(f"**时间范围**: {start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 按优先级排序分类
        sorted_categories = self._sort_categories(categorized_results, interests_map)
        
        # 生成各分类内容
        total_news = 0
        for interest_id in sorted_categories:
            results = categorized_results.get(interest_id, [])
            if not results:
                continue
            
            interest_info = interests_map.get(interest_id, {})
            interest_value = interest_info.get('value', '其他')
            interest_type = interest_info.get('type', 'topic')
            
            # 类型 emoji
            type_emoji = {"topic": "🔥", "person": "👤", "keyword": "🔑"}.get(interest_type, "📌")
            priority = interest_info.get('priority', 'medium')
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
            
            lines.append(f"---\n")
            lines.append(f"## {type_emoji} {interest_value} ({len(results)}条) {priority_emoji}\n")
            
            for i, result in enumerate(results[:10], 1):  # 每类最多 10 条
                lines.append(f"### {i}. [{result.title}]({result.url})")
                lines.append(f"**来源**: {result.source} | **时间**: {self._format_time(result.published_at)}")
                
                # 摘要
                summary = result.summary.strip()
                if len(summary) > 200:
                    summary = summary[:200] + "..."
                if summary:
                    lines.append(f"\n{summary}\n")
                else:
                    lines.append("")
                
                total_news += 1
            
            # 如果有更多结果被截断
            if len(results) > 10:
                lines.append(f"*...还有 {len(results) - 10} 条相关新闻*\n")
        
        # 统计信息
        lines.append("---\n")
        lines.append("## 📊 简报统计\n")
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 关注主题 | {len(categorized_results)} 个 |")
        lines.append(f"| 新闻总数 | {stats['total_results']} 条 |")
        lines.append(f"| 涉及来源 | {len(stats['by_source'])} 个 |")
        
        # API 使用情况
        api_usage = []
        for api, count in sorted(stats['by_api'].items(), key=lambda x: -x[1]):
            api_display = (api or "unknown").capitalize()
            api_usage.append(f"{api_display} ({count}次)")
        if api_usage:
            lines.append(f"| API 使用 | {' / '.join(api_usage)} |")
        
        lines.append("")
        
        # 页脚
        lines.append("---\n")
        lines.append("💡 **提示**: 回复 `newsman add <关键词>` 添加新关注 | `newsman list` 查看列表 | `newsman run` 立即执行")
        lines.append("")
        
        return "\n".join(lines)
    
    def _sort_categories(self, categorized_results: Dict, 
                         interests_map: Dict) -> List[str]:
        """按优先级排序分类"""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        
        categories = list(categorized_results.keys())
        categories.sort(key=lambda cid: (
            priority_order.get(interests_map.get(cid, {}).get('priority', 'medium'), 2),
            -len(categorized_results.get(cid, []))  # 同优先级按数量倒序
        ))
        
        return categories
    
    def _format_time(self, time_str: str) -> str:
        """格式化时间字符串"""
        if not time_str:
            return "未知"
        
        try:
            # 尝试多种格式
            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', 
                       '%Y-%m-%d', '%m-%d %H:%M']:
                try:
                    dt = datetime.strptime(time_str[:19], fmt)
                    return dt.strftime('%m-%d %H:%M')
                except:
                    continue
            
            # 尝试 ISO 格式
            from dateutil import parser
            dt = parser.parse(time_str)
            return dt.strftime('%m-%d %H:%M')
        except:
            return time_str[:16] if len(time_str) > 16 else time_str


def main():
    """测试简报生成"""
    import sys
    import os
    
    # 创建测试数据
    test_results = {
        "abc123": [
            SearchResult(
                title="OpenAI 发布 GPT-5 预览版",
                url="https://example.com/1",
                summary="OpenAI 今日凌晨意外放出 GPT-5 技术预览，据称在推理能力上实现重大突破...",
                source="TechCrunch",
                published_at="2026-02-21T14:30:00",
                search_api="kimi"
            ),
            SearchResult(
                title="Google DeepMind 推出新模型",
                url="https://example.com/2",
                summary="DeepMind 研究团队发布了新一代多模态模型...",
                source="The Verge",
                published_at="2026-02-21T22:15:00",
                search_api="kimi"
            )
        ]
    }
    
    test_interests = {
        "interests": [
            {"id": "abc123", "type": "topic", "value": "人工智能", "priority": "high"}
        ]
    }
    
    generator = DigestGenerator()
    digest = generator.generate(test_results, test_interests)
    
    print(digest)


if __name__ == "__main__":
    main()
