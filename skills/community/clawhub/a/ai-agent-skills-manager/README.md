# 🦞 AI Agent Skills Manager

智能体技能安装管理工具 - 推广版

## 简介

这是一个用于安装和管理 OpenClaw AI Agent 技能的工具。基于 [pskoett/pskoett-ai-skills](https://github.com/pskoett/pskoett-ai-skills) 项目，提供交互式技能选择和批量安装功能。

## 核心功能

- ✅ 交互式技能选择 - 图形化界面选择要安装的技能
- ✅ 批量安装 - 一次选择多个技能
- ✅ 自动克隆 - 自动从 GitHub 克隆源仓库
- ✅ 进度跟踪 - 显示安装进度和日志
- ✅ 易于推广 - 适合分享给其他开发者

## 快速开始

### 1. 运行安装器

```bash
cd ~/Desktop
./skill-installer.sh
```

### 2. 选择技能

在交互界面中：
- 按空格键选择/取消技能
- Enter 确认选择
- q 退出

### 3. 查看已安装技能

```bash
ls ~/.openclaw/skills/
```

## 技能说明

| 技能 | 作用 | 适用场景 |
|------|------|----------|
| `self-improvement` | 记录错误和学习经验 | 所有任务 |
| `simplify-and-harden` | 代码质量审查 | 中等以上复杂度任务 |
| `plan-interview` | 需求访谈 | 新功能、重构 |
| `intent-framed-agent` | 范围监控 | 多文件任务 |
| `context-surfing` | 上下文监控 | 长期任务 |

## 推广建议

### 分发方式

1. **直接分享**
   ```bash
   # 发送脚本文件
   scp ~/Desktop/skill-installer.sh user@remote:/tmp/
   ```

2. **创建安装包**
   ```bash
   # 创建 deb 包
   debuild -us -uc
   ```

3. **发布到包管理器**
   ```bash
   npm install ai-agent-skills-manager
   ```

### 文档完善

- [x] 安装说明
- [x] 使用指南
- [ ] 视频教程
- [ ] 故障排除

### 社区推广

- GitHub 仓库
- 技术博客
- 社区分享
- 会议演讲

## 技术支持

遇到问题？查看日志：

```bash
cat ~/.ai_agent_skills/install.log
```

## 许可证

MIT - 自由使用、修改和分发

---

Made with ❤️ by OpenClaw Assistant
