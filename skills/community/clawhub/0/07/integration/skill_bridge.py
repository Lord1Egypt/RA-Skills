#!/usr/bin/env python3
"""
Agent Reach 与 5个 AI 技能的安全桥接
将 Agent Reach 获取的数据安全地传递给本地 AI 技能处理
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import hashlib
from datetime import datetime

# 添加技能路径
SKILLS_BASE = Path.home() / "ai-skills"
sys.path.insert(0, str(SKILLS_BASE))

try:
    from skill_2_search.web_search import CachedSearch
    from skill_1_memory.ai_memory import AIMemory
    from skill_5_summary.summary_review import ContentSummarizer
    SKILLS_AVAILABLE = True
except ImportError:
    SKILLS_AVAILABLE = False
    print("⚠️  警告: AI 技能未找到，将仅使用缓存模式")


class AgentReachBridge:
    """Agent Reach 与 AI 技能的安全桥接"""

    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir or "~/agent-reach-secure/cache")
        self.cache_dir.expanduser().mkdir(parents=True, exist_ok=True)

        # 初始化技能（如果可用）
        if SKILLS_AVAILABLE:
            self.search_skill = CachedSearch(cache_dir=str(self.cache_dir / "search"))
            self.memory_skill = AIMemory(db_path=str(self.cache_dir / "memory.db"))
            self.summary_skill = ContentSummarizer()

        # 数据清洗规则
        self.sanitize_rules = {
            'remove_patterns': [
                r'<script[^>]*>.*?</script>',
                r'<iframe[^>]*>.*?</iframe>',
            ],
            'max_length': 100000,  # 100KB
            'allowed_fields': [
                'text', 'url', 'author', 'timestamp', 'platform',
                'likes', 'shares', 'comments'
            ]
        }

    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """清洗和验证数据"""
        import re

        # 1. 只保留允许的字段
        sanitized = {k: v for k, v in data.items()
                    if k in self.sanitize_rules['allowed_fields']}

        # 2. 移除危险模式
        for field in ['text', 'author']:
            if field in sanitized:
                for pattern in self.sanitize_rules['remove_patterns']:
                    sanitized[field] = re.sub(pattern, '', sanitized[field], flags=re.IGNORECASE)

        # 3. 长度限制
        for field, value in sanitized.items():
            if isinstance(value, str) and len(value) > self.sanitize_rules['max_length']:
                sanitized[field] = value[:self.sanitize_rules['max_length']] + "... [truncated]"

        # 4. 添加元数据
        sanitized['sanitized_at'] = datetime.now().isoformat()
        sanitized['data_hash'] = hashlib.sha256(json.dumps(sanitized, sort_keys=True).encode()).hexdigest()[:16]

        return sanitized

    def fetch_from_agent_reach(self, platform: str, query: str, **kwargs) -> List[Dict]:
        """从 Agent Reach 获取数据（模拟）"""
        # 实际使用时，这里会调用 Agent Reach 的 API
        # 现在只是模拟返回数据
        return [{
            'text': f"Sample content from {platform}",
            'url': f"https://{platform}.com/sample",
            'author': 'sample_user',
            'timestamp': datetime.now().isoformat(),
            'platform': platform
        }]

    def cache_data(self, platform: str, query: str, data: List[Dict]) -> bool:
        """缓存数据到本地搜索技能"""
        if not SKILLS_AVAILABLE:
            return False

        try:
            # 将数据转换为搜索结果格式
            for item in data:
                cache_key = hashlib.md5(f"{platform}:{query}:{item.get('url', '')}".encode()).hexdigest()

                # 存储到搜索技能的缓存
                # 这里简化处理，实际应该调用 CachedSearch 的方法
                cache_file = self.cache_dir / f"{cache_key}.json"
                with open(cache_file, 'w') as f:
                    json.dump(item, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"❌ 缓存失败: {e}")
            return False

    def store_to_memory(self, data: List[Dict], tags: List[str] = None) -> bool:
        """存储到记忆技能"""
        if not SKILLS_AVAILABLE:
            return False

        try:
            for item in data:
                content = f"From {item.get('platform', 'unknown')}: {item.get('text', '')}"

                # 添加到记忆
                self.memory_skill.add(
                    content=content,
                    tags=(tags or []) + [item.get('platform', 'unknown')]
                )

            return True
        except Exception as e:
            print(f"❌ 存储到记忆失败: {e}")
            return False

    def summarize_data(self, data: List[Dict], content_type: str = 'general') -> str:
        """总结数据"""
        if not SKILLS_AVAILABLE:
            return f"Summary of {len(data)} items"

        try:
            # 合并所有文本
            combined_text = "\n\n".join([
                f"{item.get('text', '')} (来源: {item.get('platform', 'unknown')})"
                for item in data
            ])

            # 使用总结技能
            result = self.summary_skill.summarize(combined_text, content_type)
            return result.get('summary', '总结生成失败')

        except Exception as e:
            print(f"❌ 总结失败: {e}")
            return f"包含 {len(data)} 条数据"

    def safe_pipeline(self, platform: str, query: str, **kwargs) -> Dict[str, Any]:
        """安全处理管道：获取 → 清洗 → 缓存 → 存储 → 总结"""
        print(f"🔍 从 {platform} 获取数据: {query}")
        print()

        # 1. 获取数据
        raw_data = self.fetch_from_agent_reach(platform, query, **kwargs)
        print(f"✅ 获取到 {len(raw_data)} 条原始数据")

        # 2. 清洗数据
        sanitized_data = [self.sanitize_data(item) for item in raw_data]
        print(f"✅ 数据清洗完成")

        # 3. 缓存数据
        if self.cache_data(platform, query, sanitized_data):
            print(f"✅ 数据已缓存")

        # 4. 存储到记忆
        if self.store_to_memory(sanitized_data, tags=[platform, query]):
            print(f"✅ 数据已存储到记忆")

        # 5. 生成总结
        summary = self.summarize(sanitized_data, content_type=platform)
        print(f"✅ 总结已生成")

        print()
        return {
            'count': len(sanitized_data),
            'summary': summary,
            'cached': True,
            'platform': platform,
            'query': query
        }

    def search_cached_data(self, query: str) -> List[Dict]:
        """搜索已缓存的数据"""
        if not SKILLS_AVAILABLE:
            return []

        # 使用搜索技能搜索缓存
        results = self.search_skill.search(query, engine='local', max_results=10)
        return results.get('results', [])


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agent Reach 安全桥接")
    parser.add_argument('action', choices=['fetch', 'search', 'pipeline'],
                       help='操作类型')
    parser.add_argument('--platform', required=True, help='平台名称')
    parser.add_argument('--query', required=True, help='搜索查询')
    parser.add_argument('--cache', action='store_true', help='缓存结果')

    args = parser.parse_args()

    bridge = AgentReachBridge()

    if args.action == 'fetch':
        data = bridge.fetch_from_agent_reach(args.platform, args.query)
        sanitized = [bridge.sanitize_data(item) for item in data]

        print(json.dumps(sanitized, indent=2, ensure_ascii=False))

        if args.cache:
            bridge.cache_data(args.platform, args.query, sanitized)

    elif args.action == 'search':
        results = bridge.search_cached_data(args.query)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.action == 'pipeline':
        result = bridge.safe_pipeline(args.platform, args.query)

        print("=" * 60)
        print("处理结果")
        print("=" * 60)
        print(f"平台: {result['platform']}")
        print(f"查询: {result['query']}")
        print(f"数据量: {result['count']} 条")
        print(f"已缓存: {'是' if result['cached'] else '否'}")
        print()
        print("总结:")
        print(result['summary'])
        print("=" * 60)


if __name__ == "__main__":
    main()
