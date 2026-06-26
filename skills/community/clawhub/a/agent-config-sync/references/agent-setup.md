# Per-Agent Auto-Sync Setup

For each agent workspace, create or append to these files:

## 1. SYNC.md (new file)

```markdown
# 配置同步机制 — 自动获取变更通知

## 检查入口
每次启动/激活时，先检查工作空间下的 `pending_sync.md` 是否存在且非空。

## 同步检查流程
```
启动/激活 → 检查工作目录存在 pending_sync.md?
  ├─ ✅ 有内容 → 读取变更摘要 → 更新本地 MEMORY.md
  │              → 根据变更内容更新本地配置
  │              → 删除 pending_sync.md（标记已处理）
  │              → 回复 AMaster 确认已同步
  └─ ❌ 无文件或空 → 无需同步
```

## 同步源
- 完整变更日志: `/home/admin/.openclaw/workspace-amaster/memory/CHANGELOG.md`
- 当前版本: `/home/admin/.openclaw/workspace-amaster/memory/.current_system_version`
- 主动查询: 可向 AMaster 询问最新版本状态

## 重要
- 使用量化交易系统 / 比价系统前，必须确认版本信息
- 如果有 pending_sync.md 但未处理，不要使用相关系统功能
```

## 2. BOOTSTRAP.md (append to end)

```markdown
## 启动检查 — 配置同步
- [ ] 检查工作目录下是否存在 `pending_sync.md`
  - 存在 → 读取变更摘要，更新 MEMORY.md，删除 pending_sync.md
  - 不存在 → 无需同步
- [ ] 使用量化系统/比价系统前先确认版本
```

## 3. HEARTBEAT.md (append to end)

```markdown
## ⭐ 配置同步检查（每次 heartbeat 执行）
- [ ] 检查工作目录下是否存在 `pending_sync.md`
  - 存在且非空 → 读取变更摘要，更新 MEMORY.md，删除文件
  - 不存在 → 跳过
```
