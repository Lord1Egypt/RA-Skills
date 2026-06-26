#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节字数检查脚本 v1.0
根据评标分值和总页数，动态计算每个章节的合格字数范围

公式：
    每页字数 = 28行 × 28字 = 780字
    每分页数 = 总页数 ÷ 总分
    章节目标 = 评分分值 × 每分页数 × 每页字数
    合格范围 = 目标字数 × 0.75 ~ 1.25
"""

import sys
import re
import os

def count_chinese_chars(text):
    """统计纯中文文字字数（忽略标点、英文、数字）"""
    # 移除所有空白字符
    text = re.sub(r'\s', '', text)
    # 中文字符范围
    chinese = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese)

def count_markdown_words(md_text):
    """统计Markdown章节字数（排除标题标记、表格分隔线等）"""
    lines = md_text.split('\n')
    total_chars = 0
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            continue
        
        # 跳过表格分隔行
        if re.match(r'^\|[-| :]+\|$', stripped):
            continue
        
        # 跳过标题标记
        if stripped.startswith('#'):
            # 标题本身也计入字数（去掉#和空格）
            content = re.sub(r'^#+\s*', '', stripped)
            total_chars += count_chinese_chars(content)
            continue
        
        # 跳过代码块
        if stripped.startswith('```'):
            continue
        
        # 跳过图片/链接语法
        line_clean = re.sub(r'!\[.*?\]\(.*?\)', '', stripped)
        line_clean = re.sub(r'\[.*?\]\(.*?\)', '', line_clean)
        
        total_chars += count_chinese_chars(line_clean)
    
    return total_chars

def parse_chapter_scores(scores_text):
    """解析章节分值配置，格式：章节名:分值,章节名:分值,...
    例如：项目背景理解:5,现状分析:5,重点难点:5
    """
    scores = {}
    for item in scores_text.split(','):
        item = item.strip()
        if ':' in item:
            name, score = item.rsplit(':', 1)
            scores[name.strip()] = int(score.strip())
    return scores

def check_chapters(md_dir, total_pages, total_score, chapter_scores):
    """
    检查目录下所有章节文件的字数
    
    Args:
        md_dir: Markdown文件目录
        total_pages: 技术标总页数
        total_score: 技术标总分
        chapter_scores: dict，章节名->分值
    """
    # 计算基础参数
    chars_per_page = 28 * 28  # 780
    pages_per_score = total_pages / total_score
    
    print(f"=" * 60)
    print(f"📊 章节字数检查")
    print(f=" * 60")
    print(f"总页数: {total_pages} | 总分: {total_score}")
    print(f"每页字数: {chars_per_page} | 每分页数: {pages_per_score:.2f}")
    print(f"")
    
    results = []
    all_pass = True
    
    # 遍历目录下所有.md文件
    for filename in sorted(os.listdir(md_dir)):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(md_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取章节名（从文件名或第一个标题）
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        chapter_name = match.group(1).strip() if match else filename
        
        # 查找对应分值
        score = None
        for name, s in chapter_scores.items():
            if name in chapter_name:
                score = s
                break
        
        if score is None:
            print(f"⚠️  找不到分值: {chapter_name}，跳过")
            continue
        
        # 计算目标字数和合格范围
        target = score * pages_per_score * chars_per_page
        min_chars = target * 0.75
        max_chars = target * 1.25
        
        # 统计字数
        actual = count_markdown_words(content)
        
        # 判断是否合格
        if min_chars <= actual <= max_chars:
            status = "✅"
        else:
            status = "❌"
            all_pass = False
        
        print(f"{status} {filename}")
        print(f"   分值: {score}分 | 目标: {target:.0f}字")
        print(f"   合格: {min_chars:.0f} ~ {max_chars:.0f}字")
        print(f"   实际: {actual}字 ({actual/target*100:.1f}%)")
        print()
        
        results.append({
            'file': filename,
            'chapter': chapter_name,
            'score': score,
            'target': target,
            'min': min_chars,
            'max': max_chars,
            'actual': actual,
            'pass': min_chars <= actual <= max_chars
        })
    
    # 汇总
    print(f"=" * 60)
    if all_pass:
        print(f"✅ 全部章节字数合格")
    else:
        print(f"❌ 以下章节需要调整:")
        for r in results:
            if not r['pass']:
                print(f"   - {r['chapter']} ({r['score']}分): {r['actual']}字")
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python3 check_chapter_words.py <目录> <总页数> <总分> <章节分值>")
        print("示例: python3 check_chapter_words.py ./chapters 400 78 '项目背景:5,现状分析:5'")
        sys.exit(1)
    
    md_dir = sys.argv[1]
    total_pages = int(sys.argv[2])
    total_score = int(sys.argv[3])
    scores_text = sys.argv[4] if len(sys.argv) > 4 else ""
    
    chapter_scores = parse_chapter_scores(scores_text) if scores_text else {}
    
    check_chapters(md_dir, total_pages, total_score, chapter_scores)
