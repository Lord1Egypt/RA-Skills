---
name: ai-agent-skills-manager
description: "AI Agent Skills Manager - 智能体技能管理工具。安装和管理 OpenClaw 技能包，提供交互式选择界面。Use when: (1) User wants to install AI agent skills, (2) User needs to manage OpenClaw skills, (3) User wants to promote this tool for distribution."
metadata:
  version: "1.0.1"
  author: "OpenClaw Assistant"
  category: "Tool Management"
  priority: "High"
  updated: "2026-03-28 - 修复安全漏洞（移除 GIT_SSL_NO_VERIFY）"
---

# 🦞 AI Agent Skills Manager

智能体技能安装管理工具 - 推广版

## 简介

这是一个用于安装和管理 OpenClaw AI Agent 技能的工具。基于 [pskoett/pskoett-ai-skills](https://github.com/pskoett/pskoett-ai-skills) 项目，提供交互式技能选择和批量安装功能。

## 核心功能

- ✅ **交互式技能选择** - 图形化界面选择要安装的技能
- ✅ **批量安装** - 一次选择多个技能
- ✅ **自动克隆** - 自动从 GitHub 克隆源仓库
- ✅ **进度跟踪** - 显示安装进度和日志
- ✅ **易于推广** - 适合分享给其他开发者

## 技能列表

| 技能 | 作用 |
|------|------|
| `self-improvement` | 自我改进，记录错误和学习经验 |
| `simplify-and-harden` | 任务完成后代码质量审查和安全加固 |
| `plan-interview` | 实施前结构化需求访谈 |
| `intent-framed-agent` | 执行范围监控 |
| `context-surfing` | 上下文质量监控 |

## 安装

### 方法 1: 桌面运行

```bash
cd ~/Desktop
./skill-installer.sh
```

### 方法 2: 系统安装

```bash
sudo cp ~/Desktop/skill-installer.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/skill-installer
skill-installer
```

### 方法 3: 直接克隆

```bash
# 克隆源仓库
git clone https://github.com/pskoett/pskoett-ai-skills.git /tmp/pskoett-ai-skills

# 手动安装技能
cp -r /tmp/pskoett-ai-skills/skills/simplify-and-harden ~/.openclaw/skills/
cp -r /tmp/pskoett-ai-skills/skills/plan-interview ~/.openclaw/skills/
cp -r /tmp/pskoett-ai-skills/skills/intent-framed-agent ~/.openclaw/skills/
cp -r /tmp/pskoett-ai-skills/skills/context-surfing ~/.openclaw/skills/
cp -r /tmp/pskoett-ai-skills/skills/self-improvement ~/.openclaw/skills/
```

## 使用

运行安装脚本：

```bash
./skill-installer.sh
```

在界面中选择要安装的技能（可多选），回车确认即可。

## 推广建议

### 1. 创建项目主页

- GitHub 仓库
- README 文档
- 安装说明
- 使用示例

### 2. 分发方式

- 直接分享脚本文件
- 创建 deb/rpm 包
- 发布到 npm 或其他包管理器
- 在技术社区分享

### 3. 文档完善

- 技能说明文档
- 最佳实践指南
- 故障排除手册
- 视频教程

### 4. 社区建设

- 收集用户反馈
- 添加更多技能
- 持续维护更新
- 鼓励贡献

## 技术栈

- **Shell Script** - 安装逻辑
- **Bash Colors** - 界面美化
- **Git** - 版本控制
- **OpenClaw** - AI Agent 平台

## 许可证

MIT License - 自由使用、修改和分发

## 贡献

欢迎贡献：

1. Fork 此工具
2. 创建特性分支
3. 提交 Pull Request

## 相关链接

- [源项目](https://github.com/pskoett/pskoett-ai-skills)
- [Agent Skills 规范](https://agentskills.io/specification)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

## 作者

Created by OpenClaw Assistant - 2026

## 版本历史

### v1.0.0 (2026-03-28)
- 初始版本
- 支持 5 个核心技能
- 交互式选择界面
- 推广功能

---

**提示**: 将此工具分享给更多开发者，帮助推广 AI Agent 最佳实践！🚀
