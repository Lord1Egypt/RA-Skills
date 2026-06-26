import sys
import os
import time
import math
import json
import argparse

# 尝试导入 Chroma (如果环境支持)
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

# 配置路径
WORKSPACE_ROOT = os.path.expanduser(r"~/.openclaw/workspace")
CHROMA_PATH = os.path.join(WORKSPACE_ROOT, r"database\chroma_store")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_config():
    """加载配置"""
    import yaml
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

CONFIG = load_config()

# 增量总结缓冲区文件
BUFFER_FILE = os.path.join(WORKSPACE_ROOT, r"database\summary_buffer.json")

class FluidMemorySkill:
    def __init__(self):
        self.use_vector = HAS_CHROMA
        
        if self.use_vector:
            # 初始化 Chroma (持久化模式)
            try:
                # 适配 Chroma 0.4+ / 0.5+ API
                if hasattr(chromadb, 'PersistentClient'):
                    self.client = chromadb.PersistentClient(path=CHROMA_PATH)
                else:
                    self.client = chromadb.Client(Settings(
                        persist_directory=CHROMA_PATH,
                        anonymized_telemetry=False
                    ))
                
                self.collection = self.client.get_or_create_collection(name="fluid_memory")
            except Exception as e:
                print(f"[WARN] Chroma 初始化失败: {e}，降级为模拟模式。")
                self.use_vector = False
        
        # 如果没有向量库，回退到 SQLite (这里为了简化，如果降级直接报错提示用户)
        if not self.use_vector:
            print("[INFO] 正在运行在无向量模式 (关键词匹配)")

    def _calculate_score(self, similarity, created_at, access_count):
        """核心流体公式"""
        LAMBDA_DECAY = 0.05  # 遗忘速度
        ALPHA_BOOST = 0.2    # 强化力度
        
        days_passed = (time.time() - created_at) / 86400
        decay = math.exp(-LAMBDA_DECAY * days_passed)
        boost = ALPHA_BOOST * math.log(1 + access_count)
        
        # 相似度在 Chroma 里是距离 (0~2)，需要转换。
        # 假设用的是 cosine distance: score = 1 - distance
        # 这里 similarity 传入时已经是归一化的分数了
        return (similarity * decay) + boost

    def remember(self, content):
        """植入记忆"""
        mem_id = f"mem_{int(time.time()*1000)}"
        now = time.time()
        
        if self.use_vector:
            try:
                self.collection.add(
                    documents=[content],
                    metadatas=[{
                        "created_at": now,
                        "last_accessed": now,
                        "access_count": 0,
                        "status": "active"
                    }],
                    ids=[mem_id]
                )
                # 静默模式：成功不返回任何内容，避免 LLM 啰嗦
                return ""
            except Exception as e:
                return f"[ERROR] 向量植入失败: {e}"
        else:
            return "[ERROR] 缺少 Chroma 支持，无法植入向量记忆。"

    def recall(self, query):
        """唤起记忆 (Vector + Fluid Logic)"""
        if not self.use_vector:
            return "[ERROR] 缺少 Chroma 支持，无法进行语义检索。"

        # 🚀 自动学习模式：每次检索时自动记录对话
        if AUTO_LEARN:
            self.remember(f"[对话] {query}")

        try:
            # 1. 粗召回：让 Chroma 找最像的 Top 10 (活跃记忆)
            results = self.collection.query(
                query_texts=[query],
                n_results=10,
                where={"status": "active"} # 只找活跃的
            )
        except Exception as e:
            return f"[ERROR] 检索失败: {e}"

        if not results['ids'][0]:
            return "[EMPTY] 没有找到相关记忆。"

        scored_memories = []
        ids = results['ids'][0]
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0]

        for i in range(len(ids)):
            # 转换距离为相似度 (通用公式)
            dist = distances[i]
            sim = 1.0 / (1.0 + dist)
            
            meta = metas[i]
            created_at = meta.get('created_at', time.time())
            access_count = meta.get('access_count', 0)
            
            # 计算最终得分
            final_score = self._calculate_score(sim, created_at, access_count)

            if final_score > 0.05: # 降低阈值
                scored_memories.append({
                    "content": docs[i],
                    "score": round(final_score, 3),
                    "id": ids[i],
                    "meta": meta
                })

        # 3. 排序取 Top 3
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        top_memories = scored_memories[:3]

        # 4. 强化机制 (Boost): 更新 Metadata
        if top_memories:
            for mem in top_memories:
                new_count = mem['meta']['access_count'] + 1
                self.collection.update(
                    ids=[mem['id']],
                    metadatas=[{
                        "created_at": mem['meta']['created_at'],
                        "last_accessed": time.time(),
                        "access_count": new_count,
                        "status": "active"
                    }]
                )
            
            # 格式化输出供 OpenClaw 读取
            return json.dumps([{
                "text": m["content"], 
                "score": m["score"]
            } for m in top_memories], ensure_ascii=False)
        else:
            return "[EMPTY] 记忆存在但权重过低，已被大脑过滤。"

    def forget(self, keyword):
        """主动遗忘 (软删除/归档)"""
        # 这里的实现比较 trick，因为 Chroma 的 update 需要 id
        # 我们先 query 找到它，再 update metadata
        if not self.use_vector: return "[ERROR] No Vector DB"
        
        results = self.collection.query(
            query_texts=[keyword],
            n_results=1, # 假设用户只想删最匹配的那条
            where={"status": "active"}
        )
        
        if results['ids'][0]:
            target_id = results['ids'][0][0]
            target_text = results['documents'][0][0]
            current_meta = results['metadatas'][0][0]
            
            # 更新状态为 archive
            current_meta['status'] = 'archive'
            self.collection.update(
                ids=[target_id],
                metadatas=[current_meta]
            )
            return f"[ARCHIVED] 已归档记忆: '{target_text}'"
        else:
            return "[404] 未找到相关活跃记忆。"

    def status(self):
        if not self.use_vector: return "Mode: Keyword (No Chroma)"
        count = self.collection.count()
        # 同时检查 Buffer 状态
        summary, rounds = self._load_buffer()
        return json.dumps({
            "total_vectors": count, 
            "backend": "ChromaDB",
            "buffer_summary": summary,
            "buffer_rounds": rounds
        })

    def summarize(self, conversation):
        """多轮对话总结 - 提取关键信息并存入记忆"""
        import json
        
        # 调用 LLM 提取关键信息
        # 这里为了简化，先用规则提取。实际可以用 LLM API。
        lines = conversation.split("|")
        
        key_info = {
            "preferences": [],
            "decisions": [],
            "todos": [],
            "learning": []
        }
        
        # 简单关键词匹配（后续可以换成 LLM 调用）
        keywords = {
            "preferences": ["喜欢", "爱", "讨厌", "不喜欢", "偏好"],
            "decisions": ["决定", "好了", "可以", "就这样"],
            "todos": ["要", "记得", "待办", "下次"],
            "learning": ["学会", "学到", "知道", "了解"]
        }
        
        for line in lines:
            for pref in keywords["preferences"]:
                if pref in line:
                    key_info["preferences"].append(line.strip())
            for dec in keywords["decisions"]:
                if dec in line:
                    key_info["decisions"].append(line.strip())
            for todo in keywords["todos"]:
                if todo in line:
                    key_info["todos"].append(line.strip())
            for learn in keywords["learning"]:
                if learn in line:
                    key_info["learning"].append(line.strip())
        
        # 去重
        for k in key_info:
            key_info[k] = list(set(key_info[k]))[:5]  # 最多5条
        
        # 存入记忆
        summary_text = f"[总结] {json.dumps(key_info, ensure_ascii=False)}"
        result = self.remember(summary_text)
        
        return json.dumps({
            "extracted": key_info,
            "stored": result
        }, ensure_ascii=False)

    def _load_buffer(self):
        """加载总结缓冲区"""
        if os.path.exists(BUFFER_FILE):
            try:
                with open(BUFFER_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('summary', ''), data.get('round_count', 0)
            except:
                pass
        return '', 0

    def _save_buffer(self, summary, round_count):
        """保存总结缓冲区"""
        os.makedirs(os.path.dirname(BUFFER_FILE), exist_ok=True)
        with open(BUFFER_FILE, 'w', encoding='utf-8') as f:
            json.dump({'summary': summary, 'round_count': round_count}, f, ensure_ascii=False)

    def increment_summarize(self, new_conversation):
        """
        增量总结 - 每次只处理新增对话
        流程：加载上次总结 → 合并新对话 → 写入ChromaDB → 清空缓冲区
        """
        # 1. 加载上次的总结
        last_summary, round_count = self._load_buffer()
        
        # 2. 构建输入：上次总结 + 新对话
        if last_summary:
            input_text = f"上次总结：{last_summary}\n\n新增对话：{new_conversation}\n\n请提炼关键事实，保持上下文连贯，输出一句话总结。"
        else:
            input_text = f"对话：{new_conversation}\n\n请提炼关键事实，输出一句话总结。"
        
        # 3. 简单规则提取（后续可换 LLM）
        # 这里用关键词提取代替 LLM
        lines = new_conversation.split("|")
        facts = []
        for line in lines:
            line = line.strip()
            if any(k in line for k in ["喜欢", "讨厌", "决定", "想", "要", "NSFW"]):
                facts.append(line)
        
        if last_summary:
            new_summary = last_summary + " + " + " | ".join(facts) if facts else last_summary
        else:
            new_summary = " | ".join(facts) if facts else "暂无关键信息"
        
        # 4. 达到阈值，写入 ChromaDB
        new_round_count = round_count + 1
        if new_round_count >= SUMMARY_THRESHOLD:
            # 写入记忆
            self.remember(f"[增量总结] {new_summary}")
            # 清空缓冲区
            self._save_buffer('', 0)
            # 静默返回
            return ""
        else:
            # 存入缓冲区，等待下次
            self._save_buffer(new_summary, new_round_count)
            # 静默返回
            return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["remember", "recall", "forget", "status", "summarize", "increment_summarize"])
    parser.add_argument("--content", help="Content")
    parser.add_argument("--query", help="Query")
    parser.add_argument("--conversation", help="Multi-round conversation for summarize")
    
    args = parser.parse_args()
    skill = FluidMemorySkill()
    
    if args.action == "remember" and args.content:
        print(skill.remember(args.content))
    elif args.action == "recall" and args.query:
        print(skill.recall(args.query))
    elif args.action == "forget" and args.content:
        print(skill.forget(args.content))
    elif args.action == "status":
        print(skill.status())
    elif args.action == "summarize" and args.conversation:
        print(skill.summarize(args.conversation))
    elif args.action == "increment_summarize" and args.conversation:
        print(skill.increment_summarize(args.conversation))
