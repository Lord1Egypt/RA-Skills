#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评论词云生成器
从评论数据生成词频统计和词云图
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

# 检查依赖
try:
    import jieba
    from wordcloud import WordCloud
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"错误: 缺少必要的依赖库")
    print(f"请安装: pip install jieba wordcloud matplotlib")
    sys.exit(1)


def load_stop_words(stop_words_file: Optional[str] = None) -> set:
    """加载停用词"""
    if not stop_words_file or not Path(stop_words_file).exists():
        return set()

    with open(stop_words_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())


def load_custom_words(custom_words_str: Optional[str] = None) -> List[str]:
    """加载自定义词库"""
    if not custom_words_str:
        return []

    words = [word.strip() for word in custom_words_str.split(',') if word.strip()]
    for word in words:
        jieba.add_word(word)
    return words


async def generate_wordcloud(
    data_file: str,
    output_dir: str,
    stop_words_file: Optional[str] = None,
    custom_words_str: Optional[str] = None,
    max_words: int = 200
) -> None:
    """
    生成词云和词频统计

    Args:
        data_file: 评论数据文件路径
        output_dir: 输出目录
        stop_words_file: 停用词文件路径
        custom_words_str: 自定义词库（逗号分隔）
        max_words: 词云最大词数
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 加载停用词和自定义词库
    stop_words = load_stop_words(stop_words_file)
    custom_words = load_custom_words(custom_words_str)

    print(f"✓ 加载停用词: {len(stop_words)} 个")
    if custom_words:
        print(f"✓ 加载自定义词库: {len(custom_words)} 个")

    # 读取评论数据
    print(f"✓ 读取评论数据: {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("错误: 评论数据为空")
        return

    print(f"✓ 加载评论数: {len(data)} 条")

    # 提取所有文本
    all_text = ' '.join(
        item.get('content', '') for item in data if 'content' in item
    )

    if not all_text.strip():
        print("错误: 没有找到有效的评论内容")
        return

    # 分词并过滤
    print("✓ 开始分词...")
    words = [
        word.strip()
        for word in jieba.lcut(all_text)
        if word.strip()
        and word not in stop_words
        and len(word.strip()) > 0
    ]

    if not words:
        print("错误: 分词后没有有效词汇")
        return

    print(f"✓ 有效词汇数: {len(words)} 个")

    # 统计词频
    print("✓ 统计词频...")
    word_freq = Counter(words)

    # 保存词频统计
    freq_file = output_path / "word_freq.json"
    with open(freq_file, 'w', encoding='utf-8') as f:
        json.dump(dict(word_freq.most_common()), f, ensure_ascii=False, indent=2)
    print(f"✓ 词频统计已保存: {freq_file}")

    # 生成词云
    print("✓ 生成词云...")
    try:
        # 取前 max_words 个词
        top_words = dict(word_freq.most_common(max_words))

        # 生成词云
        wordcloud = WordCloud(
            font_path=None,  # 使用系统默认字体
            width=800,
            height=400,
            background_color='white',
            max_words=max_words,
            stopwords=stop_words,
            colormap='viridis',
            contour_color='steelblue',
            contour_width=1,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(top_words)

        # 保存词云图
        cloud_file = output_path / "word_cloud.png"
        plt.figure(figsize=(10, 5), facecolor='white')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(cloud_file, format='png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 词云图已保存: {cloud_file}")
        print(f"✓ 完成！共生成 {len(top_words)} 个词的词云")

    except Exception as e:
        print(f"错误: 生成词云失败: {e}")
        print("提示: 如果是中文字体问题，请安装中文字体并修改 font_path 参数")


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python generate_wordcloud.py <data_file> <output_dir> [options]")
        print("参数:")
        print("  data_file          评论数据文件路径（必填）")
        print("  output_dir         输出目录（必填）")
        print("  --stop-words FILE 停用词文件路径（可选）")
        print("  --custom-words WORDS 自定义词库，逗号分隔（可选）")
        print("  --max-words N     词云最大词数（可选，默认 200）")
        print("\n示例:")
        print("  python generate_wordcloud.py comments.json output/")
        print("  python generate_wordcloud.py comments.json output/ --max-words 100")
        print("  python generate_wordcloud.py comments.json output/ --custom-words '热词,关键词'")
        sys.exit(1)

    # 解析参数
    data_file = sys.argv[1]
    output_dir = sys.argv[2]
    stop_words_file = None
    custom_words_str = None
    max_words = 200

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--stop-words' and i + 1 < len(sys.argv):
            stop_words_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--custom-words' and i + 1 < len(sys.argv):
            custom_words_str = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--max-words' and i + 1 < len(sys.argv):
            try:
                max_words = int(sys.argv[i + 1])
            except ValueError:
                print(f"错误: max-words 必须是整数")
                sys.exit(1)
            i += 2
        else:
            i += 1

    # 检查数据文件
    if not Path(data_file).exists():
        print(f"错误: 数据文件不存在: {data_file}")
        sys.exit(1)

    # 运行
    asyncio.run(generate_wordcloud(
        data_file=data_file,
        output_dir=output_dir,
        stop_words_file=stop_words_file,
        custom_words_str=custom_words_str,
        max_words=max_words
    ))


if __name__ == '__main__':
    main()
