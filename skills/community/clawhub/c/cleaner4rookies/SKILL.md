---
name: openclaw-cleaner
description: OpenClaw 临时文件自动清理工具。扫描 ~/.openclaw/workspace/ 下的临时文件，按规则自动归档或删除，防止工作区膨胀。面向 ClawHub 小白用户，默认安全（dry-run）+ 自动备份归档。
---

# openclaw-cleaner 🧹

> 清理 OpenClaw 临时文件，防止工作区膨胀。默认安全，值得信赖。

## 功能

- 自动扫描 `~/.openclaw/workspace/` 下的临时文件（音频/文档/图片/日志等）
- 支持**归档**（安全移走）和**删除**两种处理方式
- **默认 dry-run**：先显示清理预览，确认后才执行
- 操作前**自动创建归档目录**，文件不会凭空消失
- 支持 **cron 定时**或**手动触发**
- 白名单机制：重要文件永不误删

## 安装

```bash
npx skills add ~/.openclaw/workspace/skills/openclaw-cleaner
```

或手动安装：

```bash
git clone https://github.com/your-repo/openclaw-cleaner.git ~/.openclaw/workspace/skills/openclaw-cleaner
```

## 快速开始

### 1. 预览（推荐先跑）

```bash
bash ~/.openclaw/workspace/skills/openclaw-cleaner/scripts/cleaner.sh
```

输出示例：

```
═══════════════════════════════════════════
  🧹 openclaw-cleaner
  模式: 🔍 dry-run（只显示，不删除）
═══════════════════════════════════════════

━━ 归档规则 ━━
  [Telegram等下载文件尽快分流] (3 个文件)
    🔍 [dry-run] doc1.docx (12K)
    🔍 [dry-run] doc2.pdf (8K)

━━ 删除规则 ━━
  [测试音频残留，无保留价值] (2 个文件)
    🔍 [dry-run] lobster-test.mp3 (128K)
```

### 2. 正式执行

加 `--force` 才真正删/归档：

```bash
bash ~/.openclaw/workspace/skills/openclaw-cleaner/scripts/cleaner.sh --force
```

## 配置

编辑 `~/.openclaw/workspace/cleaner.yaml`（不存在则自动使用内置 `config.yaml`）：

```yaml
# 清理规则
rules:
  - pattern: "*.mp3 *.wav *.m4a"
    action: delete
    age_days: 0          # 0 = 立即

  - pattern: "*.docx *.doc *.pdf"
    action: archive       # 移到归档目录
    age_days: 1           # 超过1天触发

  - pattern: "*.png *.jpg *.gif"
    action: delete
    age_days: 7           # 超过7天触发

  - pattern: "media/inbound/*"
    action: archive
    age_days: 3

# 执行控制
dry_run: true             # 默认预览，要关闭设为 false
archive_dir: "~/.openclaw/workspace/cleaner-archive"
cron_schedule: ""         # 填 "0 3 * * *" = 每天凌晨3点

# 白名单（绝对路径，不会被删除）
whitelist:
  - "~/.openclaw/workspace/SOUL.md"
  - "~/.openclaw/workspace/MEMORY.md"
```

## cron 定时任务

在 `cleaner.yaml` 里填入 cron 表达式：

```yaml
cron_schedule: "0 3 * * *"   # 每天凌晨3点
```

或手动通过 OpenClaw cron 管理：

```
cron add --name "openclaw-cleaner" \
  --schedule "0 3 * * *" \
  --command "bash ~/.openclaw/workspace/skills/openclaw-cleaner/scripts/cleaner.sh --force"
```

> ⚠️ **强烈建议**：首次用 cron 前，先手动跑一次 dry-run，确认规则符合预期。

## 安全特性

| 特性 | 说明 |
|------|------|
| 默认 dry-run | 永远先显示预览，不直接操作 |
| 自动归档 | 删除改为归档到 `cleaner-archive/`，可恢复 |
| 白名单 | 显式声明的文件永不删除 |
| 详细日志 | 记录每个文件的处理结果 |

## 卸载

```bash
rm -rf ~/.openclaw/workspace/skills/openclaw-cleaner
rm -rf ~/.openclaw/workspace/cleaner-archive
# 如有 cron，手动删除对应的 cron job
```

## 故障排除

| 问题 | 解法 |
|------|------|
| "未找到配置文件" | 确认 `~/.openclaw/workspace/cleaner.yaml` 或 `config.yaml` 存在 |
| 想恢复归档的文件 | 去 `~/.openclaw/workspace/cleaner-archive/` 找 |
| 某些文件不该删 | 加入 `whitelist` 列表 |
| dry-run 显示 0 个文件 | 说明没有符合条件（时间阈值未到）的文件 |

## 更新日志

### v1.0.0
- 首发：支持归档/删除、白名单、dry-run、cron 定时
