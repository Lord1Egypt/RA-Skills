"""
知乎 (Zhihu.com) 内容格式化脚本 🐱
纯内容适配，不碰 API！
"""

import re


class ZhihuFormatter:
    def __init__(self):
        pass

    def format_article(self, title: str, content: str, topics: list = None) -> dict:
        if topics is None:
            topics = self.extract_topics(content)

        optimized = self._rewrite_for_zhihu(title, content)

        return {
            "platform": "知乎",
            "title": optimized["title"],
            "content": optimized["content"],
            "topics": topics[:5],
            "suggestions": self._get_suggestions(content),
        }

    def _rewrite_for_zhihu(self, title: str, content: str) -> dict:
        # 知乎风格：问答式、个人经历感
        new_title = title
        if "如何" not in title and "为什么" not in title and "?" not in title:
            new_title = f"如何看待{title}？"

        # 增强"个人经验"感
        new_content = f"先说结论：\n\n" + content
        new_content += "\n\n---\n\n以上是我个人的经验总结，欢迎在评论区讨论喵～ 🐱"

        return {"title": new_title, "content": new_content}

    def _get_suggestions(self, content: str) -> list:
        s = []
        if len(content) < 3000:
            s.append("💡 知乎热榜文章通常 3000 字以上")
        s.append("💡 多用'个人经历'增强可信度")
        s.append("💡 善用引用格式和加粗")
        s.append("💡 开头前 100 字决定推荐量")
        return s

    def extract_topics(self, content: str) -> list:
        topics = ["人工智能", "深度学习", "程序员", "互联网", "效率提升", "工具推荐", "Python", "数据分析"]
        return [t for t in topics if t.lower() in content.lower()][:5]
