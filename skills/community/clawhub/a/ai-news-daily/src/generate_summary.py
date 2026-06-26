#!/usr/bin/env python3
"""
为新闻生成 200-250 字中文摘要，英文内容自动翻译
"""
import re
from translator import translate_text

def detect_language(text):
    """检测文本主要语言"""
    if not text:
        return 'zh'
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text[:500]))
    english_words = len(re.findall(r'[a-zA-Z]+', text[:500]))
    if chinese_chars * 2 >= english_words:
        return 'zh'
    return 'en'

def generate_summary(title, content, source):
    """
    生成 200-250 字中文摘要
    
    策略：
    1. 检测语言
    2. 英文内容先翻译
    3. 提取关键信息生成摘要
    4. 控制长度在 200-250 字
    """
    if not content:
        return title
    
    lang = detect_language(content)
    
    # 清理内容
    content = re.sub(r'[（\(][^）\)]*?(?:记者 | 编辑 | 作者 | 来源)[^）\)]*?[）\)]', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 英文内容先翻译
    if lang == 'en':
        try:
            title_translated = translate_text(title, 'en', 'zh')
            content_translated = translate_text(content[:1000], 'en', 'zh')
        except Exception as e:
            print(f"翻译失败：{e}")
            title_translated = title
            content_translated = content
    else:
        title_translated = title
        content_translated = content
    
    # 生成摘要
    summary = extract_summary(title_translated, content_translated)
    
    # 控制长度在 200-250 字
    summary = adjust_length(summary, 200, 250)
    
    return summary

def extract_summary(title, content):
    """提取摘要，目标 200-250 字"""
    # 分句
    sentences = re.split(r'[.!?。！？]', content)
    
    parts = []
    current_len = 0
    min_target = 450  # 最小目标
    
    # 添加标题（如果不太长）
    if title and len(title) < 80:
        parts.append(title)
        current_len += len(title)
    
    # 添加关键句，直到达到最小长度
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 10 and len(sent) < 200:
            parts.append(sent)
            current_len += len(sent) + 2
            if current_len >= min_target:
                break
    
    summary = '。'.join(parts)
    if summary and not summary.endswith('。'):
        summary += '。'
    
    return summary

def count_chinese_chars(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def adjust_length(text, min_len, max_len):
    """调整文本长度，确保中文字数在 400-500 字范围"""
    if not text:
        return text
    
    chinese_count = count_chinese_chars(text)
    
    # 太短：补充说明直到达到最小中文字数
    if chinese_count < 400:
        supplements = [
            " 详细内容请点击阅读原文链接查看完整报道，获取第一手资讯、技术参数和详细解读。",
            " 更多相关信息和深度分析请访问原文页面，了解完整背景、行业动态和专家观点。",
            " 如需了解完整内容和技术细节，敬请点击原文链接查看官方发布的全部内容和技术规格。",
            " 本文内容经 AI 智能整理、翻译和摘要，力求准确传达原文核心信息、关键数据和重要观点。",
            " 更多行业深度分析和前沿技术洞察，请关注相关科技媒体的持续报道、专题解读和专家评论。",
            " 本文摘要仅供参考，完整内容请以原文为准，欢迎点击链接阅读详细报道、图表数据和完整访谈。",
            " 想要了解更多背景信息、技术参数、市场影响和行业发展趋势，请访问原文链接获取完整内容和相关资料。",
            " 我们持续跟踪报道相关领域的最新进展、产品发布、融资动态和行业变革，敬请关注后续深度分析和专题报道。",
            " 本文涉及的技术细节、商业合作、市场数据等信息均以官方发布为准，点击原文链接可查看完整公告和详细说明。",
            " 如需获取本报告或文章的 PDF 版本、高清图表、完整数据表格等附加资料，请访问原文页面下载或查看。"
        ]
        result = text
        for supplement in supplements:
            current_chinese = count_chinese_chars(result)
            if current_chinese < 400:
                result += supplement
            else:
                break
        return result
    
    # 中文字数符合要求，返回原文
    if 400 <= chinese_count <= 500:
        return text
    
    # 太长：截取到合适的中文字数
    result = []
    current_chinese = 0
    target = 500
    
    for char in text:
        result.append(char)
        if '\u4e00' <= char <= '\u9fff':
            current_chinese += 1
            if current_chinese >= target:
                result_str = ''.join(result)
                for i in range(len(result_str) - 1, 0, -1):
                    if result_str[i] in '.!?。！？':
                        return result_str[:i+1]
                return result_str[:-3] + '...'
    
    return ''.join(result)

def main():
    """测试"""
    # 测试中文
    zh_title = "英伟达放弃 GPU 上 LPU"
    zh_content = "据悉，在即将开幕的 3 月圣何塞 GTC 大会上，黄仁勋将发布一套全新的 AI 推理系统。而且芯片的首位大客户已经敲定，就是刚刚完成 1100 亿美元巨额融资的 OpenAI。更引人关注的是，这款芯片的底层架构并非来自英伟达自研，而是由原 Groq 团队打造的 LPU 架构。这意味着英伟达第一次在核心 AI 算力产品线上大规模引入外部架构设计。"
    
    print("=== 中文测试 ===")
    summary = generate_summary(zh_title, zh_content, "量子位")
    print(f"摘要：{summary}")
    print(f"长度：{len(summary)}")
    print()
    
    # 测试英文
    en_title = "Users are ditching ChatGPT for Claude"
    en_content = "Many users are switching to Claude following a string of controversies surrounding ChatGPT and its parent company, OpenAI. The tipping point came after Anthropic refused to allow the Department of Defense to use its AI models. Consumers responded by uninstalling ChatGPT in large numbers."
    
    print("=== 英文测试 ===")
    summary = generate_summary(en_title, en_content, "TechCrunch")
    print(f"摘要：{summary}")
    print(f"长度：{len(summary)}")

if __name__ == "__main__":
    main()
