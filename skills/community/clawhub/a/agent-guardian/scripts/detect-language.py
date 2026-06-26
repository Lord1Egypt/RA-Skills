#!/usr/bin/env python3
"""
语言检测工具 - 基于字符集 + langdetect 双重检测
用法: python3 detect-language.py "text"
返回: zh / en / ja / ko / unknown
"""
import sys
import re

def strip_code_blocks(text):
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    return text

def strip_non_text(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(r'[，。！？、；：\u201c\u201d\u2018\u2019（）【】《》\x2d\u2014\u2013\u2026\u00b7.!?,;:\'\"()\[\]{}<>/\\@#$%^&*+=|~]', '', text)
    return text.strip()

def detect(text):
    text = strip_code_blocks(text)
    text = strip_non_text(text)

    if not text:
        return "unknown"

    cjk_chars = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
    hiragana = len(re.findall(r'[\u3040-\u309f]', text))
    katakana = len(re.findall(r'[\u30a0-\u30ff]', text))
    hangul = len(re.findall(r'[\uac00-\ud7af\u1100-\u11ff]', text))
    latin = len(re.findall(r'[a-zA-Z]', text))

    total = cjk_chars + hiragana + katakana + hangul + latin
    if total == 0:
        return "unknown"

    jp_chars = hiragana + katakana
    if jp_chars > 0 and jp_chars >= latin:
        return "ja"
    if hangul > 0 and hangul >= latin and hangul >= cjk_chars:
        return "ko"
    if cjk_chars > 0 and cjk_chars >= latin:
        return "zh"
    if latin > 0:
        if latin > 20:
            try:
                from langdetect import detect as ld
                return ld(text)
            except:
                pass
        return "en"
    return "unknown"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    print(detect(text))
