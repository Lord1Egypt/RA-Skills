#!/usr/bin/env python3
"""
随机文本生成器
纯 Python 标准库实现
"""

import secrets
import argparse
import random
import sys

# Lorem Ipsum 英文单词库
ENGLISH_WORDS = [
    'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing',
    'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore',
    'et', 'dolore', 'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam',
    'quis', 'nostrud', 'exercitation', 'ullamco', 'laboris', 'nisi',
    'aliquip', 'ex', 'ea', 'commodo', 'consequat', 'duis', 'aute', 'irure',
    'in', 'reprehenderit', 'voluptate', 'velit', 'esse', 'cillum', 'fugiat',
    'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat', 'cupidatat',
    'non', 'proident', 'sunt', 'culpa', 'qui', 'officia', 'deserunt',
    'mollit', 'anim', 'id', 'est', 'laborum', 'accumsan', 'bibendum',
    'erat', 'volutpat', 'nam', 'mi', 'pretium', 'risus', 'tristique',
    'senectus', 'netus', 'malesuada', 'fames', 'turpis', 'egestas',
    'proin', 'sagittis', 'nisl', 'rhoncus', 'mattis', 'purus', 'enim',
]

# 中文占位文本
CHINESE_WORDS = [
    '的', '是', '了', '在', '和', '与', '以及', '或者', '还是',
    '但是', '然而', '因为', '所以', '如果', '虽然', '虽然说',
    '这个', '那个', '一个', '一些', '可以', '能够', '应该',
    '必须', '需要', '要求', '希望', '想要', '觉得', '认为',
    '可能', '也许', '大概', '应该', '必须', '一定', '必然',
]


def secure_choice(sequence):
    """使用 secrets 模块安全随机选择"""
    return secrets.choice(sequence)


def random_choice(sequence, seed=None):
    """使用 random 模块随机选择（可选种子）"""
    if seed is not None:
        random.seed(seed)
    return random.choice(sequence)


def generate_words(count: int, lang: str = 'en', use_seed: bool = False, seed: int = None) -> list:
    """生成随机单词列表"""
    word_list = ENGLISH_WORDS if lang == 'en' else CHINESE_WORDS
    result = []
    for _ in range(count):
        if use_seed:
            result.append(random_choice(word_list, seed))
        else:
            result.append(secure_choice(word_list))
    return result


def generate_sentences(count: int, lang: str = 'en', use_seed: bool = False, seed: int = None,
                       min_words: int = 5, max_words: int = 15) -> list:
    """生成完整句子"""
    sentences = []
    for _ in range(count):
        word_count = random.randint(min_words, max_words) if use_seed else secrets.randbelow(max_words - min_words + 1) + min_words
        words = generate_words(word_count, lang, use_seed, seed)
        if lang == 'en':
            sentences.append(' '.join(words).capitalize() + '.')
        else:
            sentences.append(''.join(words) + '。')
    return sentences


def generate_paragraphs(count: int, lang: str = 'en', use_seed: bool = False, seed: int = None,
                        min_sentences: int = 3, max_sentences: int = 8) -> list:
    """生成段落"""
    paragraphs = []
    for _ in range(count):
        sentence_count = random.randint(min_sentences, max_sentences) if use_seed else secrets.randbelow(max_sentences - min_sentences + 1) + min_sentences
        sentences = generate_sentences(sentence_count, lang, use_seed, seed)
        paragraphs.append(' '.join(sentences))
    return paragraphs


def main():
    parser = argparse.ArgumentParser(
        description='随机文本生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s words 10                    生成 10 个随机单词
  %(prog)s sentences 5                 生成 5 个完整句子
  %(prog)s paragraphs 3                 生成 3 个段落
  %(prog)s words 20 --seed 42           使用固定种子
  %(prog)s words 10 --lang zh           中文模式
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # words
    p_words = subparsers.add_parser('words', help='生成随机单词')
    p_words.add_argument('count', type=int, help='单词数量')
    p_words.add_argument('--seed', type=int, help='随机种子（用于复现）')
    p_words.add_argument('--lang', choices=['en', 'zh'], default='en', help='语言')

    # sentences
    p_sentences = subparsers.add_parser('sentences', help='生成随机句子')
    p_sentences.add_argument('count', type=int, help='句子数量')
    p_sentences.add_argument('--seed', type=int, help='随机种子（用于复现）')
    p_sentences.add_argument('--lang', choices=['en', 'zh'], default='en', help='语言')
    p_sentences.add_argument('--min', type=int, default=5, help='每句最少单词数')
    p_sentences.add_argument('--max', type=int, default=15, help='每句最多单词数')

    # paragraphs
    p_paragraphs = subparsers.add_parser('paragraphs', help='生成随机段落')
    p_paragraphs.add_argument('count', type=int, help='段落数量')
    p_paragraphs.add_argument('--seed', type=int, help='随机种子（用于复现）')
    p_paragraphs.add_argument('--lang', choices=['en', 'zh'], default='en', help='语言')
    p_paragraphs.add_argument('--min-sentences', type=int, default=3, help='每段最少句子数')
    p_paragraphs.add_argument('--max-sentences', type=int, default=8, help='每段最多句子数')

    args = parser.parse_args()

    if args.command == 'words':
        use_seed = args.seed is not None
        words = generate_words(args.count, args.lang, use_seed, args.seed)
        print(' '.join(words))

    elif args.command == 'sentences':
        use_seed = args.seed is not None
        sentences = generate_sentences(args.count, args.lang, use_seed, args.seed,
                                      args.min, args.max)
        print('\n'.join(sentences))

    elif args.command == 'paragraphs':
        use_seed = args.seed is not None
        paragraphs = generate_paragraphs(args.count, args.lang, use_seed, args.seed,
                                        args.min_sentences, args.max_sentences)
        print('\n\n'.join(paragraphs))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
