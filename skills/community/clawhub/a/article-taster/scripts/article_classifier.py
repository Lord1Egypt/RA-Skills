"""
M1: 文章类型自动识别模块
支持: 技术文章 | 情感散文 | 小说 | 其他
"""

from typing import Tuple, Dict
import re


class ArticleClassifier:
    """文章类型分类器 - 基于关键词密度匹配"""

    TYPE_KEYWORDS: Dict[str, list] = {
        "technical_article": [
            "代码", "算法", "架构", "实现", "技术", "开发", "API",
            "框架", "数据库", "性能", "优化", "部署", "测试",
            "函数", "类", "模块", "接口", "编程", "系统", "网络",
            "服务器", "客户端", "前端", "后端", "云", "容器"
        ],
        "essay": [
            "感受", "心情", "回忆", "思念", "人生", "感悟",
            "情感", "心灵", "成长", "温暖", "爱", "希望",
            "时光", "岁月", "梦想", "勇气", "坚强", "心疼",
            "亲情", "友情", "爱情", "乡愁", "童年", "青春"
        ],
        "novel": [
            "人物", "情节", "故事", "场景", "对话", "叙述",
            "主角", "配角", "高潮", "结局", "章节", "叙事",
            "小说", "情节", "转折", "冲突", "描写", "刻画",
            "视角", "第一人称", "第三人称", "伏笔", "悬念"
        ]
    }

    def classify(self, title: str, content: str) -> Tuple[str, float]:
        """
        识别文章类型

        Returns:
            (article_type, confidence) 元组
            article_type: technical_article | essay | novel | other
            confidence: 0.0-1.0 置信度
        """
        text = f"{title} {content}".lower()
        scores = {}

        for art_type, keywords in self.TYPE_KEYWORDS.items():
            keyword_matches = sum(1 for kw in keywords if kw in text)
            density = keyword_matches / max(len(text) / 500, 1)
            scores[art_type] = keyword_matches + density * 10

        if not scores or max(scores.values()) == 0:
            return "other", 0.5

        best_type = max(scores, key=scores.get)
        max_score = scores[best_type]
        confidence = min(0.95, 0.5 + max_score * 0.05)

        return best_type, round(confidence, 2)

    def classify_with_hints(
        self,
        title: str,
        content: str,
        user_hint: str = None
    ) -> Tuple[str, float, str]:
        """
        带用户提示的类型识别

        Args:
            title: 文章标题
            content: 文章内容
            user_hint: 用户提示的预期类型

        Returns:
            (article_type, confidence, source) 元组
            source: "auto" | "user_hint"
        """
        auto_type, auto_conf = self.classify(title, content)

        if user_hint and user_hint in ["technical_article", "essay", "novel", "other"]:
            return user_hint, 0.95, "user_hint"

        return auto_type, auto_conf, "auto"


if __name__ == "__main__":
    classifier = ArticleClassifier()

    test_cases = [
        ("Python异步编程实战", "本文介绍Python异步编程的核心概念..."),
        ("那一年夏天的回忆", "阳光、蝉鸣、还有那个再也回不去的夏天..."),
        ("三体读后感", "刘慈欣的《三体》构建了一个宏大的宇宙图景..."),
    ]

    for title, content in test_cases:
        t, c = classifier.classify(title, content)
        print(f"[{title[:15]}...] -> {t} ({c:.0%})")
