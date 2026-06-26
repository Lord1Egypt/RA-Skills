---
name: claude-code-engine
description: 将 OpenClaw 升级为 Claude-Code 引擎架构 - 并发执行/自我反思/向量检索/子代理系统/上下文压缩
---

# Claude-Code 引擎赋能 OpenClaw

> 整合 Claude-Code 核心架构 | 并发执行 | 自我反思 | 向量检索 | 子代理系统

---

## 一、核心定位

本技能帮助将 OpenClaw 升级为类 Claude-Code 的高效代理架构，核心目标：

| 目标 | 说明 |
|------|------|
| **并发执行** | 子代理并行处理，无需等待前序任务 |
| **自我反思** | 每6小时无交互时自动反思教训/经验/错误 |
| **向量检索** | 精准从记忆文件中找回历史内容 |
| **上下文压缩** | 92%阈值自动压缩，保留核心信息 |
| **长时自主** | 支持30-50小时连续运行 |

---

## 二、Claude-Code 核心架构

### 2.1 N0 引擎核心循环

```
┌─────────────────────────────────────────────────────┐
│              Claude-Code N0 循环架构                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│   while True:                                         │
│     ┌─────────┐                                      │
│     │ 获取输入 │ ← 用户请求 + 项目背景 + 系统状态      │
│     └────┬────┘                                      │
│          ↓                                           │
│     ┌─────────┐                                      │
│     │ 模型决策 │ → stop_reason + tool_calls          │
│     └────┬────┘                                      │
│          ↓                                           │
│     ┌─────────┐                                      │
│     │ 执行工具 │ → bash/read/write/edit/grep/browser │
│     └────┬────┘                                      │
│          ↓                                           │
│     ┌─────────┐                                      │
│     │ 反馈循环 │ → 工具结果返回 → 再次进入模型         │
│     └─────────┘                                      │
│          ↓                                           │
│   直到 stop_reason == endturn                        │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 2.2 七种内置工具

| 工具 | 功能 | OpenClaw 等价 |
|------|------|--------------|
| `bash` | 执行命令行 | `exec` |
| `read` | 读文件 | `read` |
| `write` | 写文件 | `write` |
| `edit` | 编辑文件 | `edit` |
| `glob/grep` | 搜索文件 | `exec find/grep` |
| `browser` | 访问网页 | `browser` |
| `skill` | 加载领域知识 | `skills` |

---

## 三、OpenClaw 升级清单

### 3.1 自我反思系统

**目标**：每6小时无交互时自动反思

```bash
# 创建自我反思脚本
cat > /root/.openclaw/scripts/self-reflection.sh << 'EOF'
#!/bin/bash
# OpenClaw 自我反思脚本
# 每6小时无交互时自动执行

REFLECTION_DIR="/root/.openclaw/workspace/memory/reflections"
mkdir -p "$REFLECTION_DIR"

反思内容包含：
- 教训 (lessons)
- 经验 (experiences)
- 错误 (errors)
- 成功 (successes)
- 待优化点 (improvements)

timestamp=$(date +%Y%m%d_%H%M%S)
log_file="$REFLECTION_DIR/${timestamp}.md"

cat > "$log_file" << 'LOG'
# 自我反思日志

## 时间
{TIMESTAMP}

## 教训 (Lessons)
-

## 经验 (Experiences)
-

## 错误 (Errors)
-

## 成功 (Successes)
-

## 待优化 (Improvements)
-

LOG

echo "反思已记录: $log_file"
EOF
chmod +x /root/.openclaw/scripts/self-reflection.sh

# 添加到 crontab（每6小时）
(crontab -l 2>/dev/null; echo "0 */6 * * * /root/.openclaw/scripts/self-reflection.sh") | crontab -
```

### 3.2 向量检索配置

**目标**：从记忆文件中精准检索

```bash
# 安装向量检索依赖
pip install chromadb sentence-transformers

# 创建向量检索脚本
cat > /root/.openclaw/scripts/vector-search.py << 'EOF'
#!/usr/bin/env python3
"""
OpenClaw 向量检索系统
基于 ChromaDB + Sentence-Transformers
"""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

class VectorMemory:
    def __init__(self, persist_dir="/root/.openclaw/workspace/memory/vector_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("openclaw_memory")
    
    def add_memory(self, text, metadata=None):
        """添加记忆到向量库"""
        embedding = self.model.encode([text])
        self.collection.add(
            embeddings=embedding.tolist(),
            documents=[text],
            metadatas=[metadata or {"source": "manual"}]
        )
    
    def search(self, query, n_results=5):
        """语义检索记忆"""
        embedding = self.model.encode([query])
        results = self.collection.query(
            query_embeddings=embedding.tolist(),
            n_results=n_results
        )
        return results
    
    def load_from_files(self, memory_dir="/root/.openclaw/workspace/memory"):
        """从文件批量加载记忆"""
        path = Path(memory_dir)
        for md_file in path.rglob("*.md"):
            content = md_file.read_text()
            self.add_memory(
                content,
                metadata={"source": str(md_file), "type": "memory"}
            )

if __name__ == "__main__":
    vm = VectorMemory()
    query = input("请输入检索内容: ")
    results = vm.search(query)
    print("检索结果:")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"\n{i+1}. [{meta['source']}]")
        print(doc[:200] + "..." if len(doc) > 200 else doc)
EOF
```

### 3.3 子代理并发系统

```bash
# 创建并发执行管理器
cat > /root/.openclaw/scripts/subagent_executor.py << 'EOF'
#!/usr/bin/env python3
"""
OpenClaw 子代理并发执行器
支持多任务并行处理，无需等待前序完成
"""

import asyncio
import concurrent.futures
from typing import List, Callable, Any
import subprocess
import json

class SubAgentExecutor:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    def run_task(self, task: dict) -> dict:
        """执行单个子任务"""
        task_type = task.get("type")
        command = task.get("command")
        
        if task_type == "bash":
            result = subprocess.run(
                command, shell=True, 
                capture_output=True, text=True, timeout=task.get("timeout", 300)
            )
            return {
                "task_id": task.get("id"),
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
        elif task_type == "skill":
            # 调用 OpenClaw skill
            result = subprocess.run(
                f"npx clawhub@latest run {command}",
                shell=True, capture_output=True, text=True
            )
            return {
                "task_id": task.get("id"),
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout
            }
        return {"task_id": task.get("id"), "status": "unknown_type"}
    
    def run_parallel(self, tasks: List[dict]) -> List[dict]:
        """并发执行多个任务"""
        futures = [self.executor.submit(self.run_task, task) for task in tasks]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
        return results

if __name__ == "__main__":
    executor = SubAgentExecutor(max_workers=5)
    
    # 示例：并行执行多个任务
    tasks = [
        {"id": "task1", "type": "bash", "command": "ls -la /root"},
        {"id": "task2", "type": "skill", "command": "mckinsey-frameworks"},
        {"id": "task3", "type": "bash", "command": "git status"},
    ]
    
    results = executor.run_parallel(tasks)
    print(json.dumps(results, indent=2))
EOF
```

---

## 四、上下文压缩系统

### 4.1 92% 阈值压缩

```python
# 创建上下文管理器
cat > /root/.openclaw/scripts/context_compressor.py << 'EOF'
#!/usr/bin/env python3
"""
OpenClaw 上下文压缩管理器
当上下文达到 92% 时自动压缩
"""

import os
import json
from pathlib import Path

class ContextCompressor:
    def __init__(self, max_tokens=200000, compression_threshold=0.92):
        self.max_tokens = max_tokens
        self.threshold = compression_threshold
        self.current_usage = 0
    
    def check_and_compress(self, messages: list) -> list:
        """检查上下文使用率并在需要时压缩"""
        total_tokens = sum(len(str(m)) // 4 for m in messages)
        self.current_usage = total_tokens / self.max_tokens
        
        if self.current_usage >= self.threshold:
            return self.compress(messages)
        return messages
    
    def compress(self, messages: list) -> list:
        """压缩策略：保留关键决策和结果"""
        compressed = []
        for msg in messages:
            content = str(msg.get("content", ""))
            # 保留关键信息：决策、结论、结果
            if any(kw in content for kw in ["✅", "❌", "决策", "结论", "result", "error"]):
                compressed.append(msg)
            # 保留工具调用结果
            elif msg.get("role") == "tool":
                compressed.append(msg)
        return compressed
    
    def extract_summary(self, messages: list) -> str:
        """提取中间总结"""
        summary = []
        for msg in messages:
            content = str(msg.get("content", ""))
            if any(kw in content for kw in ["架构选择", "测试结论", "决策", "selected"]):
                summary.append(content[:200])
        return "\n".join(summary)
EOF
```

### 4.2 记忆文件化系统

```markdown
# 四层记忆文件结构（参考 Claude-Code）

root: /root/.openclaw/workspace/memory/
├── daily/                 # 每日日志
│   ├── 2026-04-19.md
│   └── 2026-04-25.md
├── reflections/           # 自我反思
│   └── ${timestamp}.md
├── lessons/             # 经验总结
│   └── lessons.md
└── memory.md            # 索引文件（由 AGENTS.md 管理）
```

---

## 五、并发执行配置

### 5.1 子代理配置

```json
// /root/.openclaw/config/subagents.json
{
  "enabled": true,
  "max_concurrent": 5,
  "default_timeout": 300,
  "strategies": {
    "code_review": {
      "type": "skill",
      "skill": "code-review"
    },
    "research": {
      "type": "skill", 
      "skill": "browser-use"
    },
    "documentation": {
      "type": "skill",
      "skill": "docs-generator"
    }
  }
}
```

### 5.2 并发执行示例

```python
# 并发执行示例
tasks = [
    {"id": "1", "type": "code_review", "target": "src/main.py"},
    {"id": "2", "type": "research", "query": "latest AI trends"},
    {"id": "3", "type": "documentation", "target": "API docs"},
]

executor = SubAgentExecutor(max_workers=3)
results = executor.run_parallel(tasks)
```

---

## 六、长时自主运行配置

### 6.1 健康检查脚本

```bash
cat > /root/.openclaw/scripts/health_check.sh << 'EOF'
#!/bin/bash
# OpenClaw 长时运行健康检查

LOG_FILE="/root/.openclaw/logs/agent_health.log"
MAX_IDLE_HOURS=6

check_idle() {
    last_activity=$(stat -c %Y /root/.openclaw/workspace/memory/memory.md 2>/dev/null || echo 0)
    now=$(date +%s)
    idle_hours=$(( (now - last_activity) / 3600 ))
    
    if [ $idle_hours -ge $MAX_IDLE_HOURS ]; then
        echo "[$(date)] 检测到空闲${idle_hours}小时，执行自我反思..." >> $LOG_FILE
        /root/.openclaw/scripts/self-reflection.sh
    fi
}

check_memory() {
    mem_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100}')
    if (( $(echo "$mem_usage > 90" | bc -l) )); then
        echo "[$(date)] 内存使用率${mem_usage}%，触发压缩..." >> $LOG_FILE
        python3 /root/.openclaw/scripts/context_compressor.py --compress
    fi
}

check_idle
check_memory
EOF
chmod +x /root/.openclaw/scripts/health_check.sh

# 添加到 crontab（每30分钟检查）
(crontab -l 2>/dev/null; echo "*/30 * * * * /root/.openclaw/scripts/health_check.sh") | crontab -
```

---

## 七、Claude-Code 工作流集成

### 7.1 N0 循环实现

```python
# claude_code_loop.py
import asyncio
from typing import Optional

class N0Engine:
    """Claude-Code N0 循环引擎"""
    
    def __init__(self):
        self.running = False
        self.context = []
    
    async def step(self, user_input: str) -> str:
        """单步执行"""
        # 1. 获取输入
        self.context.append({"role": "user", "content": user_input})
        
        # 2. 模型决策（调用 LLM）
        response = await self.llm.chat(messages=self.context)
        
        # 3. 执行工具
        if response.tool_calls:
            for tool in response.tool_calls:
                result = await self.execute_tool(tool)
                self.context.append({"role": "tool", "content": result})
        
        # 4. 检查停止条件
        if response.stop_reason == "endturn":
            self.running = False
        
        return response.content
    
    async def run(self, user_input: str):
        """主循环"""
        self.running = True
        while self.running:
            result = await self.step(user_input)
            print(result)
            user_input = input("> ")
    
    async def execute_tool(self, tool_call: dict) -> str:
        """执行工具调用"""
        tool_name = tool_call["name"]
        args = tool_call["arguments"]
        
        if tool_name == "bash":
            return await self.run_bash(args["command"])
        elif tool_name == "read":
            return self.read_file(args["path"])
        # ... 其他工具
        
        return "tool executed"
```

### 7.2 与 OpenClaw 集成

```python
# openclaw_n0_bridge.py
from openclaw import OpenClaw

class OpenClawN0Bridge:
    """将 N0 引擎桥接到 OpenClaw"""
    
    def __init__(self, openclaw: OpenClaw):
        self.oc = openclaw
        self.context = []
    
    async def process(self, user_input: str) -> str:
        """处理用户输入"""
        # 添加到上下文
        self.context.append({"role": "user", "content": user_input})
        
        # 检查压缩
        compressor = ContextCompressor()
        self.context = compressor.check_and_compress(self.context)
        
        # 调用 OpenClaw 处理
        response = await self.oc.chat(messages=self.context)
        
        # 添加响应到上下文
        self.context.append({"role": "assistant", "content": response})
        
        return response
```

---

## 八、使用方式

### 触发场景

```
用户说「启动 Claude-Code 模式」→ 激活 N0 引擎
用户说「并发执行这些任务」→ 触发子代理系统
用户说「搜索记忆」→ 启动向量检索
用户说「自我反思」→ 执行反思脚本
用户说「检查上下文」→ 触发压缩检查
```

### 配置检查清单

```bash
# 1. 确认 crontab 已配置
crontab -l | grep self-reflection

# 2. 确认向量数据库已初始化
ls /root/.openclaw/workspace/memory/vector_db/

# 3. 确认并发执行器可运行
python3 /root/.openclaw/scripts/subagent_executor.py --test

# 4. 确认健康检查已启用
ps aux | grep health_check
```

---

## 九、技术对比

| 功能 | Claude-Code | OpenClaw (当前) | OpenClaw (目标) |
|------|------------|----------------|----------------|
| N0 循环 | ✅ while True | ⚠️ 单次交互 | ✅ 实现 |
| 并发执行 | ✅ 子代理并行 | ❌ 顺序执行 | ✅ 实现 |
| 上下文压缩 | ✅ 92% 阈值 | ❌ 无 | ✅ 实现 |
| 自我反思 | ✅ 日志记录 | ⚠️ 手动 | ✅ 自动 |
| 向量检索 | ⚠️ 外部工具 | ❌ 无 | ✅ 实现 |
| 7 种内置工具 | ✅ 完整 | ⚠️ 部分 | ✅ 补充 |

---

## 十、已知限制

```
⚠️ 限制说明：
- N0 引擎需要持续运行进程，当前 OpenClaw 为请求-响应模式
- 并发执行需要多进程/多线程支持，单核环境受限
- 向量检索需要额外存储（约 500MB 用于向量库）
- 自我反思依赖 LLM 调用，需 API Key
- 部分功能需要 root 权限（crontab）
```

---

## 十一、相关技能

| 技能 | 关系 |
|------|------|
| `thinking-knowledge-system` | 认知闭环构建 |
| `ai-research-tools` | 子代理研究系统 |
| `browser-use` | 浏览器工具支持 |

---

*本技能帮助将 OpenClaw 升级为类 Claude-Code 的高效代理架构*
