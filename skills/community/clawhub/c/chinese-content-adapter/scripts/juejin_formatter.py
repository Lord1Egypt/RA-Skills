"""
掘金 (Juejin.cn) 内容格式化脚本 🐱
纯内容适配，不碰 API！
"""

import re


class JuejinFormatter:
    def __init__(self):
        pass

    def format_article(self, title: str, content: str, tags: list = None) -> dict:
        if tags is None:
            tags = self.extract_tags(content)

        optimized_title = self._optimize_title(title)

        # 检查技术深度
        has_code = bool(re.search(r"```", content))
        depth_score = self._assess_depth(content)

        return {
            "platform": "掘金",
            "title": optimized_title,
            "content": self._add_formatting_hints(content),
            "tags": tags[:5],
            "score": {
                "technical_depth": depth_score,
                "has_code": has_code,
                "title_length_ok": 10 <= len(optimized_title) <= 35,
            },
            "suggestions": self._get_suggestions(content, has_code),
        }

    def _optimize_title(self, title: str) -> str:
        if len(title) > 35:
            return title[:32] + "…"
        return title

    def _assess_depth(self, content: str) -> str:
        lines = content.split("\n")
        code_lines = [l for l in lines if l.strip().startswith("```") or "\t" in l]
        if len(code_lines) > 20:
            return "深"
        elif len(code_lines) > 5:
            return "中"
        return "浅"

    def _get_suggestions(self, content: str, has_code: bool) -> list:
        s = []
        if not has_code:
            s.append("💡 添加代码示例可提升 50%+ 浏览量")
        if len(content) < 500:
            s.append("💡 掘金推荐 1500 字以上的深度文章")
        s.append("💡 首段前 50 字包含核心关键词")
        s.append("💡 配图/架构图能显著提升浏览量")
        s.append("💡 文末加互动引导提升评论率")
        return s

    def _add_formatting_hints(self, content: str) -> str:
        return content  # Markdown 掘金原生支持

    def extract_tags(self, content: str) -> list:
        keywords = [
            "OpenClaw", "AI", "Python", "JavaScript", "自动化",
            "前端", "后端", "DevOps", "机器学习", "效率工具",
            "TypeScript", "Vue", "React", "Docker", "数据库",
        ]
        return [kw for kw in keywords if kw.lower() in content.lower()][:5]
