---
name: claude-code-architecture
description: 基于 Claude Code 源码分析提炼的 AI Agent 架构设计模式。当你需要设计/重构 Agent 工具系统、安全门控、上下文压缩、任务编排时使用。
version: 2.0.3
author: di
tags: [agent, architecture, harness, safety, tool-system]
---

# AI Agent 架构设计模式

> 从公开的 Agent 架构讨论和主流框架设计中提炼的实战设计模式
> 触发：设计Agent工具系统 / 实现安全门控 / 优化上下文管理 / 搭建多Agent编排

---

## ⚡ 快速使用

当 agent 需要进行架构设计时，按场景选择模板：

| 场景 | 对应模板 | 触发词 |
|------|----------|--------|
| 需要工具权限控制 | 模板 A：权限门控 | "生成权限门控代码" |
| Token 消耗太大 | 模板 B：工具按需加载 | "实现工具按需加载" |
| 上下文快满了 | 模板 C：上下文压缩 | "生成上下文压缩方案" |
| 多工具并发 | 模板 D：读写分离 | "实现读写分离调度" |

Agent 应按当前任务选择模板并生成定制代码。

⚠️ **安全规则**：
- 生成代码前须告知用户目标路径，**等待确认再写入**
- 不可直接覆盖已有文件（先备份或询问）
- 建议用户在新分支或沙箱环境中测试生成代码
- 模板代码为设计参考，需要根据实际项目调整

---

## 🏛️ 核心原则

**护城河不是模型，是 harness（框架）** — 任务编排、工具系统、上下文管理、安全机制

### 七大设计模式

| # | 模式 | 一句话 |
|---|------|--------|
| 1 | Initiative/Execution 分离 | 规划层与执行层解耦 |
| 2 | 读写分离并发 | 只读并行，写入排队 |
| 3 | 工具按需加载 | 先给轻量索引，选中后再加载完整参数 |
| 4 | 记忆不记代码 | 代码事实实时从源码读取 |
| 5 | 五级上下文压缩 | 剪裁→精简→折叠→AI总结→强制保留 |
| 6 | 插件式工具架构 | 每个工具独立权限+验证+格式化 |
| 7 | Fail-closed 安全 | 默认拒绝，显式授权 |

---

## 模板 A：权限门控

```python
class ToolPermissionGate:
    """Fail-closed 权限门控。默认拒绝，显式授权。"""
    def __init__(self):
        self.permissions = {}
        self.default = "none"
    
    def can_execute(self, tool_name: str, user: str) -> bool:
        if not self._is_declared_readonly(tool_name):
            return self.permissions.get(user, self.default) >= self._required_level(tool_name)
        return True
    
    def request(self, tool_name: str) -> str:
        return f"⚠️ 需要授权执行 {tool_name}。确认吗？"
```

参考具体实现：`references/permission_gate_full.py`

---

## 模板 B：工具按需加载

```python
class ToolRegistry:
    """轻量索引 → 选中 → 加载完整参数"""
    def __init__(self):
        self.index = {}      # 轻量：名称+用途
        self.loaders = {}    # 完整参数加载器
    
    def list_tools(self) -> list:
        return [{"name": k, "purpose": v} for k, v in self.index.items()]
    
    def get_full(self, name: str) -> dict:
        return self.loaders[name]() if name in self.loaders else None
```

参考具体实现：`references/tool_lazy_loading_full.py`

---

## 模板 C：五级上下文压缩

| 级别 | 方法 | 适用 |
|------|------|------|
| 1 Prune | 删除低价值消息 | 日常清理 |
| 2 Micro | 精简长消息 | 接近限制 |
| 3 Fold | 折叠摘要 | 上下文紧张 |
| 4 Auto | AI 自动总结 | 严重溢出 |
| 5 Hard | 强制保留关键信息 | 最后手段 |

```python
class ContextCompressor:
    LEVELS = {1: "prune", 2: "micro", 3: "fold", 4: "auto", 5: "hard"}
    
    def compress(self, messages: list, level: int, max_tokens: int) -> list:
        # 按级别执行对应压缩策略
        ...
```

参考具体实现：`references/context_compressor_full.py`

---

## 模板 D：读写分离调度

```python
class ReadWriteScheduler:
    """只读操作并发，写操作排队"""
    async def execute(self, ops: list) -> list:
        reads = [op for op in ops if op.is_readonly]
        writes = [op for op in ops if not op.is_readonly]
        
        results = await asyncio.gather(*[self._read(op) for op in reads])
        for op in writes:
            results.append(await self._write(op))
        return results
```

参考具体实现：`references/rw_scheduler_full.py`

---

## 📦 结构

```
claude-code-architecture/
├── SKILL.md                              # 主文件（含 4 个内联模板）
└── references/
    ├── permission_gate_full.py           # 模板 A 完整实现
    ├── tool_lazy_loading_full.py         # 模板 B 完整实现
    ├── context_compressor_full.py        # 模板 C 完整实现
    ├── rw_scheduler_full.py             # 模板 D 完整实现
    └── framework_comparison.md           # 主流框架对比
```

## 📖 参考资料

- 完整代码实现 → `references/` 目录各模板完整版
- 与其他框架对比 → `references/framework_comparison.md`
- 设计思想来源 → 公开的主流 Agent 框架架构讨论

---

_版本 2.0.3 | 修复权限门控默认拒绝、审批检查、摘要角色_
