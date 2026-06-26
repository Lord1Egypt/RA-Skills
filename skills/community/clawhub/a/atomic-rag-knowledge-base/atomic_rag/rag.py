"""
RAG检索增强引擎

提供多路召回、重排序、上下文组装功能。
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class RetrievedAtom:
    """检索到的知识原子"""
    atom_id: str
    title: str
    content: str
    similarity: float
    metadata: Dict


class MultiRecallRAG:
    """
    多路召回RAG检索引擎
    
    功能：
    1. 向量检索
    2. 关键词检索
    3. 知识图谱检索
    4. 重排序
    5. 上下文组装
    """
    
    def __init__(self, vector_store=None, knowledge_graph=None):
        """
        初始化RAG引擎
        
        Args:
            vector_store: 向量数据库实例
            knowledge_graph: 知识图谱实例
        """
        self.vector_store = vector_store
        self.kg = knowledge_graph
    
    def ask(self, query: str, top_k: int = 5, return_sources: bool = True) -> Dict:
        """
        问答接口
        
        Args:
            query: 用户问题
            top_k: 返回结果数量
            return_sources: 是否返回引用来源
            
        Returns:
            Dict: 回答和引用
        """
        # 1. 多路召回
        results = self.retrieve(query, top_k * 2)
        
        # 2. 重排序
        reranked = self.rerank(query, results)[:top_k]
        
        # 3. 构建上下文
        context = self.build_context(reranked)
        
        # 4. 生成回答（这里调用LLM，实际使用时替换为具体调用）
        answer = self.generate_answer(query, context)
        
        # 5. 提取引用来源
        sources = []
        if return_sources:
            sources = [
                {
                    "atom_id": r.atom_id,
                    "title": r.title,
                    "snippet": r.content[:200]
                }
                for r in reranked
            ]
        
        return {
            "answer": answer,
            "sources": sources,
            "context_used": len(reranked)
        }
    
    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievedAtom]:
        """多路召回"""
        results = []
        
        # 1. 向量检索
        if self.vector_store:
            vector_results = self._vector_search(query, top_k)
            results.extend(vector_results)
        
        # 2. 关键词检索
        keyword_results = self._keyword_search(query, top_k)
        results.extend(keyword_results)
        
        # 3. 知识图谱检索
        if self.kg:
            kg_results = self._kg_search(query, top_k)
            results.extend(kg_results)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            if r.atom_id not in seen:
                seen.add(r.atom_id)
                unique_results.append(r)
        
        return unique_results
    
    def _vector_search(self, query: str, top_k: int) -> List[RetrievedAtom]:
        """向量检索"""
        try:
            docs = self.vector_store.similarity_search(query, k=top_k)
            
            results = []
            for doc in docs:
                results.append(RetrievedAtom(
                    atom_id=doc.metadata.get("atom_id", ""),
                    title=doc.metadata.get("title", ""),
                    content=doc.page_content,
                    similarity=0.9,  # 向量相似度需要从实际结果获取
                    metadata=doc.metadata
                ))
            
            return results
        except Exception as e:
            print(f"⚠️ 向量检索失败: {e}")
            return []
    
    def _keyword_search(self, query: str, top_k: int) -> List[RetrievedAtom]:
        """关键词检索"""
        # 实际实现需要基于倒排索引
        # 这里返回空列表，实际使用时需要实现
        return []
    
    def _kg_search(self, query: str, top_k: int) -> List[RetrievedAtom]:
        """知识图谱检索"""
        # 实际实现需要基于图数据库
        # 这里返回空列表，实际使用时需要实现
        return []
    
    def rerank(self, query: str, results: List[RetrievedAtom]) -> List[RetrievedAtom]:
        """
        重排序
        
        根据以下因素综合评分：
        1. 向量相似度
        2. 关键词匹配度
        3. 知识图谱关联度
        4. 使用频率
        5. 用户画像匹配度
        """
        if not results:
            return []
        
        # 简单实现：按相似度排序
        # 实际实现需要考虑更多因素
        reranked = sorted(results, key=lambda x: x.similarity, reverse=True)
        
        return reranked
    
    def build_context(self, atoms: List[RetrievedAtom]) -> str:
        """
        构建RAG上下文
        
        格式：
        ### 知识点1
        标题: xxx
        内容: xxx
        
        ### 知识点2
        标题: xxx
        内容: xxx
        """
        if not atoms:
            return ""
        
        context_parts = []
        
        for i, atom in enumerate(atoms, 1):
            part = f"""
### 知识点{i}: {atom.title}
{atom.content}

**关键要点**: {self._extract_key_points(atom.content)}

**方法步骤**: {self._extract_steps(atom.content)}
"""
            context_parts.append(part)
        
        context = "\n\n---\n\n".join(context_parts)
        
        return context
    
    def _extract_key_points(self, content: str) -> str:
        """提取关键要点"""
        # 简单实现：取前100字
        return content[:100] + "..." if len(content) > 100 else content
    
    def _extract_steps(self, content: str) -> str:
        """提取步骤"""
        # 简单实现：返回前2句
        sentences = content.split('。')
        steps = '。'.join(sentences[:2])
        return steps if steps else content[:100]
    
    def generate_answer(self, query: str, context: str) -> str:
        """
        生成回答
        
        实际实现需要调用LLM API
        这里返回模拟回答
        """
        prompt = f"""基于以下知识库内容回答用户问题。

知识库内容：
{context}

用户问题：{query}

请基于知识库给出准确、详细的回答，并说明引用了哪些知识点。"""
        
        # TODO: 实际实现需要调用LLM
        # from langchain.chat_models import ChatOpenAI
        # llm = ChatOpenAI()
        # return llm.invoke(prompt)
        
        # 模拟返回
        return f"""基于检索到的知识库内容，我可以从以下几个角度回答您的问题：

{context[:500]}...

（实际回答需要LLM生成）"""


class AdaptiveRAG(MultiRecallRAG):
    """
    自适应RAG
    
    根据问题类型自动选择最优的检索策略
    """
    
    def __init__(self, vector_store=None, knowledge_graph=None):
        super().__init__(vector_store, knowledge_graph)
    
    def classify_query(self, query: str) -> str:
        """
        问题分类
        
        类型：
        - factual: 事实性问题
        - conceptual: 概念性问题  
        - procedural: 过程性问题
        - problem_solving: 解决问题类
        """
        query_lower = query.lower()
        
        # 关键词匹配分类
        if any(kw in query_lower for kw in ['是什么', '什么是', '定义', '概念']):
            return "conceptual"
        
        if any(kw in query_lower for kw in ['如何', '怎么', '步骤', '方法', '过程']):
            return "procedural"
        
        if any(kw in query_lower for kw in ['解', '计算', '求', '证明', '推导']):
            return "problem_solving"
        
        return "factual"
    
    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievedAtom]:
        """根据问题类型自适应检索"""
        query_type = self.classify_query(query)
        
        results = super().retrieve(query, top_k)
        
        # 根据问题类型调整结果
        if query_type == "problem_solving":
            # 问题解决类：优先返回有步骤和方法的内容
            results = [r for r in results if '步骤' in r.content or '方法' in r.content]
        elif query_type == "conceptual":
            # 概念类：优先返回简洁定义
            results = results[:5]  # 取前5个最相关的
        
        return results[:top_k]
