#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级文档处理器 (Advanced Document Processor)

支持Dify风格的高级分块和处理策略
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import hashlib
from datetime import datetime
import logging

from .parser import DocumentParser
from .advanced_chunker import AdvancedChunker, AdvancedChunk
from .embedder import Embedder
from .chroma_client import ChromaVectorDB

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class AdvancedProcessResult:
    """高级处理结果"""
    success: bool
    document_id: str
    document_name: str
    chunk_count: int
    chunks_info: Dict[str, Any]  # 块类型统计信息
    message: str
    error: str = ""


class AdvancedDocumentProcessor:
    """高级文档处理器"""
    
    def __init__(self, chunker: AdvancedChunker, embedder: Embedder, 
                 db: ChromaVectorDB, documents_dir: str = "./documents"):
        """
        初始化高级文档处理器
        
        Args:
            chunker: 高级分块器
            embedder: 嵌入生成器
            db: 向量数据库
            documents_dir: 文档存储目录
        """
        self.chunker = chunker
        self.embedder = embedder
        self.db = db
        self.documents_dir = documents_dir
        
        # 初始化文档解析器
        self.parser = DocumentParser()
        
        # 确保文档目录存在
        os.makedirs(documents_dir, exist_ok=True)
        
        logger.info("高级文档处理器初始化完成")
    
    def process_document(self, file_path: str, document_name: str = None, 
                        metadata: Dict[str, Any] = None) -> AdvancedProcessResult:
        """
        处理文档: 解析 → 高级分块 → 嵌入 → 存储
        
        Args:
            file_path: 文档文件路径
            document_name: 可选的自定义名称
            metadata: 额外的元数据
            
        Returns:
            AdvancedProcessResult 处理结果
        """
        try:
            # 验证文件
            if not os.path.exists(file_path):
                return AdvancedProcessResult(
                    success=False,
                    document_id="",
                    document_name=document_name or "",
                    chunk_count=0,
                    chunks_info={},
                    message="",
                    error=f"文件不存在: {file_path}"
                )
            
            if not self.parser.is_supported(file_path):
                ext = Path(file_path).suffix
                return AdvancedProcessResult(
                    success=False,
                    document_id="",
                    document_name=document_name or "",
                    chunk_count=0,
                    chunks_info={},
                    message="",
                    error=f"不支持的文件格式: {ext}. 支持的格式: {', '.join(DocumentParser.SUPPORTED_FORMATS)}"
                )
            
            # 生成文档ID
            if document_name is None:
                document_name = Path(file_path).stem
            
            document_id = self._generate_document_id(document_name)
            
            logger.info(f"开始处理文档: {document_name} (ID: {document_id})")
            
            # 检查文档是否已存在
            existing_count = self.db.count_by_document(document_id)
            if existing_count > 0:
                # 删除现有块
                self.db.delete_by_document(document_id)
                logger.warning(f"替换了现有文档的 {existing_count} 个块")
            
            # 解析文档
            logger.info("解析文档内容...")
            text = self.parser.parse(file_path)
            
            if not text or not text.strip():
                return AdvancedProcessResult(
                    success=False,
                    document_id=document_id,
                    document_name=document_name,
                    chunk_count=0,
                    chunks_info={},
                    message="",
                    error="文档为空或无法提取文本内容"
                )
            
            logger.info(f"文档解析完成，文本长度: {len(text)} 字符")
            
            # 高级分块
            logger.info("执行高级分块...")
            
            # 合并元数据
            chunk_metadata = {
                "uploaded_at": datetime.now().isoformat(),
                "file_path": file_path,
                "file_size": os.path.getsize(file_path),
                **(metadata or {})
            }
            
            chunks = self.chunker.chunk_text(
                text=text,
                document_id=document_id,
                document_name=document_name,
                metadata=chunk_metadata
            )
            
            if not chunks:
                return AdvancedProcessResult(
                    success=False,
                    document_id=document_id,
                    document_name=document_name,
                    chunk_count=0,
                    chunks_info={},
                    message="",
                    error="分块失败，未生成任何块"
                )
            
            # 统计块信息
            chunks_info = self._analyze_chunks(chunks)
            logger.info(f"分块完成，生成 {len(chunks)} 个块: {chunks_info}")
            
            # 生成嵌入向量
            logger.info("生成嵌入向量...")
            storage_data = []
            
            for chunk in chunks:
                try:
                    # 生成嵌入向量
                    embedding = self.embedder.embed_query(chunk.text)
                    
                    # 准备存储数据
                    storage_item = {
                        "id": chunk.id,
                        "vector": embedding,
                        "text": chunk.text,
                        "document_id": chunk.document_id,
                        "document_name": chunk.document_name,
                        "chunk_index": chunk.chunk_index,
                        "metadata": {
                            "document_id": chunk.document_id,
                            "document_name": chunk.document_name,
                            "chunk_index": chunk.chunk_index,
                            "chunk_type": chunk.chunk_type,
                            "parent_id": chunk.parent_id,
                            "child_ids": ",".join(chunk.child_ids) if chunk.child_ids else "",
                            "structure_level": chunk.structure_level,
                            "structure_path": chunk.structure_path,
                            "semantic_score": chunk.semantic_score,
                            "keywords": ",".join(chunk.keywords) if chunk.keywords else "",
                            "summary": chunk.summary,
                            **chunk.metadata
                        }
                    }
                    
                    storage_data.append(storage_item)
                    
                except Exception as e:
                    logger.error(f"处理块 {chunk.id} 时出错: {e}")
                    continue
            
            if not storage_data:
                return AdvancedProcessResult(
                    success=False,
                    document_id=document_id,
                    document_name=document_name,
                    chunk_count=0,
                    chunks_info=chunks_info,
                    message="",
                    error="嵌入向量生成失败"
                )
            
            logger.info(f"嵌入向量生成完成，准备存储 {len(storage_data)} 个块")
            
            # 存储到向量数据库
            logger.info("存储到向量数据库...")
            inserted_count = self.db.add_chunks(storage_data)
            
            # 复制文件到文档目录
            try:
                dest_path = os.path.join(self.documents_dir, f"{document_id}_{document_name}")
                shutil.copy2(file_path, dest_path)
                logger.info(f"文档已复制到: {dest_path}")
            except Exception as e:
                logger.warning(f"复制文档文件失败: {e}")
            
            success_message = f"成功处理文档 {document_name}: 生成 {inserted_count} 个块"
            logger.info(success_message)
            
            return AdvancedProcessResult(
                success=True,
                document_id=document_id,
                document_name=document_name,
                chunk_count=inserted_count,
                chunks_info=chunks_info,
                message=success_message
            )
        
        except Exception as e:
            error_msg = f"文档处理失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            return AdvancedProcessResult(
                success=False,
                document_id=document_id if 'document_id' in locals() else "",
                document_name=document_name or "",
                chunk_count=0,
                chunks_info={},
                message="",
                error=error_msg
            )
    
    def _generate_document_id(self, document_name: str) -> str:
        """生成唯一的文档ID"""
        # 使用文档名 + 时间戳的哈希值确保唯一性
        content = f"{document_name}_{datetime.now().isoformat()}"
        hash_obj = hashlib.md5(content.encode())
        return f"doc_{hash_obj.hexdigest()[:12]}"
    
    def _analyze_chunks(self, chunks: List[AdvancedChunk]) -> Dict[str, Any]:
        """分析块的统计信息"""
        info = {
            "total_count": len(chunks),
            "parent_count": 0,
            "child_count": 0,
            "other_count": 0,
            "avg_chunk_size": 0,
            "total_text_length": 0,
            "chunk_types": {}
        }
        
        total_length = 0
        
        for chunk in chunks:
            chunk_type = chunk.chunk_type
            
            # 统计类型
            if chunk_type == "parent":
                info["parent_count"] += 1
            elif chunk_type == "child":
                info["child_count"] += 1
            else:
                info["other_count"] += 1
            
            # 统计各类型数量
            info["chunk_types"][chunk_type] = info["chunk_types"].get(chunk_type, 0) + 1
            
            # 统计文本长度
            text_length = len(chunk.text)
            total_length += text_length
        
        info["total_text_length"] = total_length
        info["avg_chunk_size"] = total_length / len(chunks) if chunks else 0
        
        return info
    
    def get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        """获取文档信息"""
        try:
            chunks = self.db.get_chunks_by_document(document_id)
            if not chunks:
                return None
            
            # 分析块信息
            chunk_objects = []
            for chunk_data in chunks:
                # 这里需要根据实际的数据结构来构建AdvancedChunk对象
                # 简化处理，只统计基本信息
                pass
            
            return {
                "document_id": document_id,
                "chunk_count": len(chunks),
                "created_at": chunks[0].get("metadata", {}).get("uploaded_at", ""),
            }
            
        except Exception as e:
            logger.error(f"获取文档信息失败: {e}")
            return None
    
    def delete_document(self, document_id: str) -> bool:
        """删除文档及其所有块"""
        try:
            deleted_count = self.db.delete_by_document(document_id)
            
            # 尝试删除文档文件
            try:
                for file_path in Path(self.documents_dir).glob(f"{document_id}_*"):
                    file_path.unlink()
                    logger.info(f"删除文档文件: {file_path}")
            except Exception as e:
                logger.warning(f"删除文档文件失败: {e}")
            
            logger.info(f"删除文档 {document_id}，共删除 {deleted_count} 个块")
            return deleted_count > 0
            
        except Exception as e:
            logger.error(f"删除文档失败: {e}")
            return False


if __name__ == "__main__":
    # 测试高级文档处理器
    print("高级文档处理器模块加载完成")
    print("支持Dify风格的父子分块和高级检索策略")