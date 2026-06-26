# Changelog

本文档记录 Chat History skill 的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [3.0.0] - 2026-03-10

### 🔥 重大变更（Breaking Changes）

- **移除系统命令依赖**
  - 移除所有 `os.popen()` 和 `os.system()` 调用
  - 不再使用系统 crontab

### ✨ 新增功能

- **OpenClaw cron 集成**
  - 使用 `openclaw cron add` 替代系统 crontab
  - 完全跨平台兼容（macOS/Windows/Linux）
  - 无需任何系统权限

- **归档时间优化**
  - 默认归档时间从 03:55 改为 23:59
  - 更符合直觉（当天归档当天对话）

### 🐛 修复

- 修复 Windows 平台不兼容问题
- 修复系统权限要求问题
- 修复硬编码路径问题（已在上个版本修复）

### 🛡️ 安全改进

- 满足 OpenClaw 官方安全规范
- 通过所有安全检查
- 移除所有被标记为"系统级变更"的代码

### 📝 文档更新

- 新增 `SECURITY-NOTICE-v3.md` (v3.0 安全声明)
- 新增 `TEST-GUIDE-v3.md` (v3.0 测试指南)
- 新增 `README-v3.md` (v3.0 说明文档)

### ⚠️ 迁移说明

从 v2.0 升级到 v3.0：

```bash
# 1. 备份数据
cp -r ~/.openclaw/workspace/conversation-archives ~/.openclaw/workspace/conversation-archives-backup

# 2. 更新文件
cd ~/.openclaw/workspace/skills/chat-history
git pull

# 3. 启动新版本
python3 main_v3.py --start

# 旧版会自动停止，新版接管
```

---

## [2.0.0] - 2026-02-22

### ✨ 新增功能

- **评估记录管理**
  - 添加 `--list-evaluations` 命令
  - 添加 `--search-evaluations` 命令
  - 自动保存和搜索 skill 评估记录

- **归档格式优化**
  - Channel 端：完整对话（包括工具调用）
  - WebUI 端：纯文字（过滤工具和代码）

- **搜索功能增强**
  - 支持多关键词搜索
  - 支持日期查询
  - 支持按 channel 分类

### 🐛 修复

- 修复硬编码路径问题
- 使用环境变量动态检测路径

### 📝 文档更新

- 新增 `SECURITY-UTILITY-ASSESSMENT.md` (安全性与实用性评估)
- 新增 `TEST-GUIDE.md` (测试指南)

---

## [1.0.0] - 2026-02-14

### ✨ 新增功能

- **初始版本发布**
  - 自动归档对话记录
  - 简单搜索功能
  - 支持多个 channel
  - 基础命令系统

### 📝 文档更新

- 创建 `README.md`
- 创建 `LICENSE`
- 创建 `SKILL.md`

---

## 版本说明

| 版本 | 发布日期 | 重要程度 |
|------|---------|---------|
| v3.0.0 | 2026-03-10 | 🔥 重大更新 |
| v2.0.0 | 2026-02-22 | ✨ 功能增强 |
| v1.0.0 | 2026-02-14 | 🎯 初始版本 |

---

[3.0.0]: https://github.com/Tonyfenwick1982/chat-history/releases/tag/v3.0.0
[2.0.0]: https://github.com/Tonyfenwick1982/chat-history/releases/tag/v2.0.0
[1.0.0]: https://github.com/Tonyfenwick1982/chat-history/releases/tag/v1.0.0
