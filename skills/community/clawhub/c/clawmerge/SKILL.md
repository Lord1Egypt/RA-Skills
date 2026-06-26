---
name: clawmerge
version: 4.0.2
description: |
  OpenClaw workspace 备份/恢复/合并工具。
  支持：完整备份、合并恢复（不覆盖已有）、Cron 任务备份、会话记录备份、配置导出。
  新增：灾难备份包含系统配置 + workspace + sessions；恢复默认安全合并，避免误覆盖运行配置。
  触发词：「备份」「恢复」「迁移」「换电脑」「导出配置」「合并记忆」「灾难备份」。
  当 workspace 需要迁移、定期备份、或从另一台设备恢复时使用。
---

# Clawmerge - Workspace 备份/恢复工具

> 换电脑不丢记忆，恢复默认不覆盖重要文件。

---

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

## 功能概览

| 功能 | 说明 |
|-----|------|
| **工作区备份** | 备份 workspace（脚本、配置、记忆） |
| **灾难备份** | 备份 workspace + 系统配置 + sessions，重装系统后一键恢复 |
| **合并恢复** | 解压时不覆盖已有文件，适合从另一台设备增量恢复 |
| **Cron 备份** | 自动备份 cron 任务配置 |
| **会话备份** | 可选包含会话记录（.jsonl） |
| **配置导出** | 导出脱敏后的公开配置 |

---

## 使用场景

### 场景 1：定期工作区备份（手动）
```bash
cd ~/.openclaw/workspace
./skills/clawmerge/scripts/one-click-backup.sh /tmp/backup-$(date +%Y%m%d).tar.gz
```

### 场景 2：灾难备份（重装系统前/中/后）
```bash
# 创建灾难备份（包含 workspace + 系统配置 + sessions）
./scripts/one-click-full-backup.sh ~/openclaw-disaster-backup.tar.gz

# 排除 sessions（减小体积）
./scripts/one-click-full-backup.sh ~/openclaw-disaster-backup.tar.gz --no-sessions

# 重装系统后一键安全恢复（默认：配置/cron/sessions 先归档候选，不覆盖 live）
./scripts/one-click-full-restore.sh ~/openclaw-disaster-backup.tar.gz

# 仅在你明确要完全覆盖旧环境时使用危险模式
./scripts/one-click-full-restore.sh ~/openclaw-disaster-backup.tar.gz --unsafe-overwrite
```

### 场景 3：换电脑后恢复（合并模式）
```bash
./skills/clawmerge/scripts/one-click-restore.sh /path/to/backup.tar.gz --merge
```

### 场景 4：查看备份内容（不解压）
```bash
tar -tzf backup.tar.gz | head -50
```

### 场景 5：只备份 Cron 任务
```bash
./skills/clawmerge/scripts/backup-cron-tasks.sh
```

---

## 灾难备份详解

### 包含内容

| 内容 | 说明 |
|-----|------|
| `system/openclaw.json` | Gateway 配置（含 token） |
| `system/.env` | 环境变量 |
| `agents/main/agent/` | Agent 认证配置 |
| `cron/jobs.json` | 定时任务定义 |
| `cron/jobs-state.json` | Cron 状态 |
| `workspace.tar.gz` | 完整 workspace（48MB） |
| `sessions.tar.gz` | 对话记录（压缩后约 50MB） |

### 大小参考

```
当前环境（2026-05-02）：
  workspace:    ~50MB
  sessions:     261MB → 压缩后 ~50MB
  系统配置:     <1MB
  -------------------
  总计:         ~103MB（含 sessions）
```

### 恢复流程

1. **备份文件上传到云端/NAS**（重装系统前）
2. **重装系统，安装 OpenClaw**
3. **恢复备份：**
   ```bash
   bash ~/.openclaw/workspace/skills/clawmerge/scripts/one-click-full-restore.sh ~/openclaw-disaster-backup.tar.gz
   ```
   默认安全模式会：
   - 将 `openclaw.json`、`.env`、cron、agent auth 放到 `~/.openclaw/restore-candidates/<timestamp>/`
   - 将 sessions 解压到 `~/.openclaw/agents/main/sessions-restored-<timestamp>/`
   - workspace 解压时跳过已有文件，避免覆盖当前记忆/人格

   如需旧版全覆盖行为，显式加 `--unsafe-overwrite`。
4. **重启 Gateway：**
   ```bash
   openclaw gateway restart
   ```

---

## 脚本清单

| 脚本 | 用途 |
|-----|------|
| `one-click-backup.sh` | 备份 workspace（不含系统配置） |
| `one-click-restore.sh` | 恢复 workspace（支持 --merge） |
| `one-click-full-backup.sh` | **灾难备份**（workspace + 系统配置 + sessions） |
| `one-click-full-restore.sh` | **灾难恢复**（一键恢复所有配置） |
| `backup-cron-tasks.sh` | 单独备份 cron 配置 |
| `restore-cron-tasks.sh` | 恢复 cron 配置 |
| `discover-scripts.py` | 扫描 workspace 中的自定义脚本 |
| `gen-requirements.py` | 生成 requirements.txt |
| `post-restore-check.sh` | 恢复后检查完整性 |
| `workspace-manager.sh` | workspace 空间管理（查看大小/清理） |

---

## 备份排除规则

以下文件默认排除（不备份）：

| 排除 | 原因 |
|-----|------|
| `*.pyc` | 编译缓存 |
| `__pycache__/` | Python 缓存 |
| `.session/` | 临时会话 |
| `node_modules/` | npm 包（可从 package.json 恢复） |
| `*.log` | 日志文件 |
| `.git` | Git 历史 |

---

## 合并恢复逻辑（--merge）

```bash
# 合并模式：遇到同名文件
# - 若原文件与备份不同 → 保留原文件（不覆盖）
# - 若原文件不存在 → 从备份解压
# - 备份中有、原文件没有 → 恢复
```

**使用 --merge 的场景**：
- 从另一台设备的备份恢复（避免覆盖本机已有的配置）
- 合并两台设备的工作成果

---

## Dry Run / 发布安全说明

```bash
# 灾难备份预览
./scripts/one-click-full-backup.sh --dry-run /tmp/test.tar.gz

# 灾难恢复预览
./scripts/one-click-full-restore.sh ~/openclaw-disaster-backup.tar.gz --dry-run

# 工作区备份预览
./one-click-backup.sh --dry-run /tmp/test.tar.gz
```

ClawHub CLI `clawhub skill publish` 在 v0.12.x 暂不支持 `--dry-run`。发布前请用本地校验替代：

```bash
bash -n skills/clawmerge/scripts/*.sh
python3 -m py_compile skills/clawmerge/scripts/*.py
clawhub inspect clawmerge --json  # 若已发布，用于发布后验证
```

不要在文档或自动流程里声称 `clawhub skill publish --dry-run` 可用。

---

## 输出物

| 文件 | 说明 |
|-----|------|
| `backup.tar.gz` | 主备份文件 |
| `MANIFEST.txt` | 备份内容清单（灾难备份） |
| `restore-report.txt` | 恢复报告 |

---

## 故障处理

| 问题 | 解决方案 |
|-----|---------|
| 备份文件过大 | 使用 `--no-sessions` 排除 sessions |
| 恢复失败 | 检查 `.tar.gz` 是否损坏；尝试 `tar -tzf` 验证 |
| Cron 未恢复 | 手动运行 `restore-cron-tasks.sh` |
| sessions 恢复失败 | 重启后 sessions 会自动重建空目录 |

---

## 依赖

- `bash`
- `tar`
- `python3`（用于 discover-scripts.py 和 gen-requirements.py）

---

*备份不是为了恢复，是为了放心地往前走。* 📦