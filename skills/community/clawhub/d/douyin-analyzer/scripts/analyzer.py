#!/usr/bin/env python3
"""
Douyin Analyzer - 内容分析模块

对转录文本进行智能分析：
- 基础文本清理（去除口语填充词、修复标点）
- 语义分段（基础规则分段，复杂分段建议由 LLM 完成）
- 要点提取（基础关键词匹配，深度提取建议由 LLM 完成）
- 智能总结（基础摘要，高质量总结建议由 LLM 完成）

设计原则：
- 本模块提供基础的文本处理能力
- 高质量的语义分析（分段、总结、要点提取）应由 OpenClaw agent（LLM）直接完成
- 本模块的输出可作为 LLM 分析的预处理输入
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional

# 配置路径
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "skills" / "douyin-config.json"
FALLBACK_CONFIG_PATH = Path.home() / ".openclaw" / "config.json"


def load_douyin_config() -> Dict:
    """加载抖音模块配置"""
    if DEFAULT_CONFIG_PATH.exists():
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    if FALLBACK_CONFIG_PATH.exists():
        with open(FALLBACK_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get("douyin", {})
    return {}


class DouyinAnalyzer:
    """内容分析器
    
    提供基础文本处理。高质量语义分析建议由 LLM 完成。
    """
    
    # 中文口语填充词（独立出现时去除）
    # 注意：中文没有 word boundary，需要用上下文判断
    FILLER_PATTERNS = [
        # 句首/句尾填充词
        r'^[嗯啊呃哦哈]+[，、]?\s*',       # 句首语气词
        r'\s*[嗯啊呃哦哈]+[。！？]?$',     # 句尾语气词
        # 句中独立填充词（前后有标点）
        r'[，。！？、]\s*就是说\s*[，。！？、]',
        r'[，。！？、]\s*然后呢\s*[，。！？、]',
        r'[，。！？、]\s*对吧\s*[，。！？、]',
        r'[，。！？、]\s*是吧\s*[，。！？、]',
        r'[，。！？、]\s*你知道吗\s*[，。！？、]',
        r'[，。！？、]\s*怎么说呢\s*[，。！？、]',
    ]
    
    # 重复标点修复
    PUNCT_FIXES = [
        (r'[，]{2,}', '，'),
        (r'[。]{2,}', '。'),
        (r'[！]{2,}', '！'),
        (r'[？]{2,}', '？'),
        (r'[、]{2,}', '、'),
        (r'，。', '。'),
        (r'。，', '。'),
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or load_douyin_config()
        
    def analyze(self, text: str, options: Optional[Dict] = None) -> Dict:
        """分析文本
        
        Args:
            text: 转录文本
            options: 分析选项
                - formalize: 去除口语化（默认 True）
                - segment: 语义分段（默认 True）
                - extract_points: 提取要点（默认 True）
                - summarize: 生成总结（默认 True）
            
        Returns:
            {
                "success": bool,
                "cleaned_text": str,        # 清理后的文本
                "segments": list,            # 分段结果
                "key_points": list,          # 要点列表
                "summary": str,              # 基础总结
                "char_count": int,           # 字符数
                "estimated_duration_min": float,  # 估计时长（分钟）
                "llm_prompt": str            # 供 LLM 深度分析的提示词
            }
        """
        options = options or {}
        
        result = {
            "success": True,
            "char_count": len(text),
            "estimated_duration_min": round(len(text) / 250, 1)  # 中文约 250 字/分钟
        }
        
        # 1. 基础文本清理
        if options.get("formalize", True):
            result["cleaned_text"] = self.clean_text(text)
        else:
            result["cleaned_text"] = text
        
        cleaned = result["cleaned_text"]
        
        # 2. 基础分段
        if options.get("segment", True):
            result["segments"] = self.segment_text(cleaned)
        
        # 3. 基础要点提取
        if options.get("extract_points", True):
            result["key_points"] = self.extract_points(cleaned)
        
        # 4. 基础总结
        if options.get("summarize", True):
            result["summary"] = self.basic_summarize(cleaned)
        
        # 5. 生成 LLM 深度分析提示词
        result["llm_prompt"] = self.generate_llm_prompt(cleaned)
        
        return result
    
    def clean_text(self, text: str) -> str:
        """清理文本：去除口语填充词、修复标点、去除多余空白
        
        Args:
            text: 原始转录文本
            
        Returns:
            清理后的文本
        """
        cleaned = text
        
        # 按句子处理填充词
        sentences = re.split(r'([。！？])', cleaned)
        processed = []
        for i, part in enumerate(sentences):
            if part in '。！？':
                processed.append(part)
                continue
            
            sentence = part
            # 去除句首语气词
            sentence = re.sub(r'^[嗯啊呃哦哈呀吧嘛]+[，、]?\s*', '', sentence)
            # 去除句尾语气词
            sentence = re.sub(r'\s*[嗯啊呃哦哈呀吧嘛]+$', '', sentence)
            
            processed.append(sentence)
        
        cleaned = ''.join(processed)
        
        # 去除句中独立填充短语
        for pattern in self.FILLER_PATTERNS:
            cleaned = re.sub(pattern, '，', cleaned)
        
        # 修复标点
        for pattern, replacement in self.PUNCT_FIXES:
            cleaned = re.sub(pattern, replacement, cleaned)
        
        # 去除多余空白
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned
    
    def segment_text(self, text: str) -> List[Dict]:
        """基础语义分段
        
        策略：按自然段落和长度分段
        - 如果文本有换行符，按换行分段
        - 否则按句号分段，每段 100-300 字
        
        注意：这是基础分段，高质量语义分段应由 LLM 完成
        """
        # 如果有换行符，按换行分段
        if '\n' in text:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            if len(paragraphs) > 1:
                return [
                    {"id": i+1, "text": p}
                    for i, p in enumerate(paragraphs)
                ]
        
        # 按句号分段
        sentences = re.split(r'(?<=[。！？])', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        segments = []
        current = ""
        seg_id = 1
        
        for sentence in sentences:
            current += sentence
            
            # 达到合理长度，创建段落
            if len(current) >= 150:
                segments.append({
                    "id": seg_id,
                    "text": current.strip()
                })
                seg_id += 1
                current = ""
        
        # 处理剩余
        if current.strip():
            if segments and len(current) < 50:
                # 太短，追加到最后一段
                segments[-1]["text"] += current
            else:
                segments.append({
                    "id": seg_id,
                    "text": current.strip()
                })
        
        # 如果只有一段且很长，强制分段
        if len(segments) == 1 and len(segments[0]["text"]) > 500:
            long_text = segments[0]["text"]
            segments = []
            sentences = re.split(r'(?<=[。！？])', long_text)
            current = ""
            seg_id = 1
            for sentence in sentences:
                current += sentence
                if len(current) >= 200:
                    segments.append({"id": seg_id, "text": current.strip()})
                    seg_id += 1
                    current = ""
            if current.strip():
                segments.append({"id": seg_id, "text": current.strip()})
        
        return segments if segments else [{"id": 1, "text": text}]
    
    def extract_points(self, text: str) -> List[str]:
        """基础要点提取
        
        策略：提取包含关键信号词的句子
        注意：这是基础提取，高质量要点提取应由 LLM 完成
        """
        signal_words = [
            "重点是", "关键是", "核心是", "本质是",
            "首先", "其次", "最后", "第一", "第二", "第三",
            "总结", "结论", "建议", "注意",
            "最重要的", "一定要", "千万不要", "必须",
            "换句话说", "也就是说", "简单来说"
        ]
        
        # 按句子拆分
        sentences = re.split(r'(?<=[。！？])', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        
        points = []
        for sentence in sentences:
            for signal in signal_words:
                if signal in sentence:
                    points.append(sentence)
                    break
        
        # 去重
        seen = set()
        unique_points = []
        for p in points:
            if p not in seen:
                seen.add(p)
                unique_points.append(p)
        
        return unique_points[:15]  # 最多 15 个
    
    def basic_summarize(self, text: str) -> str:
        """基础总结
        
        策略：提取首段和尾段作为概要
        注意：这是基础总结，高质量总结应由 LLM 完成
        """
        if len(text) <= 200:
            return text
        
        sentences = re.split(r'(?<=[。！？])', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        
        if len(sentences) <= 3:
            return text
        
        # 取前 2 句 + 后 1 句
        summary_parts = sentences[:2] + ["..."] + sentences[-1:]
        return ''.join(summary_parts)
    
    def generate_llm_prompt(self, text: str) -> str:
        """生成供 LLM 深度分析的提示词
        
        当 agent 需要更高质量的分析时，可以将此提示词和文本一起发给 LLM
        """
        char_count = len(text)
        est_minutes = round(char_count / 250, 1)
        
        return f"""请对以下转录文本进行深度分析（约 {char_count} 字，估计 {est_minutes} 分钟内容）：

1. **语义分段**：按主题/话题将文本分成若干段落，每段加上小标题
2. **核心要点**：提取 3-7 个核心观点或关键信息
3. **内容总结**：用 100-200 字概括全文核心内容
4. **口语化处理**：将口语表达转为书面语，保留所有要点，不做摘要压缩

转录文本：
---
{text[:500]}{'...(已截断，完整文本请直接传入)' if len(text) > 500 else ''}
---"""


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="内容分析模块")
    parser.add_argument("input", help="输入文件路径或文本")
    parser.add_argument("--action", 
                       choices=["clean", "segment", "extract_points", "summarize", "full", "llm_prompt"],
                       default="full",
                       help="分析类型")
    parser.add_argument("-o", "--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 读取输入
    if os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.input
    
    analyzer = DouyinAnalyzer()
    
    if args.action == "clean":
        result = analyzer.clean_text(text)
        print(result)
    elif args.action == "segment":
        result = analyzer.segment_text(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "extract_points":
        result = analyzer.extract_points(text)
        for i, p in enumerate(result, 1):
            print(f"{i}. {p}")
    elif args.action == "summarize":
        result = analyzer.basic_summarize(text)
        print(result)
    elif args.action == "llm_prompt":
        result = analyzer.generate_llm_prompt(text)
        print(result)
    else:  # full
        result = analyzer.analyze(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.output and args.action == "full":
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 已保存到: {args.output}")


if __name__ == "__main__":
    main()