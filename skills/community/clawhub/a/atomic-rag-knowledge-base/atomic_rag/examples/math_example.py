"""
数学知识库构建示例

演示如何使用AtomicRAGBuilder构建数学知识库。
"""

import sys
sys.path.append('..')

from atomic_rag import AtomicRAGBuilder


def build_math_knowledge_base():
    """构建高等数学知识库"""
    
    # 初始化构建器（数学领域）
    builder = AtomicRAGBuilder(
        domain="math",
        embedding_model="text-embedding-ada-002"
    )
    
    # 处理PDF文件
    atoms = builder.process_pdf(
        file_path="高等数学.pdf",
        metadata={
            "title": "高等数学",
            "author": "同济大学数学系",
            "subject": "数学",
            "isbn": "978-7-04-058959-6"
        }
    )
    
    # 保存到JSON（用于检查和调试）
    builder.save_atoms_to_json(atoms, "math_atoms.json")
    
    # 存储到向量数据库
    builder.store_to_vector_db(
        atoms,
        collection_name="math_knowledge",
        db_type="chroma"
    )
    
    print(f"✅ 成功构建数学知识库，共 {len(atoms)} 个知识原子")
    return atoms


def query_math_knowledge_base():
    """查询数学知识库"""
    from atomic_rag import MultiRecallRAG
    
    # 初始化RAG引擎
    rag = MultiRecallRAG()
    
    # 提问
    questions = [
        "如何求解一元二次方程？",
        "导数的定义是什么？",
        "定积分和不定积分的区别？",
        "如何证明函数连续？"
    ]
    
    for q in questions:
        print(f"\n{'='*50}")
        print(f"问题: {q}")
        print(f"{'='*50}")
        
        result = rag.ask(q, return_sources=True)
        
        print(f"回答: {result['answer'][:500]}...")
        print(f"\n引用来源:")
        for source in result['sources'][:3]:
            print(f"  - {source['title']}")


if __name__ == "__main__":
    # 构建知识库
    build_math_knowledge_base()
    
    # 查询知识库
    # query_math_knowledge_base()
