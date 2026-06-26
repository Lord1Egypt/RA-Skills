# Code Review Cycle

快捷命令：**`/cr <功能描述>`**

## 角色分工

| 角色 | 职责 | 权限 |
|------|------|------|
| **A (Coder)** | 写代码、改文件 | ✅ 可写 |
| **B (Reviewer)** | Review、提建议 | ❌ **只读** |

## 用法

### 基础用法（推荐）
```
/cr 实现用户登录表单验证
```
→ A=codex 写代码 → B=claude-code Review（只读） → 等你决定

### 指定 Agent
```
/cr --a claude --b codex 添加暗色模式
```

### 自动循环（最多 N 轮）
```
/cr --rounds 2 重构 utils/date.ts
```

## 输出格式

### A (编码)
```markdown
## [A-Code] 改动
- 文件 1: ...

## [A-Code] 说明
...
```

### B (Review - 只读)
```markdown
## [B-Review] 严重问题
- [ ] ...

## [B-Review] 建议
- [ ] ...

## [B-Review] 结论
□ 需要修改  □ 可以直接合并

---
[B 职责说明] 我只负责 Review，不修改任何文件。
```

## 后续操作

B Review 后，你可以说：
- `A，修改第 1、3 点` → 继续循环
- `可以了` / `结束` → 完成
- `B，再看一下 XXX` → 追加 Review（仍只读）
