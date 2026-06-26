#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility functions for text processing - Optimized version."""

import re
from pathlib import Path
from typing import List, Optional, Union

# ---------- 句子分割 ----------
# 预编译正则，避免重复编译
_SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[。！？!?…])\s*(?=[^。！？!?…]|$)')
_SPACE_PATTERN = re.compile(r' +')
_NEWLINE_PATTERN = re.compile(r'\n{3,}')
_SPACE_BEFORE_COMMA = re.compile(r'\s+,')


def split_sentences(text: str) -> List[str]:
    """将文本分割为句子列表，保持标点。"""
    sentences = _SENTENCE_SPLIT_PATTERN.split(text)
    return [s.strip() for s in sentences if s.strip()]


# ---------- 文本清洗 ----------
def clean_text(text: str) -> str:
    """基础清洗：去除多余空格、合并换行、修复标点等。"""
    text = text.strip()
    text = _SPACE_PATTERN.sub(' ', text)
    text = _NEWLINE_PATTERN.sub('\n\n', text)
    text = _SPACE_BEFORE_COMMA.sub(',', text)
    text = re.sub(r'([。！？])([^"\'\s])', r'\1 \2', text)
    return text


# ---------- 文件读写 ----------
def read_file(path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """读取文件内容。"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding=encoding)


def write_file(path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
    """写入内容到文件。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)


# ---------- 文本统计 ----------
# 预编译词语匹配正则
_WORD_PATTERN = re.compile(r'[\u4e00-\u9fa5]+|[a-zA-Z]+(?:\'[a-zA-Z]+)?|\d+')


def word_count(text: str) -> int:
    """统计中英文混合文本的词语数量。"""
    return len(_WORD_PATTERN.findall(text))


def char_count(text: str) -> int:
    """返回字符总数（不含空白）。"""
    return len(re.sub(r'\s', '', text))


# ---------- 句子特征提取 ----------
def sentence_length(sentence: str) -> int:
    """返回句子长度（字符数，不含空白）。"""
    return len(re.sub(r'\s', '', sentence))


def count_em_dashes(text: str) -> int:
    """统计破折号数量。"""
    return text.count('——') + text.count('—')


# 弯引号列表
_CURLY_QUOTES = ('\u201c', '\u201d', '\u2018', '\u2019')  # " " ' '


def count_curly_quotes(text: str) -> int:
    """统计弯引号数量。"""
    return sum(text.count(q) for q in _CURLY_QUOTES)


def count_exclamation(text: str) -> int:
    """统计感叹号数量。"""
    return text.count('！') + text.count('!')


def count_question(text: str) -> int:
    """统计问号数量。"""
    return text.count('？') + text.count('?')


# ---------- 通用正则匹配辅助 ----------
def find_matches(text: str, patterns: List[str]) -> List[tuple]:
    """在文本中查找多个模式，返回 (匹配词, 次数) 列表。
    
    注意：此函数已废弃，保留仅为向后兼容。
    优化后的检测器使用统一正则扫描。
    """
    matches = []
    lower_text = text.lower()
    for p in patterns:
        count = lower_text.count(p.lower())
        if count > 0:
            matches.append((p, count))
    return sorted(matches, key=lambda x: -x[1])


def find_regex_matches(text: str, pattern: str) -> List[str]:
    """返回所有正则匹配结果。"""
    return re.findall(pattern, text)


# ---------- spaCy 集成（可选）----------
try:
    import spacy
    HAS_SPACY = True
    try:
        nlp = spacy.load('zh_core_web_sm')
    except OSError:
        nlp = None
except ImportError:
    HAS_SPACY = False
    nlp = None


def spacy_sentences(text: str) -> Optional[List[str]]:
    """如果 spaCy 可用，使用其句子分割。"""
    if HAS_SPACY and nlp is not None:
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]
    return None


def get_sentences(text: str) -> List[str]:
    """智能句子分割：优先 spaCy，否则使用正则。"""
    if HAS_SPACY and nlp is not None:
        sents = spacy_sentences(text)
        if sents:
            return sents
    return split_sentences(text)
