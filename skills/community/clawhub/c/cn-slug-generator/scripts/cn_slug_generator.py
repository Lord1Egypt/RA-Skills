#!/usr/bin/env python3
"""
cn-slug-generator - URL Slug生成器
将中文标题转换为SEO友好的URL Slug
"""
import argparse
import re
import sys
import os

def translate_text(text):
    """翻译中文为英文"""
    # 关键词词典（只保留常见英文词）
    zh_dict = {
        '如何': 'how', '怎么': 'how', '怎样': 'how',
        '为什么': 'why', '什么': 'what', '哪个': 'which', '哪些': 'which',
        '使用': 'use', '方法': 'method', '技巧': 'tips', '教程': 'tutorial',
        '指南': 'guide', '攻略': 'guide', '推荐': 'recommend', '介绍': 'intro',
        '分析': 'analysis', '讲解': 'explain', '说明': 'explain', '解析': 'analysis',
        '问题': 'question', '答案': 'answer', '解答': 'answer', '解决': 'solve',
        '方式': 'way', '模式': 'mode', '方案': 'plan', '策略': 'strategy',
        '工具': 'tools', '软件': 'software', '应用': 'app', '平台': 'platform',
        '系统': 'system', '服务': 'service', '产品': 'product', '项目': 'project',
        '技术': 'tech', '科技': 'tech', '创新': 'innovation', '开源': 'open-source',
        '免费': 'free', '付费': 'paid', '价格': 'price', '购买': 'buy', '订阅': 'subscribe',
        '入门': 'getting-started', '基础': 'basic', '高级': 'advanced', '实战': 'practice',
        '进阶': 'advanced', '精通': 'master', '总结': 'summary', '汇总': 'summary',
        '人工智能': 'ai', '机器学习': 'machine-learning', '深度学习': 'deep-learning',
        '神经网络': 'neural-network', '大模型': 'llm', '自然语言处理': 'nlp',
        '计算机视觉': 'cv', '生成式AI': 'generative-ai', 'AIGC': 'aigc',
        '提示词': 'prompt', '微调': 'fine-tuning', '智能体': 'agent',
        'OpenClaw': 'openclaw', 'ClawHub': 'clawhub', 'Claude': 'claude',
        'Python': 'python', 'JavaScript': 'javascript', 'TypeScript': 'typescript',
        'React': 'react', 'Vue': 'vue', 'Node': 'node', 'Go': 'go', 'Rust': 'rust',
        'Docker': 'docker', 'Kubernetes': 'kubernetes', 'Git': 'git', 'GitHub': 'github',
        'API': 'api', 'SDK': 'sdk', 'CLI': 'cli',
        'JSON': 'json', 'XML': 'xml', 'HTML': 'html', 'CSS': 'css',
        'Markdown': 'markdown', 'PDF': 'pdf',
        'OCR': 'ocr', 'TTS': 'tts', 'SEO': 'seo',
        '飞书': 'feishu', '钉钉': 'dingtalk', '小红书': 'xiaohongshu',
        '抖音': 'douyin', '知乎': 'zhihu', 'Bilibili': 'bilibili',
        '微信公众号': 'wechat', '微信': 'wechat', 'Notion': 'notion',
    }
    
    result = []
    text = text.strip()
    i = 0
    
    while i < len(text):
        matched = False
        # 尝试最长匹配
        for length in range(min(4, len(text) - i + 1), 0, -1):
            chunk = text[i:i+length]
            if chunk in zh_dict:
                eng = zh_dict[chunk]
                if eng:
                    result.append(eng)
                i += length
                matched = True
                break
        
        if not matched:
            char = text[i]
            if char.isascii() and (char.isalpha() or char.isdigit()):
                j = i
                while j < len(text) and text[j].isascii() and (text[j].isalpha() or text[j].isdigit()):
                    j += 1
                result.append(text[i:j].lower())
                i = j
            else:
                # 中文/其他字符 - 跳过，由pinyin处理
                i += 1
    
    return ' '.join(result)

def to_slug(text, separator='-'):
    """文本转Slug"""
    translated = translate_text(text)
    
    # 如果没有翻译出结果，用pinyin
    if not translated.strip():
        return pinyin_slug(text, separator)
    
    words = translated.split()
    stop_words = {'is', 'a', 'an', 'the', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 
                  'and', 'or', 'but', 'be', 'have', 'has', 'will', 'can', 'not', 'no', 
                  'all', 'also', 'very', 'then', 'this', 'that', 'these', 'those', 
                  'with', 'from', 'its', 'it', 'i', 'you', 'he', 'she', 'we', 'they'}
    words = [w for w in words if w and w.lower() not in stop_words and len(w) > 1]
    return separator.join(words)

def pinyin_slug(text, separator='-'):
    """转换为拼音Slug"""
    try:
        import pypinyin
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        py = pypinyin.lazy_pinyin(text)
        words = [w for w in py if w.strip()]
        return separator.join(words)
    except ImportError:
        return text

def batch_convert(texts, pinyin=False, separator='-'):
    """批量转换"""
    results = []
    for line in texts.strip().split('\n'):
        line = line.strip()
        if line:
            if pinyin:
                slug = pinyin_slug(line, separator)
            else:
                slug = to_slug(line, separator)
            results.append(slug)
    return results

def main():
    parser = argparse.ArgumentParser(description='URL Slug生成器', 
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog='''
示例:
  python3 cn_slug_generator.py "如何用Python写爬虫"
  python3 cn_slug_generator.py "深度学习入门教程" --pinyin
  python3 cn_slug_generator.py --batch < titles.txt
''')
    parser.add_argument('text', nargs='?', help='要转换的文本')
    parser.add_argument('--pinyin', action='store_true', help='转换为拼音')
    parser.add_argument('--separator', default='-', help='分隔符 (默认: -)')
    parser.add_argument('--output', help='输出到文件')
    parser.add_argument('--batch', action='store_true', help='批量模式')
    
    args = parser.parse_args()
    
    if args.batch:
        if args.text and os.path.exists(args.text):
            with open(args.text, 'r', encoding='utf-8') as f:
                input_text = f.read()
        else:
            input_text = sys.stdin.read()
        results = batch_convert(input_text, args.pinyin, args.separator)
        output = '\n'.join(results)
    else:
        if not args.text:
            print("用法: python3 cn_slug_generator.py '中文标题'")
            print("  python3 cn_slug_generator.py '标题' --pinyin")
            print("  python3 cn_slug_generator.py --batch < file.txt")
            return
        if args.pinyin:
            output = pinyin_slug(args.text, args.separator)
        else:
            output = to_slug(args.text, args.separator)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已保存: {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()