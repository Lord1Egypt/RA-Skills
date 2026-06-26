"""
小红书风格文案转换器 🐱
把任何长文变成小红书爆款风格喵！

核心能力：
- 标题党生成（emoji+痛点+数字）
- 正文转换（短句+分段+emoji点缀）
- 标签推荐（#话题# 格式）
- 配图建议
"""

import re
import random
from typing import Optional


class XiaohongshuConverter:
    """小红书文案转换器"""

    def __init__(self):
        self.emojis = [
            "💡",
            "✨",
            "🔥",
            "💰",
            "🚀",
            "👀",
            "❗",
            "📌",
            "✅",
            "🎯",
            "💪",
            "🌟",
            "👇",
            "⚡",
            "🎁",
            "🐱",
        ]
        self.title_templates = [
            "{emoji} 用了{time}就{benefit}，后悔没早知！",
            "{emoji} 建议{target}都来试试这个！",
            "{emoji} {number}分钟搞定{task}，打工人必备！",
            "{emoji} 被问爆的{topic}神器！",
            "{emoji} 别再{pain}了！试试这个！",
            "{emoji} 我愿称之为{domain}天花板！",
            "{emoji} 偷偷告诉你一个{domain}的捷径！",
        ]

    def generate_title(
        self,
        content: str,
        target: str = "打工人",
        domain: str = "效率工具",
    ) -> str:
        """生成小红书爆款标题"""
        # 提取关键词
        keywords = self.extract_keywords(content)

        template = random.choice(self.title_templates)

        title = template.format(
            emoji=random.choice(self.emojis),
            time=random.choice(["3分钟", "5分钟", "10分钟", "半天"]),
            benefit=random.choice(["效率翻倍", "准时下班", "月入过万", "升职加薪"]),
            target=target,
            number=random.choice(["3", "5", "7", "10"]),
            task=random.choice(keywords[:3]) if keywords else "工作",
            topic=random.choice(keywords[:3]) if keywords else "神器",
            pain="浪费时间" if not keywords else f"为{keywords[0]}头疼",
            domain=domain,
        )

        return title

    def convert_to_xhs_style(self, content: str, max_chars: int = 1000) -> str:
        """把长文转换成小红书风格"""
        # 分段处理
        paragraphs = self.split_into_short_paragraphs(content)

        result = []

        for i, para in enumerate(paragraphs[:8]):  # 最多8段
            if i == 0:
                # 开头用emoji吸引人
                result.append(f"{random.choice(self.emojis)} {para}")
            elif i == len(paragraphs) - 1:
                # 结尾引导互动
                result.append(f"💬 觉得有用的话，记得❤️⭐哦~")
                result.append(f"\n#效率工具 #打工人必备 #AI助手")
            else:
                # 中间段落加点emoji
                if random.random() > 0.5:
                    result.append(f"{random.choice(self.emojis)} {para}")
                else:
                    result.append(para)

        return "\n\n".join(result)[:max_chars]

    def generate_tags(self, content: str, max_tags: int = 10) -> list:
        """生成小红书标签"""
        base_tags = ["效率工具", "AI", "打工人", "自我提升", "干货分享"]
        
        # 从内容中提取更多标签
        keywords = self.extract_keywords(content)
        for kw in keywords[:5]:
            if kw not in base_tags:
                base_tags.append(kw)

        return [f"#{tag}#" for tag in base_tags[:max_tags]]

    def image_suggestions(self, content: str) -> list:
        """生成配图建议"""
        suggestions = [
            "🖼️ 封面：大字报风格，突出痛点或结果",
            "🖼️ 对比图：使用前 vs 使用后",
            "🖼️ 截图：实际操作界面截图",
            "🖼️ 步骤图：分步骤操作指南",
            "🖼️ 成果图：最终效果展示",
        ]
        return suggestions[:3]

    def split_into_short_paragraphs(self, content: str) -> list:
        """把文章拆成短句"""
        # 先按段落分
        paragraphs = re.split(r"\n\n+", content)

        result = []
        for para in paragraphs:
            # 再按句子分
            sentences = re.split(r'[。！？\n]', para)
            short_sents = [s.strip() for s in sentences if s.strip()]

            # 组合成短段落（2-3句一段）
            for i in range(0, len(short_sents), 3):
                chunk = short_sents[i : i + 3]
                result.append("".join(chunk))

        return result

    def extract_keywords(self, content: str) -> list:
        """简单的关键词提取"""
        # 常见中文关键词
        keywords = []
        common_words = [
            "效率",
            "自动化",
            "AI",
            "工具",
            "赚钱",
            "副业",
            "技巧",
            "方法",
            "教程",
            "攻略",
        ]

        for word in common_words:
            if word in content:
                keywords.append(word)

        return keywords


def convert(content: str, title_hint: str = "", max_chars: int = 1000) -> dict:
    """对外接口"""
    converter = XiaohongshuConverter()

    title = title_hint if title_hint else converter.generate_title(content)
    body = converter.convert_to_xhs_style(content, max_chars)
    tags = converter.generate_tags(content)
    images = converter.image_suggestions(content)

    return {
        "title": title,
        "body": body,
        "tags": tags,
        "image_suggestions": images,
    }
