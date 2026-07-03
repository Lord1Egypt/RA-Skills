# Commit Discipline

SAFETY checkpoint 和增量提交规范。按需加载。

## Checkpoint Commit（SAFETY 阶段）

格式：
```
checkpoint: <简短描述>
```

示例：
```
checkpoint: before fixing auth middleware
checkpoint: before refactoring user service
checkpoint: before adding rate limiter
```

规则：
- 仅用于 SAFETY 回退点，不做为正式提交
- 始终在临时分支上
- 一个 SAFETY 阶段 = 一个 checkpoint

## 增量提交（EXECUTE 完成后，可选）

格式：
```
<type>: <简短描述>
```

type 取值：
| Type | 用途 |
|---|---|
| `feat` | 新功能 |
| `fix` | 修 bug |
| `refactor` | 重构（不改行为） |
| `chore` | 依赖更新、配置变更 |
| `test` | 加测试 |
| `docs` | 文档 |

示例：
```
feat: add rate limiter middleware
fix: handle null user in auth flow
refactor: extract token validation to separate fn
```

## 提交粒度

一个逻辑变更 = 一个 commit。

| ✅ 正确 | ❌ 错误 |
|---|---|
| `fix: handle null user` + `test: add null user test` | 一个 commit 包含 feat + fix + refactor |
| `refactor: extract validateToken()` 单独提交 | 重构混在 feat 里 |

## 关键规则

1. **Checkpoint 不 push** —— 临时分支仅本地，不回退就删除
2. **增量提交在临时分支上** —— 全部完成后由用户决定 merge/rebase 策略
3. **不自动 push** —— push 是用户决策，agent 不代劳
4. **Commit message 一行说清** —— 不要多行描述（除非用户要求）
