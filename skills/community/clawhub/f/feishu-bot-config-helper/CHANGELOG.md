# 📝 更新日志

## v1.0.0 (2026-03-17)

**核心功能**:
- ✅ 飞书机器人自动配置系统
- ✅ 在飞书对话中直接配置新机器人
- ✅ 智能匹配 Agent（7 种规则）
- ✅ 自动更新 openclaw.json
- ✅ 自动重启 Gateway

**智能匹配规则**:
| 关键词 | Agent ID |
|--------|---------|
| 笔记/笔记虾/第二大脑 | notes |
| 内容/创作/通用 | generic_content |
| 朋友圈/社交 | moment |
| 视频/导演 | video |
| Seedance/提示词 | seedance |
| 图片/设计 | image |
| 工作/助手 | work |

**配置规范**:
- 每个飞书机器人对应一个独立 Agent
- 拥有独立的工作空间和记忆
- dmScope: per-account-channel-peer
- groupPolicy: open

**核心文件**:
- scripts/auto-configure-bot.js - 自动配置脚本
- index.js - 主入口
- install.sh / install.bat - 安装脚本
- package.json - 项目配置

---
