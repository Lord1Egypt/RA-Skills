# 使用手册

## 快速开始

### 1. 查看记忆

```bash
python3 skill.py profile
```

### 2. 添加记忆

```bash
python3 skill.py add --content "我喜欢简洁" --type preference
```

### 3. 检索记忆

```bash
python3 skill.py search --query "项目"
```

---

## 命令行使用

### 查看用户画像

```bash
python3 skill.py profile
```

输出示例：
```json
{
  "preferences": ["我喜欢简洁的汇报风格"],
  "facts": ["我负责 POC 项目"],
  "tasks": ["每周四提交 OKR 周报"],
  "general": []
}
```

### 检索记忆

```bash
python3 skill.py search --query "项目" --k 5
```

参数：
- `--query`: 搜索关键词
- `--k`: 返回数量（默认 5）

### 添加记忆

```bash
python3 skill.py add --content "内容" --type preference
```

类型：
- `preference`: 偏好
- `fact`: 事实
- `task`: 任务
- `general`: 其他

### 自动抽取

```bash
python3 skill.py auto --message "我负责 POC 项目，喜欢简洁的代码"
```

自动识别并保存记忆。

### 查看统计

```bash
python3 skill.py stats
```

输出：
```json
{
  "total_memories": 10,
  "by_type": {
    "preference": 3,
    "fact": 4,
    "task": 3
  }
}
```

### 清理过期记忆

```bash
python3 skill.py cleanup
```

---

## Python API

### 初始化

```python
from skills.memory.openclaw_integration import OpenClawMemoryIntegration

mem = OpenClawMemoryIntegration(user_id="ou_xxx")
```

### 生成 System Prompt

```python
prompt = mem.get_session_system_prompt("你是小美式")
print(prompt)
```

### 检索记忆

```python
results = mem.search_memory("项目", k=5)
for r in results:
    print(f"{r['type']}: {r['content']}")
```

### 添加记忆

```python
mem.add_memory(
    content="我喜欢简洁",
    type="preference",
    importance=0.8
)
```

### 获取用户画像

```python
profile = mem.get_user_profile()
print(f"偏好：{profile['preferences']}")
print(f"事实：{profile['facts']}")
print(f"任务：{profile['tasks']}")
```

---

## 最佳实践

### 1. 记忆命名

使用清晰、具体的描述：

✅ 好："我负责 POC 项目，使用 OceanBase 数据库"  
❌ 差："POC 项目"

### 2. 类型选择

- **preference**: 个人偏好、习惯
- **fact**: 客观事实、背景信息
- **task**: 有待办、有截止时间
- **general**: 其他

### 3. 重要性评分

```python
mem.add_memory("重要项目", importance=0.9)  # 0-1，越高越重要
```

### 4. 任务过期时间

```python
mem.add_memory(
    "明天开会",
    type="task",
    expires_hours=24
)
```

---

## 高级用法

### 批量添加

```python
memories = [
    ("我喜欢简洁", "preference"),
    ("我负责 POC", "fact"),
    ("周四交周报", "task")
]

for content, type in memories:
    mem.add_memory(content, type=type)
```

### 自定义检索

```python
results = mem.memory.search_memories(
    query="项目",
    user_id="ou_xxx",
    k=10,
    type_filter=["fact", "task"],
    min_importance=0.5
)
```

### 导出记忆

```python
import json

profile = mem.get_user_profile()
with open("memories.json", "w") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
```

---

## 提示与技巧

### 1. 定期清理

```bash
# 每周清理一次
python3 skill.py cleanup
```

### 2. 备份记忆

```bash
cp -r memory_lancedb memory_lancedb_backup
```

### 3. 多用户支持

```python
mem1 = OpenClawMemoryIntegration(user_id="user1")
mem2 = OpenClawMemoryIntegration(user_id="user2")
```

### 4. 批量导入

```python
import json

with open("memories.json") as f:
    data = json.load(f)

for content in data["preferences"]:
    mem.add_memory(content, type="preference")
```

---

需要更多帮助？查看 [FAQ.md](FAQ.md)
