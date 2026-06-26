#!/usr/bin/env python3
"""
AI味去除工具 - 自动检测并替换AI味词汇，优化文风
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple


# AI味词汇及替换建议
AI_WORDS_REPLACEMENTS = {
    # 过渡词
    "值得一提的是": ["", "有意思的是", ""],
    "不难发现": ["", "一眼就能看出", ""],
    "从某种意义上说": ["", "说白了", ""],
    "总的来说": ["", "总之", ""],
    "总而言之": ["总之", ""],
    "综上所述": ["", "所以", ""],
    "由此可见": ["", "显然", ""],
    "显而易见": ["", "明眼人都看得出", ""],
    "毫无疑问": ["", "毫无疑问地", ""],
    "不可否认": ["", "确实", ""],
    "必须承认": ["", "说实话", ""],
    "客观地说": ["", "", ""],
    "平心而论": ["", "老实说", ""],
    "老实说": ["", ""],
    "说实话": ["", ""],
    
    # 逻辑连接词过度使用 - 建议删除或替换
    "然而": ["但", "不过", "可"],
    "因此": ["所以", "于是", ""],
    "于是": ["", "就", ""],
    "所以": ["", "于是", ""],
    "但是": ["但", "不过", "可"],
    "不过": ["但", "可", ""],
    "可是": ["但", "", ""],
    "虽然": ["", "尽管", ""],
    "尽管": ["", "虽然", ""],
    "即使": ["", "就算", ""],
    "既然": ["", ""],
    "由于": ["", "因为", ""],
    "因为": ["", ""],
    
    # 空洞修饰词 - 建议删除
    "非常": ["", "够", "很是"],
    "极其": ["", "", ""],
    "无比": ["", "", ""],
    "相当": ["", "挺", ""],
    "特别": ["", "格外", ""],
    "十分": ["", "", ""],
    "格外": ["", "特别", ""],
    "太": ["", "过于", ""],
    "很": ["", "挺", ""],
    "最": ["", ""],
    "更": ["", "更加", ""],
    "比较": ["", "还算", ""],
    "稍微": ["", "稍稍", ""],
    
    # 抽象概括词 - 建议删除
    "一定程度上": ["", "", ""],
    "某种意义上": ["", "", ""],
    "某种程度上": ["", "", ""],
    "某种程度上说": ["", "", ""],
    "从某种角度来看": ["", "", ""],
    "从某种意义上": ["", "", ""],
    "从某种程度上": ["", "", ""],
    
    # 书面化表达 - 简化
    "进行了": ["", ""],
    "做出了": ["", ""],
    "给予了": ["给", ""],
    "提供了": ["给", "提供"],
    "展示了": ["露出", "展现", ""],
    "体现了": ["显出", "", ""],
    "表现了": ["显出", "", ""],
    "反映了": ["", "", ""],
    "代表了": ["", "", ""],
    "意味着": ["说明", "代表", ""],
    
    # 冗余表达 - 删除
    "可以说": ["", ""],
    "也就是说": ["", "", ""],
    "换句话说": ["", "", ""],
    "换言之": ["", "", ""],
    "简单来说": ["", "", ""],
    "简而言之": ["", "", ""],
    "说白了": ["", "", ""],
    "事实上": ["", "", ""],
    "实际上": ["", "", ""],
    "其实": ["", "", ""],
    "本来": ["", "", ""],
    "原本": ["", "", ""],
    "本来就已经": ["", "", ""],
    
    # 过度解释 - 删除
    "这意味着": ["", ""],
    "这表明": ["", ""],
    "这说明": ["", ""],
    "这证明": ["", ""],
    "这反映出": ["", ""],
    "这体现了": ["", ""],
    "这显示了": ["", ""],
    "这暗示了": ["", ""],
}


class AITasteRemover:
    """AI味去除器"""
    
    def __init__(self, content: str):
        self.original = content
        self.content = content
        self.changes = []
    
    def remove_ai_taste(self, aggressive: bool = False) -> str:
        """
        去除AI味
        
        Args:
            aggressive: 是否激进模式（更多替换）
        
        Returns:
            处理后的文本
        """
        self.changes = []
        
        # 1. 替换AI味词汇
        for word, replacements in AI_WORDS_REPLACEMENTS.items():
            if word in self.content:
                # 统计出现次数
                count = self.content.count(word)
                
                # 选择替换词（第一个非空选项）
                replacement = next((r for r in replacements if r), "")
                
                # 执行替换
                self.content = self.content.replace(word, replacement)
                
                self.changes.append({
                    "type": "词汇替换",
                    "original": word,
                    "replacement": replacement if replacement else "[删除]",
                    "count": count
                })
        
        # 2. 清理多余空格
        self.content = re.sub(r'  +', ' ', self.content)
        
        # 3. 清理空行
        self.content = re.sub(r'\n\n\n+', '\n\n', self.content)
        
        # 4. 激进模式：进一步简化
        if aggressive:
            self._aggressive_cleanup()
        
        return self.content
    
    def _aggressive_cleanup(self):
        """激进清理"""
        # 删除句首的"而"、"但"等（如果前面是段落开头）
        self.content = re.sub(r'\n\s*而', '\n', self.content)
        self.content = re.sub(r'\n\s*但', '\n', self.content)
        
        # 简化"XX地说道" -> "XX道"
        self.content = re.sub(r'([\u4e00-\u9fa5]{1,4})地说道', r'\1道', self.content)
        
        # 简化"XX地笑了" -> "XX笑了"
        self.content = re.sub(r'([\u4e00-\u9fa5]{1,4})地笑了', r'\1笑了', self.content)
    
    def optimize_dialogue(self) -> str:
        """优化对话"""
        # 简化对话标签
        # "XXX。"他说道。 -> "XXX。"他说。
        self.content = re.sub(r'(["""」』])[^\u4e00-\u9fa5]*说道。', r'\1他说。', self.content)
        
        # 减少"了"的使用
        # 但保留语义必要的"了"
        # 这是一个复杂的NLP问题，这里做简单处理
        
        return self.content
    
    def enhance_pacing(self) -> str:
        """增强节奏感"""
        # 将长段落拆分
        lines = self.content.split('\n')
        new_lines = []
        
        for line in lines:
            if len(line) > 200 and '。' in line:
                # 尝试在句号处拆分
                parts = line.split('。')
                if len(parts) > 2:
                    # 每2-3句一段
                    for i in range(0, len(parts)-1, 2):
                        segment = '。'.join(parts[i:i+2]) + '。'
                        new_lines.append(segment)
                    if len(parts) % 2 == 0:
                        new_lines.append(parts[-1])
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        self.content = '\n'.join(new_lines)
        return self.content
    
    def get_changes_report(self) -> str:
        """获取修改报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("AI味去除报告")
        lines.append("=" * 60)
        
        if not self.changes:
            lines.append("未发现明显的AI味词汇")
            return '\n'.join(lines)
        
        lines.append(f"共处理 {len(self.changes)} 类词汇\n")
        
        for change in self.changes:
            lines.append(f"• '{change['original']}' -> '{change['replacement']}' (出现{change['count']}次)")
        
        # 统计
        original_words = len(self.original.replace(' ', '').replace('\n', ''))
        new_words = len(self.content.replace(' ', '').replace('\n', ''))
        reduction = original_words - new_words
        
        lines.append(f"\n字数变化：{original_words} -> {new_words} (减少{reduction}字)")
        lines.append("=" * 60)
        
        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: ai_taste_remover.py <file_path> [--aggressive]")
        print("       ai_taste_remover.py --text \"要处理的文本\" [--aggressive]")
        return
    
    aggressive = "--aggressive" in sys.argv
    
    if sys.argv[1] == "--text":
        content = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"错误：文件不存在 {file_path}")
            return
        content = file_path.read_text(encoding='utf-8')
    
    remover = AITasteRemover(content)
    result = remover.remove_ai_taste(aggressive=aggressive)
    
    print(remover.get_changes_report())
    print("\n【处理后的文本】\n")
    print(result)


if __name__ == "__main__":
    main()
