# API 规格说明书 — 认知力增强引擎 (Cognitive Enhancement Engine)

## CognitiveEnhancer

核心类，整合所有认知能力。

### 构造函数

```python
CognitiveEnhancer(
    long_term_capacity: int = 1000,
    working_memory_size: int = 10,
    similarity_threshold: float = 0.15
)
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `long_term_capacity` | int | 1000 | 长期记忆最大条目数 |
| `working_memory_size` | int | 10 | 工作记忆 FIFO 缓存大小 |
| `similarity_threshold` | float | 0.15 | 检索相似度最低阈值 |

---

### 方法

#### `perceive(observation: str) -> None`
将感知信息存入工作记忆。

- **输入：** `observation` — 感知文本（非空字符串）
- **输出：** 无
- **错误：** 空字符串抛出 ValueError

#### `recall(query: str, top_k: int = 5) -> List[Dict]`
从长期记忆中检索最相关内容。

- **输入：** `query` — 查询文本；`top_k` — 返回结果数（1-50）
- **输出：** `[{content, metadata, importance, score, timestamp}, ...]`
- **错误：** 空 query 返回空列表

#### `memorize(content: str, metadata: Optional[Dict] = None, importance: float = 1.0) -> str`
将内容存入长期记忆。

- **输入：** `content` — 记忆内容；`metadata` — 元数据字典；`importance` — 重要性（0-2.0）
- **输出：** `memory_id` — 记忆唯一标识
- **错误：** 空内容抛出 ValueError

#### `plan(goal: str) -> List[Dict]`
将目标分解为可执行步骤。

- **输入：** `goal` — 目标描述
- **输出：** `[{step_id, action, params, expected_output}, ...]`
- **任务类型自动检测：** 计算、搜索、摘要、翻译、写作

#### `reason(problem: str) -> str`
基于长期记忆进行推理问答。

- **输入：** `problem` — 问题描述
- **输出：** 推理结果文本

#### `reflect() -> List[str]`
主动反思，挖掘失败模式并生成改进建议。

- **输入：** 无
- **输出：** 建议列表

#### `execute_task(goal: str, executor: Optional[Callable] = None) -> Dict`
完整任务执行流程（规划 → 执行 → 记忆 → 反思）。

- **输入：** `goal` — 目标；`executor` — 自定义执行函数（默认用内置推理器）
- **输出：** `{goal, plan, result, reflections, status, working_memory, ...}`

#### `get_status() -> Dict`
返回引擎完整运行状态。

- **输入：** 无
- **输出：** `{long_term_count, working_memory, reflection_count, ...}`

---

## 内部组件

### Tokenizer
统一分词工具，中英文基础支持。

### VectorMemory
TF-IDF + 倒排索引的长期记忆存储，O(n) 检索 → O(query_tokens)。

### WorkingMemory
FIFO 短期上下文缓存，附带时间戳。

### Planner
目标分解引擎，通过关键词匹配自动识别任务类型。

### Reasoner
基于记忆检索的问答引擎。

### Reflector
失败模式记录和重复失败规律挖掘。

### MetacognitiveMonitor
任务耗时和错误率追踪。
