#!/usr/bin/env python3
"""
风格检查工具 - 检测AI味词汇，提供爽文写作建议
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter

# AI味词汇列表
AI_WORDS = [
    # 过渡词滥用
    "值得一提的是", "不难发现", "从某种意义上说", "总的来说", "总而言之",
    "综上所述", "由此可见", "显而易见", "毫无疑问", "不可否认",
    "必须承认", "客观地说", "平心而论", "老实说", "说实话",
    
    # 逻辑连接词过度使用
    "然而", "因此", "于是", "所以", "但是", "不过", "可是",
    "虽然", "尽管", "即使", "既然", "由于", "因为",
    
    # 空洞修饰词
    "非常", "极其", "无比", "相当", "特别", "十分", "格外",
    "太", "很", "最", "更", "比较", "稍微",
    
    # 抽象概括词
    "一定程度上", "某种意义上", "某种程度上", "某种程度上说",
    "从某种角度来看", "从某种意义上", "从某种程度上",
    
    # 书面化表达
    "进行了", "做出了", "给予了", "提供了", "展示了",
    "体现了", "表现了", "反映了", "代表了", "意味着",
    
    # 冗余表达
    "可以说", "可以说，", "也就是说", "换句话说", "换言之",
    "简单来说", "简而言之", "说白了", "事实上", "实际上",
    "其实", "本来", "原本", "本来就已经",
    
    # 过度解释
    "这意味着", "这表明", "这说明", "这证明", "这反映出",
    "这体现了", "这显示了", "这暗示了",
]

# 爽点关键词
SHUANGDIAN_WORDS = [
    "震惊", "不可思议", "难以置信", "骇然", "惊骇", "惊呆",
    "碾压", "秒杀", "吊打", "虐杀", "横扫", "无敌",
    "突破", "升级", "进阶", "蜕变", "觉醒", "爆发",
    "打脸", "装逼", "反转", "逆袭", "崛起", "腾飞",
    "奖励", "获得", "解锁", "激活", "开启", "觉醒",
]

# 对话标记
DIALOGUE_MARKERS = ['"', '"', '"', '"', '"""', "'''", "「", "」", "『", "』"]


class StyleChecker:
    """风格检查器"""
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.words = self._extract_words()
    
    def _extract_words(self) -> List[str]:
        """提取所有词语"""
        # 移除标点，保留中文和英文单词
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', self.content)
        return text.split()
    
    def check_ai_words(self) -> List[Dict]:
        """检查AI味词汇"""
        issues = []
        
        for ai_word in AI_WORDS:
            count = self.content.count(ai_word)
            if count > 0:
                # 找出出现位置
                positions = []
                start = 0
                while True:
                    idx = self.content.find(ai_word, start)
                    if idx == -1:
                        break
                    # 找到所在行
                    line_num = self.content[:idx].count('\n') + 1
                    positions.append(line_num)
                    start = idx + len(ai_word)
                
                issues.append({
                    "word": ai_word,
                    "count": count,
                    "lines": positions[:5],  # 最多显示5个位置
                    "severity": "high" if count > 3 else "medium"
                })
        
        return sorted(issues, key=lambda x: x["count"], reverse=True)
    
    def check_sentence_patterns(self) -> List[Dict]:
        """检查句式问题"""
        issues = []
        
        # 检查长句（超过50字）
        long_sentences = []
        sentences = re.split(r'[。！？]', self.content)
        for i, sent in enumerate(sentences):
            if len(sent) > 50:
                long_sentences.append({
                    "line": i + 1,
                    "length": len(sent),
                    "preview": sent[:30] + "..."
                })
        
        if len(long_sentences) > 5:
            issues.append({
                "type": "长句过多",
                "count": len(long_sentences),
                "examples": long_sentences[:3],
                "suggestion": "适当拆分长句，增加节奏感"
            })
        
        # 检查连续短句
        short_sentence_pattern = r'([。！？][^。！？]{1,10}[。！？]){3,}'
        matches = re.findall(short_sentence_pattern, self.content)
        if len(matches) > 10:
            issues.append({
                "type": "短句堆砌",
                "count": len(matches),
                "suggestion": "避免连续使用过多短句，适当使用复合句"
            })
        
        return issues
    
    def check_dialogue_ratio(self) -> Dict:
        """检查对话比例"""
        # 简单估算对话内容（引号内的内容）
        dialogue_chars = 0
        
        # 匹配双引号内容
        dialogue_pattern = r'["""]([^"""]+)["""]'
        for match in re.finditer(dialogue_pattern, self.content):
            dialogue_chars += len(match.group(1))
        
        # 匹配中文引号
        dialogue_pattern2 = r'[「『]([^」』]+)[」』]'
        for match in re.finditer(dialogue_pattern2, self.content):
            dialogue_chars += len(match.group(1))
        
        total_chars = len(self.content.replace(' ', '').replace('\n', ''))
        ratio = dialogue_chars / total_chars if total_chars > 0 else 0
        
        return {
            "dialogue_chars": dialogue_chars,
            "total_chars": total_chars,
            "ratio": ratio,
            "percentage": f"{ratio*100:.1f}%",
            "assessment": "对话比例适中" if 0.2 <= ratio <= 0.5 else 
                         "对话偏少，建议增加互动" if ratio < 0.2 else 
                         "对话偏多，注意叙事平衡"
        }
    
    def check_shuangdian_density(self) -> Dict:
        """检查爽点密度"""
        shuangdian_count = 0
        found_words = []
        
        for word in SHUANGDIAN_WORDS:
            count = self.content.count(word)
            if count > 0:
                shuangdian_count += count
                found_words.append((word, count))
        
        total_chars = len(self.content.replace(' ', '').replace('\n', ''))
        density = shuangdian_count / (total_chars / 1000) if total_chars > 0 else 0
        
        return {
            "count": shuangdian_count,
            "density_per_1000": density,
            "found_words": sorted(found_words, key=lambda x: x[1], reverse=True)[:10],
            "assessment": "爽点充足" if density >= 3 else 
                         "爽点偏少，建议增加" if density < 2 else 
                         "爽点适中"
        }
    
    def check_pacing(self) -> Dict:
        """检查节奏"""
        # 检查段落长度分布
        paragraphs = [p for p in self.content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return {"assessment": "无法分析"}
        
        lengths = [len(p) for p in paragraphs]
        avg_length = sum(lengths) / len(lengths)
        max_length = max(lengths)
        min_length = min(lengths)
        
        # 检查是否有大段叙述
        long_paragraphs = [i for i, l in enumerate(lengths) if l > 500]
        
        return {
            "paragraph_count": len(paragraphs),
            "avg_length": int(avg_length),
            "max_length": max_length,
            "min_length": min_length,
            "long_paragraphs": len(long_paragraphs),
            "assessment": "节奏良好" if avg_length < 300 and len(long_paragraphs) < 3 else
                         "存在大段叙述，建议分段增加节奏感"
        }
    
    def generate_report(self) -> str:
        """生成完整报告"""
        report = []
        report.append("=" * 60)
        report.append("小说风格检查报告")
        report.append("=" * 60)
        
        # 基础统计
        total_chars = len(self.content.replace(' ', '').replace('\n', ''))
        report.append(f"\n【基础统计】")
        report.append(f"总字数：{total_chars}")
        report.append(f"总行数：{len(self.lines)}")
        
        # AI味检查
        report.append(f"\n【AI味词汇检查】")
        ai_issues = self.check_ai_words()
        if ai_issues:
            report.append(f"发现 {len(ai_issues)} 个AI味词汇：")
            for issue in ai_issues[:10]:
                lines_str = ", ".join(map(str, issue["lines"]))
                report.append(f"  - '{issue['word']}'：出现{issue['count']}次 (行: {lines_str})")
        else:
            report.append("未发现明显AI味词汇 ✓")
        
        # 句式检查
        report.append(f"\n【句式检查】")
        sentence_issues = self.check_sentence_patterns()
        if sentence_issues:
            for issue in sentence_issues:
                report.append(f"  ⚠ {issue['type']}：{issue['count']}处")
                report.append(f"    建议：{issue['suggestion']}")
        else:
            report.append("句式结构良好 ✓")
        
        # 对话比例
        report.append(f"\n【对话比例】")
        dialogue_info = self.check_dialogue_ratio()
        report.append(f"  对话占比：{dialogue_info['percentage']}")
        report.append(f"  评估：{dialogue_info['assessment']}")
        
        # 爽点密度
        report.append(f"\n【爽点密度】")
        shuangdian_info = self.check_shuangdian_density()
        report.append(f"  爽点词频：{shuangdian_info['count']}次")
        report.append(f"  每千字密度：{shuangdian_info['density_per_1000']:.1f}")
        report.append(f"  评估：{shuangdian_info['assessment']}")
        if shuangdian_info['found_words']:
            words_str = ", ".join([f"{w}({c})" for w, c in shuangdian_info['found_words'][:5]])
            report.append(f"  高频爽点词：{words_str}")
        
        # 节奏检查
        report.append(f"\n【节奏检查】")
        pacing_info = self.check_pacing()
        report.append(f"  段落数：{pacing_info['paragraph_count']}")
        report.append(f"  平均段落长度：{pacing_info['avg_length']}字")
        report.append(f"  超长段落：{pacing_info['long_paragraphs']}个")
        report.append(f"  评估：{pacing_info['assessment']}")
        
        # 总体建议
        report.append(f"\n【总体建议】")
        suggestions = []
        
        if ai_issues:
            suggestions.append("- 减少AI味词汇使用，让文字更自然")
        if dialogue_info['ratio'] < 0.15:
            suggestions.append("- 适当增加对话，增强场景感")
        if shuangdian_info['density_per_1000'] < 2:
            suggestions.append("- 增加爽点密度，保持读者期待感")
        if pacing_info['long_paragraphs'] > 3:
            suggestions.append("- 拆分长段落，加快阅读节奏")
        
        if suggestions:
            report.extend(suggestions)
        else:
            report.append("整体风格良好，保持当前写作状态！")
        
        report.append("\n" + "=" * 60)
        
        return '\n'.join(report)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: style_checker.py <file_path>")
        print("       style_checker.py --text \"要检查的文本\"")
        return
    
    if sys.argv[1] == "--text":
        content = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"错误：文件不存在 {file_path}")
            return
        content = file_path.read_text(encoding='utf-8')
    
    checker = StyleChecker(content)
    print(checker.generate_report())


if __name__ == "__main__":
    main()
