# API 参考

## OpenClawMemoryIntegration

主集成类，提供所有记忆管理功能。

### 初始化

```python
from skills.memory.openclaw_integration import OpenClawMemoryIntegration

mem = OpenClawMemoryIntegration(
    user_id="ou_xxx"  # 用户 ID
)
```

### 方法

#### get_session_system_prompt(base_prompt)

生成包含记忆的 system prompt。

**参数**:
- `base_prompt` (str): 基础 system prompt

**返回**: str - 完整的 system prompt

**示例**:
```python
prompt = mem.get_session_system_prompt("你是小美式")
```

---

#### search_memory(query, k=5)

检索记忆。

**参数**:
- `query` (str): 搜索关键词
- `k` (int): 返回数量

**返回**: List[Dict] - 记忆列表

**示例**:
```python
results = mem.search_memory("项目", k=5)
for r in results:
    print(r["content"], r["type"])
```

---

#### add_memory(content, type="general", **kwargs)

添加记忆。

**参数**:
- `content` (str): 记忆内容
- `type` (str): 记忆类型
- `importance` (float): 重要性（0-1）
- `expires_hours` (int): 过期时间（小时）

**返回**: str - 记忆 ID

**示例**:
```python
mem.add_memory("我喜欢简洁", type="preference", importance=0.8)
```

---

#### get_user_profile()

获取用户画像。

**返回**: Dict - 用户画像

**示例**:
```python
profile = mem.get_user_profile()
print(profile["preferences"])
print(profile["facts"])
print(profile["tasks"])
```

---

#### cleanup_expired()

清理过期记忆。

**返回**: int - 清理数量

**示例**:
```python
count = mem.cleanup_expired()
print(f"清理了 {count} 条记忆")
```

---

## LanceDBMemory

底层记忆管理类。

### 初始化

```python
from skills.memory.lancedb_memory import LanceDBMemory

db = LanceDBMemory(
    db_path="./memory_lancedb",
    embedding_model="embedding-3"
)
```

### 方法

#### search_memories(query, user_id, k=5, ...)

语义检索记忆。

**参数**:
- `query` (str): 查询文本
- `user_id` (str): 用户 ID
- `k` (int): 返回数量
- `type_filter` (List[str]): 类型过滤
- `min_importance` (float): 最小重要性

**返回**: List[Dict]

---

#### add_memory(content, user_id, type, ...)

添加记忆。

**参数**:
- `content` (str): 内容
- `user_id` (str): 用户 ID
- `type` (str): 类型
- `metadata` (Dict): 元数据
- `expires_hours` (int): 过期时间

**返回**: str - 记忆 ID

---

#### get_user_profile(user_id)

获取用户画像。

**返回**: Dict

---

#### format_memories_for_prompt(memories)

格式化记忆为 Prompt。

**参数**:
- `memories` (List[Dict]): 记忆列表

**返回**: str

---

## AutoMemoryExtractor

自动记忆抽取器。

### 初始化

```python
from skills.memory.auto_memory import AutoMemoryExtractor

extractor = AutoMemoryExtractor(mem)
```

### 方法

#### extract_from_message(message)

从消息中提取记忆。

**参数**:
- `message` (str): 用户消息

**返回**: List[Dict] - 提取的记忆

**示例**:
```python
extracted = extractor.extract_from_message("我喜欢简洁的代码")
for e in extracted:
    print(e["content"], e["type"])
```

---

#### save_memories(extracted, **kwargs)

保存提取的记忆。

**参数**:
- `extracted` (List[Dict]): 提取的记忆列表

**返回**: List[str] - 保存的记忆 ID

---

## 工具函数

### init_memory(user_id)

快捷初始化。

```python
from skills.memory.openclaw_integration import init_memory

mem = init_memory("ou_xxx")
```

### build_system_prompt(base_prompt, mem)

构建 system prompt。

```python
from skills.memory.openclaw_integration import build_system_prompt

prompt = build_system_prompt("你是小美式", mem)
```
