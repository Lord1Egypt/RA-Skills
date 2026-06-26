# Changelog - context-memory-manager

## v1.2.0 (2026-04-14)

### 🔄 架构重构
- **核心机制改为 `session_status` 检测**：每次被唤醒时自动检查上下文使用率，不再依赖磁盘文件大小判断
- **移除 `monitor_context.py`**：扫磁盘 KB 大小无法反映真实上下文使用量
- **压缩前先保存完整对话**：`sessions_history` → `memory/chat/`（不裁剪），再提炼项目记忆

### ✨ 新功能
- 唤醒时自动检查流程：
  1. `session_status` → 上下文 ≥ 70% 执行压缩
  2. 保存完整对话到 `memory/chat/YYYY-MM-DD.md`
  3. 提炼项目记忆 → `memory/projects/<项目名>/`
  4. 更新 `MEMORY.md`
- 新增首次安装引导：Agent 自动设置 crontab 复盘任务

### 🗑️ 移除
- `monitor_context.py` 脚本（无意义的磁盘大小扫描）
- crontab 中的每 2 小时监控任务
- `--auto-truncate` 自动裁剪功能（不应丢弃用户对话）

### 📝 文档
- SKILL.md 完全重写，以 `session_status` 为核心
- 架构说明图更新为两步流程（Compress + Review）

---

## v1.1.0 (2026-04-14)

### 🐛 Bug 修复
- 修复 `daily_review.py` 增量过滤的时区比较报错（naive vs aware datetime）
- 修复 `.last_review` 时间戳写入失败问题

### ✨ 新功能
- cron 报告持久化到 `/tmp/cmm_review_report.json`
- Agent 唤醒时自动检查并处理积压报告

---

## v1.0.0 (2026-04-13)

### 首次发布
- 多 Agent 上下文监控 + 智能压缩 + 每日复盘
- cron 每 2 小时扫描 memory 文件磁盘占用
- cron 每天凌晨 3 点增量复盘
- 自动归档旧文件（默认 30 天）
