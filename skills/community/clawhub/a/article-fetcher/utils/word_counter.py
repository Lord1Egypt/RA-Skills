"""
字数统计：剔除 HTML 标签和图片链接后统计字符数
"""
import re


def count_words(html_content: str) -> int:
    """
    统计 HTML 内容的纯文本字数（不含标签、图片链接、空白字符）
    """
    if not html_content:
        return 0
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', html_content)
    # 去除空白字符
    text = re.sub(r'\s+', '', text)
    return len(text)
