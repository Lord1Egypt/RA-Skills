#!/usr/bin/env python3
"""
Genos DNA 序列分析 - 示例脚本
展示如何使用 Genos DNA 分析工具的各种功能
"""

import sys
import json
from genos_dna import (
    analyze_dna_sequence,
    predict_next_base,
    extract_sequence_features
)


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_1_simple_analysis():
    """示例 1: 简单序列分析"""
    print_header("示例 1: 简单序列分析")
    
    sequence = "ACGTACGTACGTACGTACGT"
    print(f"输入序列: {sequence}")
    
    result = analyze_dna_sequence(sequence)
    
    print(f"\n分析结果:")
    print(f"  原始长度: {result['original_length']}")
    print(f"  清理长度: {result['cleaned_length']}")
    print(f"  GC 含量: {result['gc_content']:.2f}%")
    print(f"  序列预览: {result['sequence_preview']}")
    
    print(f"\n碱基频率:")
    for base, count in result['base_frequency'].items():
        percentage = (count / result['cleaned_length']) * 100
        print(f"  {base}: {count} ({percentage:.2f}%)")


def example_2_base_prediction():
    """示例 2: 碱基预测"""
    print_header("示例 2: 碱基预测")
    
    sequence = "ACGTACGTACGT"
    print(f"输入序列: {sequence}")
    
    predictions = predict_next_base(sequence, top_k=5)
    
    print(f"\n预测结果 (Top 5):")
    print(f"  输入序列: {predictions['input_sequence']}")
    
    for i, pred in enumerate(predictions['predictions'], 1):
        print(f"  {i}. 碱基: {pred['base']}, 概率: {pred['probability']:.4f}")


def example_3_feature_extraction():
    """示例 3: 特征提取"""
    print_header("示例 3: 序列特征提取")
    
    sequence = "ACGTACGTACGT"
    print(f"输入序列: {sequence}")
    
    features = extract_sequence_features(sequence)
    
    print(f"\n序列特征:")
    print(f"  长度: {features['length']}")
    print(f"  GC 含量: {features['gc_content']}")
    print(f"  AT 含量: {features['at_content']}")
    
    print(f"\n碱基组成:")
    for base, percentage in features['base_composition'].items():
        print(f"  {base}: {percentage}")
    
    print(f"\n模型信息:")
    for key, value in features['model_info'].items():
        print(f"  {key}: {value}")


def example_4_batch_analysis():
    """示例 4: 批量分析"""
    print_header("示例 4: 批量序列分析")
    
    sequences = [
        "ACGTACGTACGT",
        "TTATATATATAT",
        "GCGCGCGCGCGC",
        "NNNNACGTACGT",
        "ACGT" * 10
    ]
    
    print(f"分析 {len(sequences)} 个序列:\n")
    
    for i, seq in enumerate(sequences, 1):
        result = analyze_dna_sequence(seq)
        print(f"序列 {i}: {seq[:15]}{'...' if len(seq) > 15 else ''}")
        print(f"  长度: {result['cleaned_length']}, GC: {result['gc_content']:.2f}%")


def example_5_advanced_usage():
    """示例 5: 高级用法"""
    print_header("示例 5: 高级用法 - 组合分析")
    
    sequence = "ACGTACGTACGTACGTACGTACGTACGTACGT"
    print(f"输入序列: {sequence[:30]}... (长度: {len(sequence)})")
    
    # 分析序列
    analysis = analyze_dna_sequence(sequence)
    
    # 预测下一个碱基
    predictions = predict_next_base(sequence, top_k=3)
    
    # 提取特征
    features = extract_sequence_features(sequence)
    
    print(f"\n综合分析结果:")
    print(f"  序列长度: {analysis['cleaned_length']}")
    print(f"  GC 含量: {analysis['gc_content']:.2f}%")
    print(f"  AT 含量: {features['at_content']}")
    
    print(f"\n预测下一个碱基:")
    for pred in predictions['predictions']:
        print(f"  {pred['base']}: {pred['probability']:.4f}")
    
    print(f"\n模型信息: {features['model_info']['name']}")


def example_6_cli_usage():
    """示例 6: 命令行用法"""
    print_header("示例 6: 命令行用法")
    
    print("\n命令行使用示例:")
    print("  # 分析 DNA 序列")
    print("  python scripts/genos_dna.py analyze 'ACGTACGTACGT'")
    print("")
    print("  # 预测下一个碱基")
    print("  python scripts/genos_dna.py predict 'ACGTACGT' --top_k 5")
    print("")
    print("  # 提取序列特征")
    print("  python scripts/genos_dna.py features 'ACGTACGTACGT'")
    print("")
    print("  # 查看帮助")
    print("  python scripts/genos_dna.py --help")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  Genos DNA 序列分析 - 示例脚本")
    print("=" * 60)
    
    print("\n可用示例:")
    print("  1. 简单序列分析")
    print("  2. 碱基预测")
    print("  3. 序列特征提取")
    print("  4. 批量序列分析")
    print("  5. 高级用法 - 组合分析")
    print("  6. 命令行用法")
    
    print("\n运行所有示例...")
    
    example_1_simple_analysis()
    example_2_base_prediction()
    example_3_feature_extraction()
    example_4_batch_analysis()
    example_5_advanced_usage()
    example_6_cli_usage()
    
    print_header("所有示例完成！")
    print("\n如需运行特定示例，请编辑此脚本并取消相应函数的注释")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n错误: {e}")
        sys.exit(1)
