"""
Knowledge Base - 知识库
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json
import os
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzy_process


@dataclass
class Document:
    """文档"""
    id: str
    question: str
    answer: str
    keywords: List[str] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}


class KnowledgeBase:
    """知识库"""
    
    def __init__(self, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.embedding_model_name = embedding_model
        self.documents: List[Document] = []
        self.embeddings: Optional[np.ndarray] = None
        self.embedding_model = None
        
        # 尝试加载语义模型
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer(embedding_model)
        except Exception:
            pass
    
    def add_document(self, question: str, answer: str,
                    doc_id: Optional[str] = None,
                    keywords: Optional[List[str]] = None) -> str:
        """添加文档"""
        if doc_id is None:
            doc_id = f"doc_{len(self.documents)}"
        
        doc = Document(
            id=doc_id,
            question=question,
            answer=answer,
            keywords=keywords or []
        )
        
        self.documents.append(doc)
        self._update_embeddings()
        
        return doc_id
    
    def add_documents(self, docs: List[Dict]):
        """批量添加文档"""
        for doc in docs:
            self.add_document(
                question=doc.get('question', ''),
                answer=doc.get('answer', ''),
                doc_id=doc.get('id'),
                keywords=doc.get('keywords')
            )
    
    def _update_embeddings(self):
        """更新文档向量"""
        if self.embedding_model is None:
            return
        
        texts = [f"{d.question} {d.answer}" for d in self.documents]
        if texts:
            self.embeddings = self.embedding_model.encode(texts)
    
    def query(self, question: str, top_k: int = 1,
             threshold: float = 0.6) -> Optional[str]:
        """
        查询知识库
        
        Args:
            question: 问题
            top_k: 返回最相关的k个结果
            threshold: 相似度阈值
        
        Returns:
            答案或None
        """
        if not self.documents:
            return None
        
        # 1. 精确匹配
        for doc in self.documents:
            if question.lower() in doc.question.lower() or \
               doc.question.lower() in question.lower():
                return doc.answer
        
        # 2. 语义相似度匹配
        if self.embedding_model and self.embeddings is not None:
            query_embedding = self.embedding_model.encode([question])
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            best_idx = np.argmax(similarities)
            
            if similarities[best_idx] >= threshold:
                return self.documents[best_idx].answer
        
        # 3. 模糊匹配
        questions = [d.question for d in self.documents]
        best_match, score = fuzzy_process.extractOne(question, questions)
        
        if score >= 70:
            for doc in self.documents:
                if doc.question == best_match:
                    return doc.answer
        
        return None
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索相关文档"""
        results = []
        
        for doc in self.documents:
            score = fuzz.ratio(query.lower(), doc.question.lower())
            results.append({
                'document': doc,
                'score': score / 100.0
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """获取指定文档"""
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        for i, doc in enumerate(self.documents):
            if doc.id == doc_id:
                del self.documents[i]
                self._update_embeddings()
                return True
        return False
    
    def save(self, path: str):
        """保存知识库"""
        data = {
            'documents': [
                {
                    'id': d.id,
                    'question': d.question,
                    'answer': d.answer,
                    'keywords': d.keywords,
                    'metadata': d.metadata
                }
                for d in self.documents
            ]
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"知识库已保存: {path}")
    
    def load(self, path: str):
        """加载知识库"""
        if not os.path.exists(path):
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.documents = [
            Document(
                id=d['id'],
                question=d['question'],
                answer=d['answer'],
                keywords=d.get('keywords', []),
                metadata=d.get('metadata', {})
            )
            for d in data['documents']
        ]
        
        self._update_embeddings()
        print(f"知识库已加载: {path}")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_documents': len(self.documents),
            'has_embeddings': self.embeddings is not None
        }


if __name__ == '__main__':
    kb = KnowledgeBase()
    
    # 添加示例文档
    kb.add_document(
        "营业时间是什么？",
        "我们的营业时间是周一至周五 9:00-18:00，周末休息。"
    )
    kb.add_document(
        "如何申请退款？",
        "请在订单页面点击'申请退款'按钮，填写退款原因后提交。"
    )
    
    # 测试查询
    print(kb.query("你们几点开门？"))
    print(kb.query("怎么退款？"))
