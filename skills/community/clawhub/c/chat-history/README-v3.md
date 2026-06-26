# Chat History - OpenClaw对话归档系统

**作者**: Tonyfenwick1982
**版本**: v3.0
**分类**: 生产力工具 / AI辅助
**平台**: OpenClaw（macOS/Windows/Linux）
**许可证**: MIT

**联系方式**: tonyfenwick881412@gmail.com

---

## 🛡️ 安全性声明

> ✅ **v3.0 已完全符合 OpenClaw 官方安全规范**

**VirusTotal报告无法获取？**
- 这是ClawHub平台的显示问题
- 完整的安全评估报告：[SECURITY-NOTICE-v3.md](SECURITY-NOTICE-v3.md)

**v3.0 安全改进**：
- ✅ 移除所有系统命令（os.popen, os.system）
- ✅ 使用 OpenClaw 原生 cron API
- ✅ 完全跨平台兼容（macOS/Windows/Linux）
- ✅ 无需任何系统权限

详细安全报告：[SECURITY-NOTICE-v3.md](SECURITY-NOTICE-v3.md)

---

## 📖 简介

Chat History是一个OpenClaw对话归档系统，帮助你自动归档和搜索对话记录。

### 核心特性

- ✅ **自动归档**：每天23:59自动归档（可自定义时间）
- ✅ **增量归档**：只归档上次归档后的新消息
- ✅ **多Channel支持**：自动识别所有channel
- ✅ **跨端查询**：无论在哪端，都能查询所有对话
- ✅ **自然语言触发**：30+关键词
- ✅ **评估记录管理**：列出/搜索评估

### v3.0 重大更新

- 🔥 **跨平台兼容**：使用 OpenClaw cron，支持 Windows/macOS/Linux
- 🔥 **无需系统权限**：不使用 crontab 或系统命令
- 🔥 **归档时间优化**：改为 23:59，符合直觉
- 🔥 **官方信赖**：满足 OpenClaw 安全规范

---

## 🚀 快速开始

### 安装

**步骤1**：复制skill到OpenClaw skills目录
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Tonyfenwick1982/chat-history.git
# 或手动复制chat-history文件夹
```

**步骤2**：进入skill目录并启动
```bash
cd ~/.openclaw/workspace/skills/chat-history
python3 main_v3.py --start
```

系统会自动设置 OpenClaw 定时任务，每天23:59归档对话。

---

### 使用

#### 基础命令
```
--help / -h         显示帮助
--archive           执行归档
--status            查看归档状态
--start             启动自动归档
--stop              停止自动归档
--timing            查看或设置归档时间
--keyword           列出触发关键词
```

#### 自然语言触发（最方便）

```
用户: 我想不起来了，之前说过关于视频的事
→ 自动搜索"视频"并显示结果

用户: 我之前评估过哪些skills
→ 自动列出评估记录
```

---

## 🔄 v2.0 → v3.0 升级指南

```bash
# 1. 备份现有数据
cp -r ~/.openclaw/workspace/conversation-archives ~/.openclaw/workspace/conversation-archives-backup

# 2. 更新文件
cd ~/.openclaw/workspace/skills/chat-history
git pull  # 或手动替换文件

# 3. 测试新版本
python3 main_v3.py --status
python3 main_v3.py --start

# 完成！新版自动接管
```

---

## 🛡️ 安全性

**安全承诺**：
- ✅ 无系统命令执行
- ✅ 无网络请求（纯本地操作）
- ✅ 无硬编码API keys
- ✅ 无上传数据到服务器

**依赖项**：
- Python 3.x
- OpenClaw CLI（用于定时任务）
- 所有依赖项为Python标准库（无第三方依赖）

---

## 📚 文档

- [v3.0 安全声明](SECURITY-NOTICE-v3.md) - v3.0 安全改进说明
- [v3.0 测试指南](TEST-GUIDE-v3.md) - 完整测试流程
- [v2.0 安全性评估](SECURITY-UTILITY-ASSESSMENT.md) - 原安全评估（仅供参考）

---

## 🎯 平台支持

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| macOS | ✅ 完全支持 | 使用 OpenClaw cron |
| Windows | ✅ 完全支持 | 使用 OpenClaw cron |
| Linux | ✅ 完全支持 | 使用 OpenClaw cron |

---

## 📞 联系方式

- Author: Tonyfenwick1982
- GitHub: https://github.com/Tonyfenwick1982
- Email: tonyfenwick881412@gmail.com

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

---

## ⚠️ 免责声明

本工具仅用于管理和搜索用户自己的对话记录，不涉及任何隐私泄露或数据传输。所有数据存储在本地，安全可控。

---

## 📋 更新日志

### v3.0 (2026-03-10)
- 🔥 移除所有系统命令（os.popen, os.system）
- 🔥 使用 OpenClaw cron 替代系统 crontab
- 🔥 完全跨平台兼容（macOS/Windows/Linux）
- 🔥 归档时间改为 23:59
- ✅ 满足 OpenClaw 官方安全规范

### v2.0 (2026-02-22)
- 添加评估记录管理功能
- 优化自然语言触发
- 添加详细的搜索和归档功能

### v1.0 (2026-02-14)
- 初始版本发布
*最后更新：2026-03-10*
