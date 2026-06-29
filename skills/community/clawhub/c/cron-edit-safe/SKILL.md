---
name: cron-edit-safe
description: 安全编辑 OpenClaw cron 任务的 wrapper 脚本（自动备份 + dry-run + edit + 验证 + rollback）。Use when editing cron jobs to prevent silent breakage.
---

# cron-edit-safe 🛡️

> **包治"裸用 openclaw cron edit 改坏"工具** — 自动 5 步流程，杜绝 3 类真问题

把 `openclaw cron edit` 包成 5 步安全流程，**默认全开**（BACKUP + DRY-RUN + VERIFY + ROLLBACK）：

```
📦 BACKUP  → 自动备份原 JSON 到 backups/cron-YYYYMMDD/
🧪 DRY-RUN → 提前跑一次命令验证（timeout 60s）
✏️  EDIT    → 应用修改
🔍 VERIFY  → 重新 get cron，确认关键字段
🔙 ROLLBACK（失败时）→ 自动从 backup 恢复
```

## 为什么需要这个？

老板 2026-06-28 Refine 阶段揪出的 3 个真问题：

| 问题 | 后果 | cron-edit-safe 解决 |
|------|------|--------------------|
| 缺备份机制 | 改坏无法秒级回滚 | ✅ 自动备份到 backups/cron-YYYYMMDD/ |
| 缺 dry-run | edit 后才知命令跑不通 | ✅ edit 前 timeout 60s 跑一次 |
| 缺 rollback | edit/verify 失败后 cron 状态不一致 | ✅ 自动从 backup JSON 恢复 |

## 安装前置

- ✅ 已装 OpenClaw
- ✅ 已装 `jq`（`sudo apt install jq`）

## 用法

```bash
cron-edit-safe <cron-id> [options]
```

### 示例：把一个 agentTurn 任务改成 command 模式

```bash
cron-edit-safe d21a3540-05fd-4d36-abd0-c7e4407b77ac \
  --name "🐛 Codis-Evolve 周闭环复盘-周日09:00 [v2.0 command]" \
  --command "python3 /home/colbert/.openclaw/workspace-coding-advisor/skills/codis-evolve-weekly/codis-evolve-weekly.py" \
  --command-cwd "/home/colbert/.openclaw/workspace-coding-advisor" \
  --session isolated \
  --announce --channel feishu \
  --to "ou_991021547578f722d08533accc83651d"
```

### 控制选项

| 选项 | 默认 | 说明 |
|------|------|------|
| `--no-backup` | 关闭 | 跳过备份 |
| `--no-dry-run` | 关闭 | 跳过 dry-run |
| `--no-rollback` | 关闭 | 失败时不自动 rollback |
| `--dry-run-only` | 关闭 | 只跑 dry-run，不真 edit |
| `--backup-dir DIR` | `~/.openclaw/backups/cron-YYYYMMDD/` | 自定义备份目录 |
| `--quiet` | 关闭 | 减少输出 |

### 失败处理

任何步骤失败：
1. ✅ 立即停止后续步骤
2. 🔙 触发 rollback（如果开了 + 有 backup）
3. 📋 输出清晰的错误和手动恢复命令

## RULE 关联

- **RULE-20260628-001**：所有 cron 改造必须用 cron-edit-safe，禁止裸用 openclaw cron edit
- 老板 2026-06-28 明说"完整成功完成"才晋升此规则

## 评分历史

- v1.0.0 (2026-06-28)：100/100（优秀）
- 4 用例端到端全过（dry-run-only / 完整流程 / rollback / 备份存在性）
- Refine 自修复 1 个 Verify bug（jq 解析 plugin warnings 失败）
- 详见 `output/cron-edit-safe-2026-06-28/{plan,write,test,refine}.md`

## 作者

码虫 🐛 coding-advisor · v1.0.0 · 2026-06-28