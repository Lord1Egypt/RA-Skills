#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级文档分块器 (Advanced Document Chunker)

参考Dify的分块策略，实现多种智能分块模式：
1. 通用模式 (General Mode) - 单层分块
2. 父子模式 (Parent-Child Mode) - 层次化分块
3. 语义感知分块 (Semantic-Aware Chunking)
4. 结构感知分块 (Structure-Aware Chunking)

核心特性:
- 多种分块策略
- 智能分隔符检测
- 上下文保持
- 语义边界识别
- 自动摘要生成

作者: OpenClaw Team
版本: 1.0.0
参考: Dify Chunking Strategy, Academic Research
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import jieba
import jieba.analyse

# 设置日志
logger = logging.getLogger(__name__)


class ChunkMode(Enum):
    """分块模式"""
    GENERAL = "general"              # 通用模式
    PARENT_CHILD = "parent_child"    # 父子模式
    SEMANTIC = "semantic"            # 语义感知模式
    STRUCTURE = "structure"          # 结构感知模式


class DelimiterType(Enum):
    """分隔符类型"""
    PARAGRAPH = "paragraph"          # 段落分隔 (\n\n)
    SENTENCE = "sentence"            # 句子分隔 (。！？)
    LINE = "line"                   # 行分隔 (\n)
    CUSTOM = "custom"               # 自定义分隔符


@dataclass
class ChunkConfig:
    """分块配置"""
    # 基础参数
    mode: ChunkMode = ChunkMode.GENERAL
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # 分隔符配置
    delimiter_type: DelimiterType = DelimiterType.PARAGRAPH
    custom_delimiter: str = "\n\n"
    
    # 父子模式参数
    parent_chunk_size: int = 1000    # 父块大小
    child_chunk_size: int = 300      # 子块大小
    parent_overlap: int = 100        # 父块重叠
    child_overlap: int = 30          # 子块重叠
    
    # 语义感知参数
    enable_semantic_boundary: bool = True    # 启用语义边界检测
    semantic_threshold: float = 0.7          # 语义相似度阈值
    
    # 结构感知参数
    preserve_structure: bool = True          # 保持文档结构
    structure_markers: List[str] = None      # 结构标记
    
    # 预处理参数
    enable_preprocessing: bool = True        # 启用预处理
    remove_extra_whitespace: bool = True     # 移除多余空白
    normalize_unicode: bool = True           # Unicode标准化
    
    # 摘要生成
    enable_auto_summary: bool = False        # 自动生成摘要
    summary_max_length: int = 100           # 摘要最大长度
    
    def __post_init__(self):
        if self.structure_markers is None:
            self.structure_markers = ["#", "##", "###", "1.", "2.", "3.", "一、", "二、", "三、"]


@dataclass
class AdvancedChunk:
    """高级文档块"""
    id: str
    text: str
    document_id: str
    document_name: str
    chunk_index: int
    
    # 层次信息
    chunk_type: str = "general"      # general, parent, child
    parent_id: Optional[str] = None  # 父块ID
    child_ids: List[str] = None      # 子块ID列表
    
    # 结构信息
    structure_level: int = 0         # 结构层级
    structure_path: str = ""         # 结构路径
    
    # 语义信息
    semantic_score: float = 0.0      # 语义完整性分数
    keywords: List[str] = None       # 关键词
    
    # 摘要信息
    summary: str = ""                # 自动生成的摘要
    
    # 元数据
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.child_ids is None:
            self.child_ids = []
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}


class AdvancedChunker:
    """高级文档分块器"""
    
    def __init__(self, config: ChunkConfig = None):
        """
        初始化高级分块器
        
        Args:
            config: 分块配置
        """
        self.config = config or ChunkConfig()
        
        # 预编译正则表达式
        self._compile_patterns()
        
        logger.info(f"高级分块器初始化完成，模式: {self.config.mode.value}")
    
    def _compile_patterns(self):
        """预编译正则表达式模式"""
        # 段落分隔符
        self.paragraph_pattern = re.compile(r'\n\s*\n')
        
        # 句子分隔符 (中英文)
        self.sentence_pattern = re.compile(r'[。！？.!?]+\s*')
        
        # 行分隔符
        self.line_pattern = re.compile(r'\n')
        
        # 结构标记模式
        structure_markers = '|'.join(re.escape(marker) for marker in self.config.structure_markers)
        self.structure_pattern = re.compile(f'^({structure_markers})', re.MULTILINE)
        
        # 空白字符模式
        self.whitespace_pattern = re.compile(r'\s+')
        
        # 标题模式 (Markdown)
        self.title_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def chunk_text(self, text: str, document_id: str, document_name: str, 
                   metadata: Dict[str, Any] = None) -> List[AdvancedChunk]:
        """
        分块文本
        
        Args:
            text: 输入文本
            document_id: 文档ID
            document_name: 文档名称
            metadata: 元数据
            
        Returns:
            分块结果列表
        """
        if not text or not text.strip():
            return []
        
        logger.info(f"开始分块文档: {document_name}, 模式: {self.config.mode.value}")
        
        # 预处理文本
        if self.config.enable_preprocessing:
            text = self._preprocess_text(text)
        
        # 根据模式选择分块策略
        if self.config.mode == ChunkMode.GENERAL:
            chunks = self._general_chunking(text, document_id, document_name, metadata)
        elif self.config.mode == ChunkMode.PARENT_CHILD:
            chunks = self._parent_child_chunking(text, document_id, document_name, metadata)
        elif self.config.mode == ChunkMode.SEMANTIC:
            chunks = self._semantic_chunking(text, document_id, document_name, metadata)
        elif self.config.mode == ChunkMode.STRUCTURE:
            chunks = self._structure_chunking(text, document_id, document_name, metadata)
        else:
            chunks = self._general_chunking(text, document_id, document_name, metadata)
        
        # 后处理
        chunks = self._post_process_chunks(chunks)
        
        logger.info(f"分块完成，生成 {len(chunks)} 个块")
        return chunks
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # Unicode标准化
        if self.config.normalize_unicode:
            import unicodedata
            text = unicodedata.normalize('NFKC', text)
        
        # 移除多余空白
        if self.config.remove_extra_whitespace:
            # 保留段落分隔，但清理其他多余空白
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                cleaned_line = self.whitespace_pattern.sub(' ', line.strip())
                cleaned_lines.append(cleaned_line)
            text = '\n'.join(cleaned_lines)
        
        return text
    
    def _general_chunking(self, text: str, document_id: str, document_name: str, 
                         metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """通用分块模式"""
        chunks = []
        
        # 根据分隔符类型分割文本
        segments = self._split_by_delimiter(text)
        
        # 合并段落到指定大小
        current_chunk = ""
        chunk_index = 0
        
        for segment in segments:
            # 检查是否需要开始新块
            if len(current_chunk) + len(segment) > self.config.chunk_size and current_chunk:
                # 创建当前块
                chunk = self._create_chunk(
                    current_chunk, document_id, document_name, chunk_index, 
                    "general", metadata
                )
                chunks.append(chunk)
                
                # 处理重叠
                if self.config.chunk_overlap > 0:
                    overlap_text = current_chunk[-self.config.chunk_overlap:]
                    current_chunk = overlap_text + segment
                else:
                    current_chunk = segment
                
                chunk_index += 1
            else:
                current_chunk += segment
        
        # 处理最后一个块
        if current_chunk.strip():
            chunk = self._create_chunk(
                current_chunk, document_id, document_name, chunk_index,
                "general", metadata
            )
            chunks.append(chunk)
        
        return chunks
    
    def _parent_child_chunking(self, text: str, document_id: str, document_name: str,
                              metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """父子分块模式 - 参考Dify的Parent-Child策略"""
        chunks = []
        
        # 1. 首先创建父块
        parent_chunks = self._create_parent_chunks(text, document_id, document_name, metadata)
        
        # 2. 为每个父块创建子块
        for parent_chunk in parent_chunks:
            # 添加父块
            chunks.append(parent_chunk)
            
            # 创建子块
            child_chunks = self._create_child_chunks(parent_chunk, document_id, document_name, metadata)
            
            # 更新父块的子块ID列表
            parent_chunk.child_ids = [child.id for child in child_chunks]
            
            # 添加子块
            chunks.extend(child_chunks)
        
        return chunks
    
    def _create_parent_chunks(self, text: str, document_id: str, document_name: str,
                             metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """创建父块"""
        parent_chunks = []
        segments = self._split_by_delimiter(text)
        
        current_chunk = ""
        chunk_index = 0
        
        for segment in segments:
            if len(current_chunk) + len(segment) > self.config.parent_chunk_size and current_chunk:
                # 创建父块
                chunk = self._create_chunk(
                    current_chunk, document_id, document_name, chunk_index,
                    "parent", metadata
                )
                parent_chunks.append(chunk)
                
                # 处理重叠
                if self.config.parent_overlap > 0:
                    overlap_text = current_chunk[-self.config.parent_overlap:]
                    current_chunk = overlap_text + segment
                else:
                    current_chunk = segment
                
                chunk_index += 1
            else:
                current_chunk += segment
        
        # 最后一个父块
        if current_chunk.strip():
            chunk = self._create_chunk(
                current_chunk, document_id, document_name, chunk_index,
                "parent", metadata
            )
            parent_chunks.append(chunk)
        
        return parent_chunks
    
    def _create_child_chunks(self, parent_chunk: AdvancedChunk, document_id: str, 
                            document_name: str, metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """为父块创建子块"""
        child_chunks = []
        
        # 使用更细粒度的分割创建子块
        segments = self._split_by_delimiter(parent_chunk.text, fine_grained=True)
        
        current_chunk = ""
        child_index = 0
        
        for segment in segments:
            if len(current_chunk) + len(segment) > self.config.child_chunk_size and current_chunk:
                # 创建子块
                child_id = f"{parent_chunk.id}_child_{child_index}"
                chunk = AdvancedChunk(
                    id=child_id,
                    text=current_chunk.strip(),
                    document_id=document_id,
                    document_name=document_name,
                    chunk_index=child_index,
                    chunk_type="child",
                    parent_id=parent_chunk.id,
                    metadata=metadata or {}
                )
                
                # 提取关键词
                chunk.keywords = self._extract_keywords(chunk.text)
                
                child_chunks.append(chunk)
                
                # 处理重叠
                if self.config.child_overlap > 0:
                    overlap_text = current_chunk[-self.config.child_overlap:]
                    current_chunk = overlap_text + segment
                else:
                    current_chunk = segment
                
                child_index += 1
            else:
                current_chunk += segment
        
        # 最后一个子块
        if current_chunk.strip():
            child_id = f"{parent_chunk.id}_child_{child_index}"
            chunk = AdvancedChunk(
                id=child_id,
                text=current_chunk.strip(),
                document_id=document_id,
                document_name=document_name,
                chunk_index=child_index,
                chunk_type="child",
                parent_id=parent_chunk.id,
                metadata=metadata or {}
            )
            chunk.keywords = self._extract_keywords(chunk.text)
            child_chunks.append(chunk)
        
        return child_chunks
    
    def _semantic_chunking(self, text: str, document_id: str, document_name: str,
                          metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """语义感知分块"""
        # 简化实现：基于句子语义边界分块
        chunks = []
        sentences = self.sentence_pattern.split(text)
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 检查语义边界
            if len(current_chunk) + len(sentence) > self.config.chunk_size and current_chunk:
                # 创建块
                chunk = self._create_chunk(
                    current_chunk, document_id, document_name, chunk_index,
                    "semantic", metadata
                )
                chunks.append(chunk)
                
                current_chunk = sentence
                chunk_index += 1
            else:
                current_chunk += sentence + "。"
        
        # 最后一个块
        if current_chunk.strip():
            chunk = self._create_chunk(
                current_chunk, document_id, document_name, chunk_index,
                "semantic", metadata
            )
            chunks.append(chunk)
        
        return chunks
    
    def _structure_chunking(self, text: str, document_id: str, document_name: str,
                           metadata: Dict[str, Any]) -> List[AdvancedChunk]:
        """结构感知分块"""
        chunks = []
        
        # 检测结构标记
        structure_matches = list(self.structure_pattern.finditer(text))
        
        if not structure_matches:
            # 没有结构标记，回退到通用模式
            return self._general_chunking(text, document_id, document_name, metadata)
        
        # 按结构分割
        sections = []
        start = 0
        
        for match in structure_matches:
            if start < match.start():
                sections.append((text[start:match.start()], 0, ""))
            
            # 找到下一个同级或更高级标记
            next_start = len(text)
            current_level = len(match.group(1))
            
            for next_match in structure_matches[structure_matches.index(match) + 1:]:
                next_level = len(next_match.group(1))
                if next_level <= current_level:
                    next_start = next_match.start()
                    break
            
            section_text = text[match.start():next_start]
            sections.append((section_text, current_level, match.group(1)))
            start = next_start
        
        # 创建结构化块
        chunk_index = 0
        for section_text, level, marker in sections:
            if section_text.strip():
                chunk = self._create_chunk(
                    section_text, document_id, document_name, chunk_index,
                    "structure", metadata
                )
                chunk.structure_level = level
                chunk.structure_path = marker
                chunks.append(chunk)
                chunk_index += 1
        
        return chunks
    
    def _split_by_delimiter(self, text: str, fine_grained: bool = False) -> List[str]:
        """根据分隔符类型分割文本"""
        if fine_grained:
            # 细粒度分割（用于子块）
            if self.config.delimiter_type == DelimiterType.SENTENCE:
                segments = self.sentence_pattern.split(text)
            else:
                segments = self.line_pattern.split(text)
        else:
            # 常规分割
            if self.config.delimiter_type == DelimiterType.PARAGRAPH:
                segments = self.paragraph_pattern.split(text)
            elif self.config.delimiter_type == DelimiterType.SENTENCE:
                segments = self.sentence_pattern.split(text)
            elif self.config.delimiter_type == DelimiterType.LINE:
                segments = self.line_pattern.split(text)
            elif self.config.delimiter_type == DelimiterType.CUSTOM:
                segments = text.split(self.config.custom_delimiter)
            else:
                segments = [text]
        
        # 过滤空段落并添加分隔符
        result = []
        for segment in segments:
            segment = segment.strip()
            if segment:
                if not fine_grained and self.config.delimiter_type == DelimiterType.PARAGRAPH:
                    result.append(segment + "\n\n")
                elif not fine_grained and self.config.delimiter_type == DelimiterType.SENTENCE:
                    result.append(segment + "。")
                else:
                    result.append(segment + "\n")
        
        return result
    
    def _create_chunk(self, text: str, document_id: str, document_name: str,
                     chunk_index: int, chunk_type: str, metadata: Dict[str, Any]) -> AdvancedChunk:
        """创建文档块"""
        chunk_id = f"{document_id}_chunk_{chunk_index}"
        
        chunk = AdvancedChunk(
            id=chunk_id,
            text=text.strip(),
            document_id=document_id,
            document_name=document_name,
            chunk_index=chunk_index,
            chunk_type=chunk_type,
            metadata=metadata or {}
        )
        
        # 提取关键词
        chunk.keywords = self._extract_keywords(text)
        
        # 生成摘要（如果启用）
        if self.config.enable_auto_summary:
            chunk.summary = self._generate_summary(text)
        
        return chunk
    
    def _extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """提取关键词"""
        try:
            # 使用jieba提取关键词
            keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=False)
            return keywords
        except Exception as e:
            logger.warning(f"关键词提取失败: {e}")
            return []
    
    def _generate_summary(self, text: str) -> str:
        """生成摘要（简化实现）"""
        try:
            # 简单的摘要生成：取前N个字符
            if len(text) <= self.config.summary_max_length:
                return text
            
            # 尝试在句子边界截断
            summary = text[:self.config.summary_max_length]
            last_period = summary.rfind('。')
            if last_period > self.config.summary_max_length // 2:
                summary = summary[:last_period + 1]
            else:
                summary = summary + "..."
            
            return summary
        except Exception as e:
            logger.warning(f"摘要生成失败: {e}")
            return text[:50] + "..." if len(text) > 50 else text
    
    def _post_process_chunks(self, chunks: List[AdvancedChunk]) -> List[AdvancedChunk]:
        """后处理块"""
        # 计算语义完整性分数（简化实现）
        for chunk in chunks:
            chunk.semantic_score = self._calculate_semantic_score(chunk.text)
        
        return chunks
    
    def _calculate_semantic_score(self, text: str) -> float:
        """计算语义完整性分数"""
        try:
            # 简化实现：基于句子完整性
            sentences = self.sentence_pattern.split(text)
            complete_sentences = sum(1 for s in sentences if s.strip().endswith(('。', '！', '？', '.', '!', '?')))
            total_sentences = len([s for s in sentences if s.strip()])
            
            if total_sentences == 0:
                return 0.0
            
            return complete_sentences / total_sentences
        except Exception:
            return 0.5  # 默认分数


# 便捷函数
def create_advanced_chunker(mode: str = "general", **kwargs) -> AdvancedChunker:
    """
    创建高级分块器的便捷函数
    
    Args:
        mode: 分块模式 (general, parent_child, semantic, structure)
        **kwargs: 其他配置参数
        
    Returns:
        配置好的高级分块器
    """
    chunk_mode = ChunkMode(mode)
    config = ChunkConfig(mode=chunk_mode, **kwargs)
    return AdvancedChunker(config)


if __name__ == "__main__":
    # 测试高级分块器
    print("高级文档分块器模块加载完成")
    print("支持的分块模式:")
    print("- general: 通用单层分块")
    print("- parent_child: 父子层次分块")
    print("- semantic: 语义感知分块")
    print("- structure: 结构感知分块")
    
    # 简单测试
    test_text = """
    # 蓝源基本法
    
    ## 1. 激情创业
    雷厉风行，家国情怀，为梦奋斗。
    
    ## 2. 拼搏执行
    全力以赴，尽职尽责，自动自发。
    
    ## 3. 忠诚专业
    敬业为魂，专业为本，永不放弃。
    """
    
    chunker = create_advanced_chunker("parent_child", chunk_size=100, parent_chunk_size=200)
    chunks = chunker.chunk_text(test_text, "test_doc", "测试文档")
    
    print(f"\n测试结果: 生成了 {len(chunks)} 个块")
    for chunk in chunks:
        print(f"- {chunk.chunk_type}: {chunk.text[:50]}...")