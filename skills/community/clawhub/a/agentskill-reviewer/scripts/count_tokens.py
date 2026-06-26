#!/usr/bin/env python3
"""
Token 计数工具
估算 skill 文件的 token 消耗
"""

import sys
from pathlib import Path
from typing import Dict


def count_tokens_approximate(text: str, mode: str = 'auto') -> int:
    """
    近似计算 token 数量
    
    Args:
        text: 文本内容
        mode: 'chinese', 'english', 'auto'
    
    Returns:
        估算的 token 数
    """
    if mode == 'auto':
        # 简单判断：中文字符占比
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        total_chars = len(text)
        
        if chinese_chars > total_chars * 0.3:
            mode = 'chinese'
        else:
            mode = 'english'
    
    if mode == 'chinese':
        # 中文：约 1.5 字符 = 1 token
        return int(len(text) / 1.5)
    else:
        # 英文：约 4 字符 = 1 token
        return int(len(text) / 4)


def analyze_skill(skill_path: Path) -> Dict:
    """
    分析 skill 的 token 使用情况
    
    Returns:
        {
            'skill_md': int,
            'references': {filename: token_count},
            'scripts': {filename: token_count},
            'total': int
        }
    """
    result = {
        'skill_md': 0,
        'references': {},
        'scripts': {},
        'total': 0
    }
    
    # SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')
        result['skill_md'] = count_tokens_approximate(content)
        result['total'] += result['skill_md']
    
    # references/
    ref_dir = skill_path / "references"
    if ref_dir.exists():
        for ref_file in ref_dir.glob("*.md"):
            content = ref_file.read_text(encoding='utf-8')
            token_count = count_tokens_approximate(content)
            result['references'][ref_file.name] = token_count
            result['total'] += token_count
    
    # scripts/ (通常不会全部加载到 context，但统计一下)
    script_dir = skill_path / "scripts"
    if script_dir.exists():
        for script_file in script_dir.glob("*.py"):
            content = script_file.read_text(encoding='utf-8')
            token_count = count_tokens_approximate(content, mode='english')
            result['scripts'][script_file.name] = token_count
            # scripts 通常不计入 total（因为可能不加载）
    
    return result


def print_analysis(skill_name: str, analysis: Dict):
    """打印分析结果"""
    print(f"\n{'='*60}")
    print(f"Token 分析：{skill_name}")
    print(f"{'='*60}\n")
    
    print(f"📄 SKILL.md: {analysis['skill_md']:,} tokens")
    
    if analysis['references']:
        print(f"\n📚 References:")
        for filename, count in sorted(analysis['references'].items()):
            print(f"  - {filename}: {count:,} tokens")
        ref_total = sum(analysis['references'].values())
        print(f"  小计: {ref_total:,} tokens")
    
    if analysis['scripts']:
        print(f"\n🔧 Scripts (参考，通常不全部加载):")
        for filename, count in sorted(analysis['scripts'].items()):
            print(f"  - {filename}: {count:,} tokens")
        script_total = sum(analysis['scripts'].values())
        print(f"  小计: {script_total:,} tokens")
    
    print(f"\n{'='*60}")
    print(f"📊 总计 (SKILL.md + references): {analysis['total']:,} tokens")
    print(f"{'='*60}\n")
    
    # 给出评估
    if analysis['total'] < 2000:
        print("✅ Token 消耗较低，控制良好")
    elif analysis['total'] < 5000:
        print("⚠️ Token 消耗中等，建议考虑进一步优化")
    else:
        print("🔴 Token 消耗较高，强烈建议优化或拆分")


def main():
    if len(sys.argv) < 2:
        print("用法: python count_tokens.py <skill-directory>")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    
    if not skill_path.exists() or not skill_path.is_dir():
        print(f"❌ 错误：{skill_path} 不是有效的目录")
        sys.exit(1)
    
    analysis = analyze_skill(skill_path)
    print_analysis(skill_path.name, analysis)


if __name__ == "__main__":
    main()
