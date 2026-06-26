# Hook System

Anima AIOS Hook 系统提供了统一的扩展机制，允许在关键节点注入自定义逻辑。

## 目录结构

```
hooks/
├── README.md                    # 本文件
├── builtin/                    # 内置 Hook 配置
│   ├── learning_logger.yaml    # 学习日志 Hook
│   ├── auth_check.yaml         # 权限检查 Hook
│   └── error_handler.yaml      # 错误处理 Hook
└── custom/                     # 自定义 Hook（用户添加）
```

## 内置 Hooks

### learning_logger

**类型:** POST_EXECUTE  
**优先级:** HIGH  
**功能:** 自动记录学习行为到 LEARNINGS.md 和 .learnings/ 目录

**触发条件:**
- 执行成功且有学习信号时
- 从 memory 文件提取到学习条目时

**输出:**
- `~/.anima/learnings/LEARNINGS.md` - 主学习日志
- `~/.anima/.learnings/{category}/` - 分类目录（兼容 self-improving-agent）

### auth_check

**类型:** PRE_EXECUTE  
**优先级:** CRITICAL  
**功能:** 执行前权限检查

**检查项:**
- 危险操作（delete, rm, sudo）需要确认
- 操作是否有权限
- 参数是否安全

### error_handler

**类型:** ON_ERROR  
**优先级:** CRITICAL  
**功能:** 错误自动记录和重试

**功能:**
- 错误分类和记录
- 指数退避重试
- 恢复策略执行

## Hook 配置格式

```yaml
# hook.yaml
name: hook_name           # Hook 名称（唯一标识）
description: 描述         # Hook 描述
trigger: pre_execute      # 触发类型
priority: high            # 优先级
enabled: true             # 是否启用

config:                   # Hook 特定配置
  # ... 配置项
```

## 触发类型

| 类型 | 说明 | 执行时机 |
|------|------|---------|
| `pre_execute` | 执行前 | 操作执行前 |
| `post_execute` | 执行后 | 操作执行后（无论成功或失败） |
| `on_error` | 错误时 | 操作发生错误时 |
| `on_success` | 成功时 | 操作成功完成时 |
| `on_timeout` | 超时时 | 操作超时时 |

## 优先级

| 优先级 | 值 | 说明 |
|--------|------|------|
| CRITICAL | 0 | 最高优先级，失败会阻止操作 |
| HIGH | 1 | 高优先级 |
| MEDIUM | 2 | 中优先级（默认） |
| LOW | 3 | 低优先级 |

## 使用示例

### 注册自定义 Hook

```python
from anima_aios.core.hook_manager import HookManager, HookTrigger, Priority

manager = HookManager()

async def my_hook(context):
    print(f"Hook triggered: {context}")
    # 自定义逻辑
    return

manager.register_hook(
    name="my_custom_hook",
    description="我的自定义 Hook",
    trigger=HookTrigger.POST_EXECUTE,
    priority=Priority.MEDIUM,
    func=my_hook
)
```

### 使用 Learning Logger

```python
from anima_aios.core.learning_logger import LearningLogger, LearningCategory, Priority

logger = LearningLogger()

# 记录纠正
logger.log_correction(
    summary="修复了内存泄漏问题",
    details="在关闭连接时没有正确释放资源",
    suggested_action="使用 context manager",
    area="memory"
)

# 记录洞察
logger.log_insight(
    summary="发现高效的缓存策略",
    details="使用 LRU 缓存可以显著提升性能",
    suggested_action="在生产环境应用",
    area="performance"
)
```

### 从 Memory 文件提取学习

```python
from anima_aios.core.learning_integration import LearningExtractor, MemoryWatcherLearning集成

# 提取学习条目
extractor = LearningExtractor()
content = Path("~/.anima/memory/2026-03-29.md").read_text()
entries = extractor.extract_from_content(content, "memory")

# 处理整个目录
processor = MemoryWatcherLearning集成()
results = processor.process_memory_directory()
```

## 与 self-improving-agent 兼容

Anima 的 Hook 系统与 self-improving-agent 完全兼容：

- 学习条目同步到 `~/.anima/.learnings/` 目录
- 使用相同的分类标准
- 兼容的文件格式

## 开发指南

### 创建新 Hook

1. 在 `hooks/custom/` 创建配置文件
2. 实现 Hook 函数
3. 注册到 HookManager

### Hook 函数签名

```python
# 同步 Hook
def sync_hook(context: Dict) -> None:
    pass

# 异步 Hook
async def async_hook(context: Dict) -> None:
    await do_something()
```

### Context 字典结构

```python
context = {
    "task_id": "task_001",           # 任务 ID
    "action": "write",               # 操作类型
    "target": "/path/to/file",       # 目标路径
    "result": {"status": "success"}, # 执行结果
    "error": None,                   # 错误信息（如有）
    "timestamp": "2026-03-29T15:00:00",
    # ... 其他上下文数据
}
```

---

_最后更新: 2026-03-29_
