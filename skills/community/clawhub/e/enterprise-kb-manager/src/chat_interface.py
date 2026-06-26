#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话式接口 - 支持用户通过对话上传文档到向量数据库

功能:
- 检测用户上传意图
- 处理文件上传
- 提供友好的对话反馈
- 集成 GTE-Rerank-v2 检索
"""

import os
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from .config_loader import load_config
from .document_processor import DocumentProcessor
from .advanced_retriever import AdvancedRetriever, RetrievalConfig, RetrievalMode
from .chroma_client import ChromaVectorDB
from .embedder import Embedder
from .manager import KnowledgeBaseManager


class ChatInterface:
    """对话式知识库接口"""
    
    def __init__(self):
        """初始化对话接口"""
        self.config = load_config()
        
        # 初始化组件
        self.processor = DocumentProcessor(self.config)
        
        self.db = ChromaVectorDB(
            collection_name=self.config.collection_name
        )
        
        self.embedder = Embedder(
            model=self.config.embedding_model,
            api_key=self.config.embedding_api_key,
            provider=self.config.embedding_provider,
            base_url=self.config.embedding_base_url
        )
        
        # 创建高级检索器 - 使用 GTE-Rerank-v2
        retrieval_config = RetrievalConfig(
            mode=RetrievalMode.HYBRID,
            top_k=3,
            enable_rerank=True,
            rerank_model="gte-rerank-v2",
            vector_weight=0.7,
            keyword_weight=0.3,
            enable_diversity=True
        )
        
        self.retriever = AdvancedRetriever(self.db, self.embedder, retrieval_config)
        self.manager = KnowledgeBaseManager(self.db, self.config.documents_dir)
        
        # 上传意图关键词
        self.upload_keywords = [
            "upload to kb", "上传到知识库", "上传文档", "添加到知识库",
            "保存到知识库", "导入知识库", "upload document", "add to kb",
            "存储文档", "入库", "上传", "导入"
        ]
        
        # 查询意图关键词
        self.query_keywords = [
            "search kb", "搜索知识库", "查询", "搜索", "问", "查找",
            "kb search", "知识库搜索", "检索"
        ]
        
        # 管理意图关键词
        self.manage_keywords = [
            "list kb", "kb list", "文档列表", "知识库列表", "查看文档",
            "kb stats", "统计", "状态", "delete kb", "删除文档"
        ]
    
    def process_message(self, message: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        处理用户消息
        
        Args:
            message: 用户消息
            file_path: 附件文件路径（可选）
            
        Returns:
            处理结果字典
        """
        message_lower = message.lower()
        
        # 1. 检测上传意图
        if file_path and self._detect_upload_intent(message_lower):
            return self._handle_upload(file_path, message)
        
        # 2. 检测管理意图
        if self._detect_manage_intent(message_lower):
            return self._handle_management(message)
        
        # 3. 检测查询意图或默认查询
        if self._detect_query_intent(message_lower) or not file_path:
            return self._handle_query(message)
        
        # 4. 有文件但没有明确意图
        if file_path:
            return {
                "type": "clarification",
                "message": f"我看到你发送了文件 {Path(file_path).name}。你想要：\n"
                          f"1. 上传到知识库 - 请说 '上传到知识库'\n"
                          f"2. 查询相关内容 - 请直接提问",
                "success": False
            }
        
        # 5. 默认处理
        return {
            "type": "help",
            "message": "我可以帮你：\n"
                      "📚 上传文档：发送文件并说 '上传到知识库'\n"
                      "🔍 查询知识：直接提问\n"
                      "📋 管理文档：说 'list kb documents' 查看文档列表",
            "success": True
        }
    
    def _detect_upload_intent(self, message: str) -> bool:
        """检测上传意图"""
        return any(keyword in message for keyword in self.upload_keywords)
    
    def _detect_query_intent(self, message: str) -> bool:
        """检测查询意图"""
        return any(keyword in message for keyword in self.query_keywords)
    
    def _detect_manage_intent(self, message: str) -> bool:
        """检测管理意图"""
        return any(keyword in message for keyword in self.manage_keywords)
    
    def _handle_upload(self, file_path: str, message: str) -> Dict[str, Any]:
        """处理文档上传"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return {
                    "type": "error",
                    "message": f"❌ 文件不存在: {file_path}",
                    "success": False
                }
            
            # 提取文档名称（如果用户指定了）
            document_name = self._extract_document_name(message, file_path)
            
            # 处理文档
            result = self.processor.process_document(file_path, document_name)
            
            if result.success:
                return {
                    "type": "upload_success",
                    "message": f"✅ 文档上传成功！\n\n"
                              f"📄 文档名称: {result.document_name}\n"
                              f"🆔 文档ID: {result.document_id}\n"
                              f"📊 创建块数: {result.chunk_count}\n\n"
                              f"现在你可以向我提问相关内容了！",
                    "success": True,
                    "document_id": result.document_id,
                    "document_name": result.document_name,
                    "chunk_count": result.chunk_count
                }
            else:
                return {
                    "type": "upload_error",
                    "message": f"❌ 文档上传失败: {result.error}",
                    "success": False,
                    "error": result.error
                }
                
        except Exception as e:
            return {
                "type": "upload_error",
                "message": f"❌ 上传过程中出错: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def _handle_query(self, message: str) -> Dict[str, Any]:
        """处理知识查询"""
        try:
            # 检查知识库是否为空
            if self.db.count() == 0:
                return {
                    "type": "empty_kb",
                    "message": "📭 知识库为空，请先上传一些文档。\n\n"
                              "💡 使用方法：发送文件并说 '上传到知识库'",
                    "success": False
                }
            
            # 执行检索
            results = self.retriever.search(message, top_k=3)
            
            if not results:
                return {
                    "type": "no_results",
                    "message": f"🔍 未找到与 '{message}' 相关的内容。\n\n"
                              f"💡 建议：\n"
                              f"- 尝试使用不同的关键词\n"
                              f"- 检查是否有相关文档已上传\n"
                              f"- 使用更简单的表达方式",
                    "success": False
                }
            
            # 格式化结果
            response_parts = [f"🔍 关于 '{message}' 的搜索结果：\n"]
            
            for i, result in enumerate(results, 1):
                response_parts.append(f"📄 **结果 {i}** (相关度: {result.final_score:.3f})")
                response_parts.append(f"📂 来源: {result.document_name}")
                
                # 显示内容摘要
                content = result.text.strip()
                if len(content) > 300:
                    content = content[:300] + "..."
                response_parts.append(f"📝 内容: {content}")
                
                # 显示匹配关键词
                if result.matched_keywords:
                    keywords = ', '.join(result.matched_keywords[:5])
                    response_parts.append(f"🔑 匹配词: {keywords}")
                
                response_parts.append("")  # 空行分隔
            
            return {
                "type": "query_success",
                "message": "\n".join(response_parts),
                "success": True,
                "results": [
                    {
                        "text": r.text,
                        "score": r.final_score,
                        "document_name": r.document_name,
                        "matched_keywords": r.matched_keywords
                    }
                    for r in results
                ]
            }
            
        except Exception as e:
            return {
                "type": "query_error",
                "message": f"❌ 查询过程中出错: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def _handle_management(self, message: str) -> Dict[str, Any]:
        """处理管理命令"""
        message_lower = message.lower()
        
        try:
            # 列出文档
            if "list" in message_lower or "文档列表" in message_lower:
                documents = self.manager.list_documents()
                
                if not documents:
                    return {
                        "type": "empty_list",
                        "message": "📭 知识库中暂无文档",
                        "success": True
                    }
                
                response_parts = [f"📚 知识库文档列表 ({len(documents)} 个)：\n"]
                
                for i, doc in enumerate(documents, 1):
                    response_parts.append(f"{i}. 📄 {doc['document_name']}")
                    response_parts.append(f"   🆔 ID: {doc['document_id']}")
                    response_parts.append(f"   📊 块数: {doc['chunk_count']}")
                    response_parts.append("")
                
                return {
                    "type": "list_success",
                    "message": "\n".join(response_parts),
                    "success": True,
                    "documents": documents
                }
            
            # 显示统计信息
            elif "stats" in message_lower or "统计" in message_lower:
                stats = self.manager.get_statistics()
                
                response_parts = ["📊 知识库统计信息：\n"]
                response_parts.append(f"📄 文档数量: {stats.get('document_count', 0)}")
                response_parts.append(f"📦 文档块数: {stats.get('chunk_count', 0)}")
                response_parts.append(f"💾 存储大小: {stats.get('total_size_mb', 0)} MB")
                response_parts.append(f"📁 文件数量: {stats.get('stored_files', 0)}")
                
                return {
                    "type": "stats_success",
                    "message": "\n".join(response_parts),
                    "success": True,
                    "stats": stats
                }
            
            # 删除文档
            elif "delete" in message_lower or "删除" in message_lower:
                # 提取文档ID或名称
                doc_id = self._extract_document_id(message)
                if doc_id:
                    result = self.manager.delete_document(doc_id)
                    return {
                        "type": "delete_result",
                        "message": result["message"],
                        "success": result["success"]
                    }
                else:
                    return {
                        "type": "delete_help",
                        "message": "请指定要删除的文档ID，例如：'delete kb document doc_123456'",
                        "success": False
                    }
            
            else:
                return {
                    "type": "manage_help",
                    "message": "📋 管理命令：\n"
                              "- 'list kb documents' - 查看文档列表\n"
                              "- 'kb stats' - 显示统计信息\n"
                              "- 'delete kb document <ID>' - 删除文档",
                    "success": True
                }
                
        except Exception as e:
            return {
                "type": "manage_error",
                "message": f"❌ 管理操作出错: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def _extract_document_name(self, message: str, file_path: str) -> str:
        """从消息中提取文档名称"""
        # 尝试从消息中提取引号内的名称
        quoted_match = re.search(r'["\']([^"\']+)["\']', message)
        if quoted_match:
            return quoted_match.group(1)
        
        # 使用文件名
        return Path(file_path).name
    
    def _extract_document_id(self, message: str) -> Optional[str]:
        """从消息中提取文档ID"""
        # 查找 doc_ 开头的ID
        match = re.search(r'doc_[a-f0-9]{12}', message)
        return match.group(0) if match else None


# 便捷函数
def create_chat_interface() -> ChatInterface:
    """创建对话接口实例"""
    return ChatInterface()


def process_user_message(message: str, file_path: Optional[str] = None) -> str:
    """
    处理用户消息的便捷函数
    
    Args:
        message: 用户消息
        file_path: 附件文件路径
        
    Returns:
        格式化的回复消息
    """
    interface = create_chat_interface()
    result = interface.process_message(message, file_path)
    return result["message"]


if __name__ == "__main__":
    # 测试对话接口
    print("🤖 企业知识库对话接口测试")
    print("=" * 50)
    
    interface = ChatInterface()
    
    # 测试查询
    test_queries = [
        "蓝源的核心价值观是什么？",
        "list kb documents",
        "kb stats"
    ]
    
    for query in test_queries:
        print(f"\n用户: {query}")
        result = interface.process_message(query)
        print(f"助手: {result['message']}")