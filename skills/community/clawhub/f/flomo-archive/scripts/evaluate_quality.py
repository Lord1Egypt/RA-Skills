#!/usr/bin/env python3
"""
Flomo 笔记质量评估 - 基于已有完整数据
无需额外 API 调用，直接评估 /tmp/flomo_YYYY_MM.json
"""
import json
import sys

def evaluate_quality(memo):
    """
    评估单条笔记质量
    返回: (是否低质量, 原因)
    """
    content = memo.get("content", "")
    word_count = memo.get("word_count", 0)
    tags = memo.get("tags", [])
    has_image = memo.get("has_image", False)
    has_link = memo.get("has_link", False)
    
    # 规则1: 有标签 + 有实质内容 → 高质量
    if tags and word_count >= 50:
        return (False, "已分类且内容充实")
    
    # 规则2: 包含链接/图片 → 有价值
    if has_link or has_image:
        return (False, "含多媒体或链接")
    
    # 规则3: 字数过少 (< 20字)
    if word_count < 20:
        return (True, f"字数过少({word_count}字)")
    
    # 规则4: 纯流水账特征
    trivial_patterns = ["起床了", "睡觉了", "晚安", "早安", "今天天气", "吃了", "到家了", "出门了"]
    if word_count < 50 and any(p in content for p in trivial_patterns):
        return (True, "疑似流水账")
    
    # 规则5: 无标签 + 短内容 → 建议审阅
    if not tags and word_count < 100:
        return (True, "无标签且内容较短")
    
    return (False, "内容完整")

def analyze_quality(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        memos = json.load(f)
    
    low_quality = []
    high_quality = []
    
    for memo in memos:
        is_low, reason = evaluate_quality(memo)
        if is_low:
            low_quality.append((memo, reason))
        else:
            high_quality.append((memo, reason))
    
    # 输出报告
    print(f"\n{'='*60}")
    print(f"📊 笔记质量评估报告")
    print(f"{'='*60}")
    print(f"总笔记: {len(memos)}")
    print(f"高质量: {len(high_quality)} ({len(high_quality)/len(memos)*100:.1f}%)")
    print(f"建议标记: {len(low_quality)} ({len(low_quality)/len(memos)*100:.1f}%)")
    
    if low_quality:
        print(f"\n📝 低质量笔记示例 (前10条):")
        for memo, reason in low_quality[:10]:
            preview = memo["content"].replace('\n', ' ')[:40]
            print(f"   [{reason}] {preview}...")
    
    return low_quality

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 evaluate_quality.py /tmp/flomo_2025_07.json")
        sys.exit(1)
    
    analyze_quality(sys.argv[1])
