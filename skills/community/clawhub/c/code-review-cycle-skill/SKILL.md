---
name: code-review-cycle
description: 执行 Coding ↔ Review 循环。A 写代码 → B Review → A 修改（可选）。支持 codex/claude-code 作为 A 或 B。
user-invocable: true
aliases: ["/cr", "/review-cycle", "/code-review"]
---

# Code Review Cycle

执行 A(编码) → B(Review) → 决策 的协作流程。

## 角色职责

| 角色 | 职责 | 权限 |
|------|------|------|
| **A (Coder)** | 写代码、改文件、实现功能 | ✅ 可写文件 |
| **B (Reviewer)** | Review 代码、提建议、做决策 | ❌ **只读，不写文件** |
| **主会话** | 调度 A/B、传递上下文、最终决策 | - |

## 触发方式

```
/cr <功能描述>
/cr --agent-a codex --agent-b claude-code <功能描述>
/cr --rounds 2 <功能描述>  # 最多自动循环 2 轮
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--agent-a` | `codex` | 负责写代码的 agent (codex/claude-code) |
| `--agent-b` | `claude-code` | 负责 Review 的 agent |
| `--rounds` | `0` | 自动循环轮数（0=只执行 A→B，等你决定） |
| `--cwd` | 当前 workspace | 代码目录 |

## 流程

1. **Spawn A** → 写代码，输出 diff + 说明
2. **Spawn B** → **只读 Review**，输出：严重问题/建议优化/结论（**不写文件**）
3. **决策点**：
   - 如果 `--rounds > 0` 且 B 认为需要修改 → 自动回到步骤 1（最多 rounds 轮）
   - 否则 → 等你指令

## 输出格式约定

### A 的输出
```markdown
## [A-Code] 改动摘要
- 文件 1: ...

## [A-Code] 实现说明
...

## [A-Code] 待确认点
1. ...
```

### B 的输出（只读 Review）
```markdown
## [B-Review] 严重问题
- [ ] ...

## [B-Review] 建议优化
- [ ] ...

## [B-Review] 结论
□ 需要修改（具体问题：#1, #3）
□ 可以直接合并

---
[B 职责说明] 我只负责 Review，不修改任何文件。如需修改，请 A 执行。
```

## 示例

```
/cr 实现用户登录表单验证
/cr --agent-a claude-code --agent-b codex 添加暗色模式切换
/cr --rounds 2 重构 utils/date.ts 增加单元测试
```

## 注意事项

- 主会话作为调度器，保留所有历史便于追溯
- 每轮结束后会暂停等你确认（除非 rounds>1）
- A 和 B 的会话是临时的，用完即弃（不保留上下文）
- **B 只读不写** — Review 角色不修改任何文件
