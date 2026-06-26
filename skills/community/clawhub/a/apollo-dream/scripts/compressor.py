#!/usr/bin/env python3
"""
compressor.py - 三层做梦压缩
Layer 1: Microcompact（浅睡） - 快速删token
Layer 2: Session Memory（REM） - 保留结构
Layer 3: Deep Compact（深睡） - 完整摘要
"""
import os
import sys
import re
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token-estimator import estimate_tokens_from_text
from density-detector import get_density_level, is_high_density

WORKFLOW_DIR = "/root/.openclaw/workspace/.workflow"
STATE_DIR = "/root/.openclaw/workspace/.dream"

def compress_micro(text):
    """
    Layer 1: Microcompact
    触发：token > 50000
    动作：快速删除过程噪音，保留最后2-3轮关键上下文
    """
    if not text:
        return text
    
    tokens = estimate_tokens_from_text(text)
    if tokens <= 50000:
        return text
    
    lines = text.split('\n')
    
    # 保留高密度行
    kept_lines = []
    dropped = 0
    
    for line in lines[-50:]:  # 保留最后50行
        if is_high_density(line) or len(line) < 20:
            kept_lines.append(line)
        else:
            dropped += 1
    
    result = '\n'.join(kept_lines)
    return f"[Microcompact: 删除了{len(lines)-len(kept_lines)}行]\n{result}"

def compress_session(text):
    """
    Layer 2: Session Memory
    触发：token > 80000
    动作：保留任务状态、决策点、用户偏好
    """
    if not text:
        return text
    
    tokens = estimate_tokens_from_text(text)
    if tokens <= 80000:
        return text
    
    # 提取高密度段落
    lines = text.split('\n')
    important = []
    
    for line in lines:
        if is_high_density(line):
            important.append(line)
    
    result = '\n'.join(important)
    return f"[Session Memory: {len(lines)}行→{len(important)}行]\n{result}"

def compress_deep(text):
    """
    Layer 3: Deep Compact
    触发：token > 120000
    动作：完整摘要，建立关联
    """
    if not text:
        return text
    
    tokens = estimate_tokens_from_text(text)
    if tokens <= 120000:
        return text
    
    # 提取所有决策和结论
    lines = text.split('\n')
    decisions = []
    actions = []
    
    for line in lines:
        level = get_density_level(line)
        if level == 'high':
            if re.search(r'决定|决策|结论', line):
                decisions.append(line)
            elif re.search(r'任务|下一步|做', line):
                actions.append(line)
    
    summary = f"""[Deep Compact摘要]
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
原始行数: {len(lines)}
保留决策: {len(decisions)}条
保留行动: {len(actions)}条

=== 决策 ===
{chr(10).join(decisions[:10])}

=== 行动 ===
{chr(10).join(actions[:10])}
"""
    
    return summary

def compress(text, layer=None):
    """
    主压缩函数
    
    Args:
        text: 要压缩的文本
        layer: 指定层(1/2/3)，None=自动选择
    
    Returns:
        tuple: (压缩后文本, 实际layer)
    """
    if not text:
        return text, 0
    
    tokens = estimate_tokens_from_text(text)
    
    if layer is None:
        if tokens > 120000:
            layer = 3
        elif tokens > 80000:
            layer = 2
        elif tokens > 50000:
            layer = 1
        else:
            return text, 0
    
    if layer == 1:
        return compress_micro(text), 1
    elif layer == 2:
        return compress_session(text), 2
    elif layer == 3:
        return compress_deep(text), 3
    else:
        return text, 0

def main():
    if len(sys.argv) < 2:
        print("用法: compressor.py <file> [layer]")
        print("   layer: 1(micro) / 2(session) / 3(deep) / auto")
        sys.exit(1)
    
    filepath = sys.argv[1]
    layer = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    with open(filepath, 'r') as f:
        text = f.read()
    
    compressed, actual_layer = compress(text, layer)
    
    print(f"压缩前token: {estimate_tokens_from_text(text)}")
    print(f"压缩后token: {estimate_tokens_from_text(compressed)}")
    print(f"使用Layer: {actual_layer}")
    print(f"\n--- 压缩结果 ---")
    print(compressed[:500] if len(compressed) > 500 else compressed)

if __name__ == '__main__':
    main()
