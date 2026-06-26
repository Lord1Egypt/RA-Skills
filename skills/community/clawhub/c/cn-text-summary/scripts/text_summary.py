#!/usr/bin/env python3
"""
文本摘要工具 - 提取文本核心要点
"""
import sys
import json
import re

try:
    import jieba
    import jieba.analyse
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False

def extract_sentences(text, max_sentences=5):
    """提取关键句子"""
    # 按句号、问号、感叹号分割
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= max_sentences:
        return sentences
    
    # 简单权重：句子位置 + 长度
    scored = []
    for i, s in enumerate(sentences):
        score = 0
        # 首尾句权重高
        if i < 2:
            score += 3
        elif i >= len(sentences) - 2:
            score += 2
        # 中等长度更好
        if 20 <= len(s) <= 100:
            score += 2
        elif len(s) > 100:
            score += 1
        scored.append((score, s))
    
    scored.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in scored[:max_sentences]]

def extract_keywords(text, top_n=5):
    """提取关键词"""
    if HAS_JIEBA:
        keywords = jieba.analyse.extract_tags(text, topK=top_n)
        return keywords
    else:
        # 简单提取：高频词
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        from collections import Counter
        freq = Counter(words)
        return [w[0] for w in freq.most_common(top_n)]

def summarize(text, max_length=300):
    """生成摘要"""
    # 提取关键句子
    sentences = extract_sentences(text, max_sentences=5)
    
    # 组合摘要
    summary = '。'.join(sentences)
    if len(summary) > max_length:
        summary = summary[:max_length] + '...'
    
    return summary

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供文本内容'}, ensure_ascii=False))
        return
    
    text = sys.argv[1]
    max_length = 300
    
    # 解析参数
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] in ['-l', '--length'] and i + 1 < len(args):
            max_length = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    # 生成摘要
    summary = summarize(text, max_length)
    keywords = extract_keywords(text)
    
    result = {
        'original_length': len(text),
        'summary_length': len(summary),
        'summary': summary,
        'keywords': keywords
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
