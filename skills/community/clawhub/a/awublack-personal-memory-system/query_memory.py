"""
自然语言查询记忆数据库的智能脚本

此脚本接收一个自然语言问题，将其转换为 SQL 查询，
从 memory.db 数据库中检索相关信息，并生成一个自然语言回答。

依赖：
- SQLite3
- re (正则表达式)
- os (文件路径)
"""

import sqlite3
import re
import os

def query_memory(question):
    """
    根据自然语言问题查询记忆数据库
    
    Args:
        question (str): 用户的自然语言问题
        
    Returns:
        str: 一个自然语言的回答，包含检索到的相关记忆
    """
    
    # 数据库路径
    DB_PATH = "/home/awu/.openclaw/workspace-work/memory.db"
    
    # 如果数据库不存在，返回错误
    if not os.path.exists(DB_PATH):
        return "抱歉，我的记忆数据库暂时不可用。请确保 MEMORY.md 文件存在并已同步。"
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 定义关键词和对应的 SQL 模式
    # 这是一个简单的规则引擎，可以进一步用 AI 模型增强
    keywords = [
        ("模型", "模型"),
        ("AI", "AI"),
        ("记忆", "记忆"),
        ("Obsidian", "Obsidian"),
        ("工作习惯", "工作习惯"),
        ("Git", "Git"),
        ("同步", "同步"),
        ("系统", "系统"),
        ("可靠性", "可靠性"),
        ("数字大脑", "数字大脑"),
        ("思考", "思考"),
        ("看法", "看法"),
        ("观点", "观点"),
        ("经验", "经验"),
        ("决策", "决策"),
    ]
    
    # 初始化查询条件
    search_terms = []
    
    # 为每个关键词检查问题中是否包含
    for keyword, db_search_term in keywords:
        if keyword.lower() in question.lower():
            search_terms.append(db_search_term)
    
    # 如果没有找到关键词，使用问题的前几个词作为通用搜索
    if not search_terms:
        # 提取问题的前3个词
        words = re.findall(r'[\w\u4e00-\u9fff]+', question)
        if words:
            search_terms = [words[0]]
    
    # 构建 SQL 查询
    if search_terms:
        # 使用 OR 连接所有搜索词
        conditions = " OR ".join(["content LIKE ?" for _ in search_terms])
        query = f"SELECT title, content FROM memories WHERE {conditions} ORDER BY created_at DESC LIMIT 5"
        
        # 执行查询
        cursor.execute(query, [f"%{term}%" for term in search_terms])
        results = cursor.fetchall()
    else:
        # 通用查询，返回最近的5条记录
        query = "SELECT title, content FROM memories ORDER BY created_at DESC LIMIT 5"
        cursor.execute(query)
        results = cursor.fetchall()
    
    # 关闭数据库连接
    conn.close()
    
    # 如果没有找到结果
    if not results:
        return "抱歉，我在我的记忆中找不到与你问题相关的信息。"
    
    # 生成自然语言回答
    answer = "根据我的记忆，以下是相关的信息：\n\n"
    for title, content in results:
        answer += f"### {title}\n{content}\n\n"
    
    answer += "\n这些信息来自你的长期记忆库。"
    return answer

# 如果直接运行此脚本，用于测试
if __name__ == "__main__":
    test_question = "我过去对 AI 模型的看法？"
    result = query_memory(test_question)
    print(result)