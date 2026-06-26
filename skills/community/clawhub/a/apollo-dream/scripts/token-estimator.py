#!/usr/bin/env python3
"""
token-estimator.py - 快速Token估算
使用字符数/4 + 中文特殊处理
"""
import os
import sys
import re

def count_tokens(text):
    """
    估算token数
    - 中文：按字符计（约1-2字符=1token）
    - 英文：按单词计（约0.75词=1token）
    """
    if not text:
        return 0
    
    # 中文字符（粗略：每个汉字=1.5token）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 英文单词（约0.75token/词）
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    
    # 其他字符（括号、标点等，约4字符=1token）
    other_chars = len(re.findall(r'[^\w\s]', text))
    
    # 空白字符
    whitespace = len(re.findall(r'\s', text))
    
    # 总估算
    # 中文贵：每个汉字1.5token
    # 英文便宜：每个词0.75token
    # 标点符号：4个约1token
    total = chinese_chars * 1.5 + english_words * 0.75 + other_chars / 4
    
    return int(total)

def estimate_tokens_from_text(text):
    """估算文本token数"""
    return count_tokens(text)

def estimate_tokens_from_file(filepath, max_chars=None):
    """
    估算文件token数
    
    Args:
        filepath: 文件路径
        max_chars: 最大字符数（None=全部）
    
    Returns:
        dict: {token_count, char_count, line_count, method}
    """
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r') as f:
        if max_chars:
            text = f.read(max_chars)
        else:
            text = f.read()
    
    char_count = len(text)
    line_count = text.count('\n') + 1
    
    return {
        'token_count': count_tokens(text),
        'char_count': char_count,
        'line_count': line_count,
        'method': 'char-word-punctuation'
    }

def main():
    if len(sys.argv) < 2:
        print("用法: token-estimator.py <file> [max_chars]")
        print("   或: token-estimator.py --text <文本>")
        sys.exit(1)
    
    if sys.argv[1] == '--text':
        text = ' '.join(sys.argv[2:])
        tokens = count_tokens(text)
        print(f"Token数: {tokens}")
        print(f"字符数: {len(text)}")
    else:
        filepath = sys.argv[1]
        max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else None
        
        result = estimate_tokens_from_file(filepath, max_chars)
        if result:
            print(f"文件: {filepath}")
            print(f"Token数: {result['token_count']}")
            print(f"字符数: {result['char_count']}")
            print(f"行数: {result['line_count']}")
            print(f"方法: {result['method']}")
        else:
            print(f"文件不存在: {filepath}")

if __name__ == '__main__':
    main()
