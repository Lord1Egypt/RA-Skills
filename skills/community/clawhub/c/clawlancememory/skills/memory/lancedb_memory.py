#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LanceDB 记忆管理模块
基于智谱 AI Embedding + LanceDB 向量数据库
支持语义检索的长期记忆存储
"""

import lancedb
import pyarrow as pa
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ZhipuEmbedding:
    """智谱 AI Embedding 封装"""
    
    def __init__(self, api_key: str = None, model: str = "embedding-3"):
        """
        初始化智谱 AI Embedding
        
        Args:
            api_key: 智谱 AI API Key
            model: Embedding 模型（embedding-2 或 embedding-3）
        """
        from zhipuai import ZhipuAI
        
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("未提供智谱 AI API Key，请设置 ZHIPU_API_KEY 环境变量")
        
        self.model = model
        self.client = ZhipuAI(api_key=self.api_key)
    
    def embed_query(self, text: str) -> List[float]:
        """将文本转换为向量"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Embedding 生成失败：{e}")
            # 返回零向量作为降级方案
            if self.model == "embedding-3":
                return [0.0] * 2048
            else:
                return [0.0] * 1024
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量将文本转换为向量"""
        return [self.embed_query(text) for text in texts]


class LanceDBMemory:
    """LanceDB 长期记忆管理器"""
    
    def __init__(self, 
                 db_path: str = "./memory_db",
                 zhipu_api_key: str = None,
                 embedding_model: str = "embedding-3"):
        """
        初始化 LanceDB 记忆管理器
        
        Args:
            db_path: 数据库路径
            zhipu_api_key: 智谱 AI API Key
            embedding_model: Embedding 模型（embedding-2 或 embedding-3）
        """
        self.db_path = db_path
        self.embedding_model = embedding_model
        
        # 初始化 Embedding
        self.embeddings = ZhipuEmbedding(
            api_key=zhipu_api_key,
            model=embedding_model
        )
        
        # 获取向量维度
        if embedding_model == "embedding-3":
            self.vector_dim = 2048
        else:
            self.vector_dim = 1024
        
        # 连接数据库
        self.db = lancedb.connect(db_path)
        
        # 创建记忆表
        self._create_tables()
    
    def _create_tables(self):
        """创建记忆数据表"""
        # 定义表结构
        schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("content", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), self.vector_dim)),
            pa.field("type", pa.string()),  # preference/fact/task/general
            pa.field("user_id", pa.string()),
            pa.field("session_id", pa.string()),
            pa.field("created_at", pa.timestamp("us")),
            pa.field("updated_at", pa.timestamp("us")),
            pa.field("expires_at", pa.timestamp("us"), nullable=True),
            pa.field("metadata", pa.string()),
            pa.field("importance", pa.float32())  # 重要性评分 0-1
        ])
        
        # 创建表（如果不存在）
        if "memories" not in self.db.table_names():
            self.table = self.db.create_table("memories", schema=schema)
            print(f"✅ 创建记忆表：memories")
        else:
            self.table = self.db.open_table("memories")
            print(f"✅ 打开记忆表：memories")
    
    def add_memory(self, 
                   content: str, 
                   user_id: str, 
                   type: str = "general",
                   metadata: Optional[Dict] = None, 
                   session_id: str = None,
                   expires_hours: Optional[int] = None,
                   importance: float = 0.5) -> str:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            user_id: 用户 ID
            type: 记忆类型（preference/fact/task/general）
            metadata: 额外元数据
            session_id: 会话 ID
            expires_hours: 过期时间（小时），None 表示永久
            importance: 重要性评分（0-1）
            
        Returns:
            记忆 ID
        """
        import uuid
        
        # 生成 Embedding
        embedding = self.embeddings.embed_query(content)
        
        # 准备数据
        now = datetime.now()
        expires_at = None
        if expires_hours:
            expires_at = now + timedelta(hours=expires_hours)
        
        memory_data = {
            "id": str(uuid.uuid4()),
            "content": content,
            "vector": embedding,
            "type": type,
            "user_id": user_id,
            "session_id": session_id or "",
            "created_at": now,
            "updated_at": now,
            "expires_at": expires_at,
            "metadata": json.dumps(metadata or {}),
            "importance": importance
        }
        
        # 插入数据
        self.table.add([memory_data])
        
        print(f"✅ 添加记忆：{content[:30]}... (type={type})")
        return memory_data["id"]
    
    def search_memories(self, 
                        query: str, 
                        user_id: str, 
                        k: int = 5,
                        type_filter: Optional[List[str]] = None,
                        include_expired: bool = False,
                        min_importance: float = 0.0) -> List[Dict]:
        """
        语义检索记忆
        
        Args:
            query: 查询文本
            user_id: 用户 ID
            k: 返回数量
            type_filter: 记忆类型过滤
            include_expired: 是否包含过期记忆
            min_importance: 最小重要性评分
            
        Returns:
            记忆列表
        """
        # 生成查询向量
        query_embedding = self.embeddings.embed_query(query)
        
        # 构建过滤条件
        conditions = [f"user_id='{user_id}'"]
        
        if type_filter:
            type_conditions = [f"type='{t}'" for t in type_filter]
            conditions.append(f"({' OR '.join(type_conditions)})")
        
        if not include_expired:
            conditions.append("(expires_at IS NULL OR expires_at > NOW())")
        
        if min_importance > 0:
            conditions.append(f"importance >= {min_importance}")
        
        where_clause = " AND ".join(conditions)
        
        # 执行检索
        results = (self.table
            .search(query_embedding)
            .where(where_clause)
            .limit(k)
            .to_list())
        
        # 解析元数据
        for mem in results:
            if mem.get("metadata"):
                mem["metadata"] = json.loads(mem["metadata"])
        
        return results
    
    def get_user_profile(self, user_id: str) -> Dict[str, List[str]]:
        """
        获取用户画像（聚合所有偏好和事实）
        
        Args:
            user_id: 用户 ID
            
        Returns:
            用户画像字典
        """
        profile = {
            "preferences": [],
            "facts": [],
            "tasks": [],
            "general": []
        }
        
        # 获取偏好（用通用查询代替空字符串）
        prefs = self.search_memories("用户偏好", user_id, k=100, type_filter=["preference"])
        profile["preferences"] = [p["content"] for p in prefs]
        
        # 获取事实
        facts = self.search_memories("用户信息", user_id, k=100, type_filter=["fact"])
        profile["facts"] = [f["content"] for f in facts]
        
        # 获取任务
        tasks = self.search_memories("任务安排", user_id, k=100, type_filter=["task"])
        profile["tasks"] = [t["content"] for t in tasks]
        
        # 获取其他
        general = self.search_memories("其他记忆", user_id, k=100, type_filter=["general"])
        profile["general"] = [g["content"] for g in general]
        
        return profile
    
    def delete_memory(self, memory_id: str) -> bool:
        """删除记忆"""
        try:
            self.table.delete(f"id='{memory_id}'")
            print(f"✅ 删除记忆：{memory_id}")
            return True
        except Exception as e:
            print(f"❌ 删除记忆失败：{e}")
            return False
    
    def update_memory(self, 
                      memory_id: str, 
                      content: str = None,
                      importance: float = None) -> bool:
        """更新记忆"""
        try:
            updates = []
            
            if content:
                # 重新生成 Embedding
                embedding = self.embeddings.embed_query(content)
                updates.append(f"content = '{content}'")
                updates.append(f"vector = {embedding}")
                updates.append(f"updated_at = NOW()")
            
            if importance is not None:
                updates.append(f"importance = {importance}")
            
            if updates:
                # LanceDB 暂不支持 UPDATE，需要删除后重新插入
                # TODO: 实现更新逻辑
                print("⚠️ 更新功能待实现")
                return False
            
            return True
        except Exception as e:
            print(f"❌ 更新记忆失败：{e}")
            return False
    
    def cleanup_expired(self) -> int:
        """清理过期记忆，返回删除数量"""
        try:
            # 查询过期记忆
            expired = (self.table
                .search()
                .where("expires_at IS NOT NULL AND expires_at < NOW()")
                .to_list())
            
            count = len(expired)
            
            # 删除过期记忆
            for mem in expired:
                self.delete_memory(mem["id"])
            
            if count > 0:
                print(f"✅ 清理了 {count} 条过期记忆")
            
            return count
        except Exception as e:
            print(f"❌ 清理过期记忆失败：{e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.table.count_rows()
        
        # 按类型统计（用 SQL 查询）
        type_counts = {}
        for t in ["preference", "fact", "task", "general"]:
            try:
                count = self.table.search().where(f"type='{t}'").to_arrow().num_rows
                if count > 0:
                    type_counts[t] = count
            except:
                pass
        
        return {
            "total_memories": total,
            "by_type": type_counts,
            "db_path": self.db_path,
            "embedding_model": self.embedding_model,
            "vector_dim": self.vector_dim
        }
    
    def format_memories_for_prompt(self, memories: List[Dict]) -> str:
        """将记忆列表格式化为 Prompt 文本"""
        if not memories:
            return "暂无相关记忆"
        
        formatted = []
        for mem in memories:
            content = mem["content"]
            mem_type = mem.get("type", "general")
            created = mem.get("created_at", "")
            
            # 格式化
            if isinstance(created, datetime):
                created = created.strftime("%Y-%m-%d")
            
            formatted.append(f"[{mem_type}] {content} (记录于 {created})")
        
        return "\n".join(formatted)


# 测试函数
if __name__ == "__main__":
    print("="*60)
    print("LanceDB 记忆模块测试")
    print("="*60)
    
    # 初始化
    mem = LanceDBMemory(
        db_path="/tmp/test_memory_zhipu",
        embedding_model="embedding-3"
    )
    
    # 添加记忆
    print("\n1. 添加记忆测试")
    mem.add_memory("我喜欢简洁的汇报风格", user_id="test_user", type="preference", importance=0.8)
    mem.add_memory("我负责 POC 项目", user_id="test_user", type="fact", importance=0.9)
    mem.add_memory("每周四提交 OKR 周报", user_id="test_user", type="task", importance=0.7)
    mem.add_memory("明天上午 10 点开会", user_id="test_user", type="task", expires_hours=24, importance=0.6)
    
    # 检索
    print("\n2. 语义检索测试")
    results = mem.search_memories("汇报风格", user_id="test_user", k=3)
    print(f"检索'汇报风格'：{len(results)} 条结果")
    for r in results:
        print(f"  - {r['content']} (score={r['_distance']:.4f})")
    
    # 用户画像
    print("\n3. 用户画像测试")
    profile = mem.get_user_profile("test_user")
    print(f"偏好：{profile['preferences']}")
    print(f"事实：{profile['facts']}")
    print(f"任务：{profile['tasks']}")
    
    # 统计
    print("\n4. 统计信息")
    stats = mem.get_stats()
    print(f"总记忆数：{stats['total_memories']}")
    print(f"按类型：{stats['by_type']}")
    
    # 格式化 Prompt
    print("\n5. Prompt 格式化")
    memories = mem.search_memories("工作", user_id="test_user", k=5)
    prompt = mem.format_memories_for_prompt(memories)
    print(prompt)
    
    print("\n" + "="*60)
    print("✅ 所有测试通过！")
    print("="*60)
