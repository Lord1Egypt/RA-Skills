#!/usr/bin/env python3
"""
Diataxis 文档类型诊断工具

分析文档内容，识别主导类型并给出建议。

使用方法:
    python3 diagnose.py <文档内容或文件路径>
    python3 diagnose.py --text "文档内容..."
    python3 diagnose.py --file path/to/doc.md
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple


class DiataxisDiagnoser:
    """Diataxis 文档类型诊断器"""
    
    # 类型特征关键词
    TUTORIAL_PATTERNS = [
        r'在这个教程中',
        r'我们将',
        r'首先.*然后',
        r'现在.*做',
        r'你将看到',
        r'注意.*',
        r'记住.*',
        r'让我们检查',
        r'先决条件',
        r'你将学到',
    ]
    
    HOW_TO_PATTERNS = [
        r'如何.*',
        r'如果要.*做',
        r'步骤.*',
        r'配置.*',
        r'安装.*',
        r'部署.*',
        r'解决.*问题',
        r'故障排除',
        r'验证.*',
        r'适用场景',
    ]
    
    REFERENCE_PATTERNS = [
        r'参数.*',
        r'返回值.*',
        r'类型.*',
        r'默认值.*',
        r'语法.*',
        r'子命令.*',
        r'选项.*',
        r'API.*',
        r'配置项.*',
        r'有效范围.*',
    ]
    
    EXPLANATION_PATTERNS = [
        r'为什么.*',
        r'原因是.*',
        r'相比之下.*',
        r'从.*角度来看',
        r'设计决策.*',
        r'权衡.*',
        r'背景.*',
        r'历史.*',
        r'原理.*',
        r'概念.*',
    ]
    
    def __init__(self):
        self.scores = {
            'Tutorial': 0,
            'How-to': 0,
            'Reference': 0,
            'Explanation': 0,
        }
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """分析文本，返回各类型得分"""
        
        # 统计各类型特征匹配
        self.scores['Tutorial'] = self._count_patterns(text, self.TUTORIAL_PATTERNS)
        self.scores['How-to'] = self._count_patterns(text, self.HOW_TO_PATTERNS)
        self.scores['Reference'] = self._count_patterns(text, self.REFERENCE_PATTERNS)
        self.scores['Explanation'] = self._count_patterns(text, self.EXPLANATION_PATTERNS)
        
        # 归一化
        total = sum(self.scores.values())
        if total > 0:
            for key in self.scores:
                self.scores[key] = (self.scores[key] / total) * 100
        
        return self.scores
    
    def _count_patterns(self, text: str, patterns: List[str]) -> int:
        """统计匹配的模式数量"""
        count = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    def get_primary_type(self) -> Tuple[str, float]:
        """获取主导类型"""
        primary = max(self.scores, key=self.scores.get)
        return primary, self.scores[primary]
    
    def get_suggestions(self) -> List[str]:
        """根据分析结果给出建议"""
        suggestions = []
        primary_type, score = self.get_primary_type()
        
        if score < 50:
            suggestions.append("⚠️  文档类型不够明确，可能需要重新定位")
        
        # 检查类型混淆
        high_scores = [k for k, v in self.scores.items() if v > 30]
        if len(high_scores) > 1:
            suggestions.append(f"⚠️  可能混合了类型：{', '.join(high_scores)}")
            suggestions.append("   建议：分离不同类型的内容到独立文档")
        
        # 针对主导类型的建议
        if primary_type == 'Tutorial' and self.scores['Explanation'] > 30:
            suggestions.append("💡 Tutorial 中 Explanation 内容过多，考虑删除或链接到解释文档")
        
        if primary_type == 'How-to' and self.scores['Tutorial'] > 30:
            suggestions.append("💡 How-to 中 Tutorial 内容过多，假设读者已有基础能力")
        
        if primary_type == 'Reference' and self.scores['Explanation'] > 20:
            suggestions.append("💡 Reference 应保持纯描述，移除解释性内容")
        
        if primary_type == 'Explanation' and self.scores['How-to'] > 30:
            suggestions.append("💡 Explanation 中混入指导内容，考虑分离到 How-to")
        
        return suggestions
    
    def print_report(self):
        """打印诊断报告"""
        print("\n" + "="*60)
        print("Diataxis 文档类型诊断报告")
        print("="*60 + "\n")
        
        print("类型分布:")
        for doc_type, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(score / 5)
            print(f"  {doc_type:12} {score:5.1f}% {bar}")
        
        primary, score = self.get_primary_type()
        print(f"\n📌 主导类型：{primary} ({score:.1f}%)")
        
        suggestions = self.get_suggestions()
        if suggestions:
            print("\n建议:")
            for suggestion in suggestions:
                print(f"  {suggestion}")
        
        print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Diataxis 文档类型诊断工具')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', '-t', help='直接输入文档内容')
    group.add_argument('--file', '-f', help='文档文件路径')
    
    args = parser.parse_args()
    
    # 获取文档内容
    if args.text:
        content = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"错误：文件不存在 - {args.file}")
            sys.exit(1)
        except Exception as e:
            print(f"错误：读取文件失败 - {e}")
            sys.exit(1)
    else:
        print("错误：请提供 --text 或 --file 参数")
        sys.exit(1)
    
    # 诊断
    diagnoser = DiataxisDiagnoser()
    diagnoser.analyze_text(content)
    diagnoser.print_report()


if __name__ == '__main__':
    main()
