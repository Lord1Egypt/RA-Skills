## 使用方式总览

Clawmerge 有两种使用方式：

1. **手动命令行使用**：你直接在服务器终端运行脚本，适合明确知道要备份/恢复哪个文件。
2. **通过 OpenClaw 调用技能**：你直接对 OpenClaw 说“帮我做灾难备份/恢复检查/合并恢复”，由助手先判断风险，再调用脚本或给出确认步骤。

---

## 手动备份模式

### 1. 普通 workspace 备份

只备份当前 workspace：记忆、人格、脚本、skills、配置模板等。

```bash
cd ~/.openclaw/workspace
bash skills/clawmerge/scripts/one-click-backup.sh ~/backups/workspace-$(date +%Y%m%d).tar.gz
```

适合：日常备份、改脚本前留档、迁移一部分 workspace。

### 2. 普通 workspace 备份预览

```bash
bash skills/clawmerge/scripts/one-click-backup.sh ~/backups/test.tar.gz --dry-run
```

只预览，不创建备份。

### 3. 灾难完整备份

备份范围更大：workspace + system config + cron + agent auth + sessions。

```bash
bash skills/clawmerge/scripts/one-click-full-backup.sh ~/openclaw-disaster-backup.tar.gz
```

适合：重装系统前、迁移整台 OpenClaw、重大升级前。

### 4. 灾难完整备份但排除 sessions

```bash
bash skills/clawmerge/scripts/one-click-full-backup.sh ~/openclaw-disaster-backup.tar.gz --no-sessions
```

适合：想减小备份体积，或者不需要历史会话。

### 5. 灾难完整备份预览

```bash
bash skills/clawmerge/scripts/one-click-full-backup.sh ~/openclaw-disaster-backup.tar.gz --dry-run
```

---

## 手动恢复模式

### 1. 普通 workspace 恢复（合并/安全）

```bash
cd ~/.openclaw/workspace
bash skills/clawmerge/scripts/one-click-restore.sh /path/to/workspace-backup.tar.gz --dry-run
bash skills/clawmerge/scripts/one-click-restore.sh /path/to/workspace-backup.tar.gz --merge
```

建议先 `--dry-run`，确认内容后再 `--merge`。

### 2. 灾难恢复预览

```bash
bash skills/clawmerge/scripts/one-click-full-restore.sh /path/to/openclaw-disaster-backup.tar.gz --dry-run
```

只检查备份包和恢复计划，不修改任何文件。

### 3. 灾难恢复（默认安全模式）

```bash
bash skills/clawmerge/scripts/one-click-full-restore.sh /path/to/openclaw-disaster-backup.tar.gz
```

默认安全模式会：

- `openclaw.json`、`.env`、cron、agent auth → 放入 `~/.openclaw/restore-candidates/<timestamp>/`
- sessions → 放入 `~/.openclaw/agents/main/sessions-restored-<timestamp>/`
- workspace → 解压时跳过已有文件，避免覆盖当前记忆/人格

### 4. 灾难恢复（危险全覆盖模式）

```bash
bash skills/clawmerge/scripts/one-click-full-restore.sh /path/to/openclaw-disaster-backup.tar.gz --unsafe-overwrite
```

只有在你明确要用备份覆盖当前运行环境时才使用。它可能覆盖：

- `~/.openclaw/openclaw.json`
- cron jobs
- workspace 文件
- live sessions

---

## 通过 OpenClaw 调用技能

你可以直接这样说：

### 备份类

- “用 clawmerge 给当前 workspace 做一次备份”
- “做一次灾难备份，包含 sessions”
- “做一次灾难备份，但不要包含 sessions”
- “先 dry-run 看看灾难备份会包含什么”

### 恢复类

- “检查这个备份包能不能恢复：/path/to/backup.tar.gz”
- “用 clawmerge 对这个备份包做 dry-run 恢复检查”
- “从这个灾难备份里安全恢复记忆和人格”
- “把 sessions 从备份里解出来，但不要合并到当前 live sessions”

### 高风险恢复类

如果涉及覆盖当前配置、启用 cron、外发消息、恢复 token、覆盖 live sessions，OpenClaw 应该先确认，不应直接执行。

示例：

> “用 clawmerge 从 `/home/admin/.openclaw/disaster-backup-2026-05-02.tar.gz` 安全恢复，重点恢复记忆和人格，不要启用定时任务。”

OpenClaw 应执行：

1. 先做当前快照
2. `tar -tzf` 检查备份结构
3. 优先恢复 `MEMORY.md`、`memory/`、`SOUL.md`、`USER.md`、`IDENTITY.md`、`AGENTS.md`
4. cron 只恢复为 disabled 或候选清单
5. 系统配置只生成候选 diff，不直接覆盖
6. 验证后写入 memory

---

## 发布前检查

ClawHub CLI v0.12.x 当前没有 `clawhub skill publish --dry-run`。发布前用这些检查替代：

```bash
bash -n skills/clawmerge/scripts/*.sh
python3 -m py_compile skills/clawmerge/scripts/*.py
bash skills/clawmerge/scripts/one-click-full-backup.sh /tmp/test.tar.gz --dry-run
bash skills/clawmerge/scripts/one-click-full-restore.sh /path/to/backup.tar.gz --dry-run
```
