#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Query Demo - 演示向量查询功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skill_indexer import AliyunEmbeddings
import chromadb
from langchain_chroma import Chroma

def query_similar_skills(query: str, top_k: int = 5):
    """查询与查询词最相似的技能"""
    
    chroma_dir = r"C:\Users\Xiabi\.openclaw\workspace\chroma_db"
    collection_name = "openclaw_skills"
    
    # 加载向量存储
    client = chromadb.PersistentClient(path=chroma_dir)
    embeddings = AliyunEmbeddings()
    
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    # 搜索
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    
    # 去重（按技能名）
    seen_skills = set()
    unique_results = []
    
    for doc, score in results:
        skill_name = doc.metadata.get("skill_name", "Unknown")
        if skill_name not in seen_skills:
            seen_skills.add(skill_name)
            unique_results.append({
                "skill_name": skill_name,
                "similarity": round(1 - score, 3),
                "filename": doc.metadata.get("filename", ""),
                "preview": doc.page_content[:200].replace('\n', ' ')
            })
    
    return unique_results


def get_skill_combinations():
    """获取技能组合（基于文件共现）"""
    skills_dir = Path(r"C:\Users\Xiabi\.openclaw\workspace\skills")
    
    # 统计哪些技能经常在同一目录或相关目录
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    
    # 简单的共现分析（基于目录结构）
    combinations = {}
    
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        
        # 查找相关的其他技能（基于文件名包含）
        related = []
        for other_dir in skill_dirs:
            if other_dir.name == skill_name:
                continue
            
            # 检查是否有相关文件交叉引用
            for md_file in skill_dir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                    
                    if other_dir.name.lower() in content:
                        related.append(other_dir.name)
                        break
                except:
                    pass
        
        if related:
            combinations[skill_name] = related[:5]  # 限制最多 5 个
    
    return combinations


if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("Skill Query Demo")
    print("=" * 60)
    
    # 测试查询
    test_queries = [
        "飞书文档生成",
        "TTS 语音",
        "记忆同步",
        "项目管理",
        "emoji 表情"
    ]
    
    results = {}
    
    for query in test_queries:
        print(f"\n查询：{query}")
        similar = query_similar_skills(query, top_k=3)
        
        results[query] = similar
        
        for i, skill in enumerate(similar, 1):
            print(f"  {i}. {skill['skill_name']} (相似度：{skill['similarity']})")
            print(f"     文件：{skill['filename']}")
    
    # 获取技能组合
    print("\n" + "=" * 60)
    print("技能组合分析:")
    print("=" * 60)
    
    combinations = get_skill_combinations()
    
    for skill, related in list(combinations.items())[:10]:
        print(f"\n{skill}:")
        for r in related:
            print(f"  + {r}")
    
    # 保存结果
    output_file = Path(r"C:\Users\Xiabi\.openclaw\workspace\skill_query_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "queries": results,
            "combinations": combinations
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到：{output_file}")
    print("\n" + "=" * 60)
