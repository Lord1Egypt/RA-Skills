# Design Digest - 发布说明

## 简介

Design Digest 是一个追踪设计工具、AI 设计动态和设计资讯的自动摘要技能，支持 OpenClaw 和 Claude Code。

## 功能特性

- ✅ 追踪 19 个精选信息源
- ✅ 每日/每周自动推送
- ✅ 双语输出（中文/英文）
- ✅ 智能去重，避免重复内容
- ✅ 零配置安装，无需 API Key
- ✅ 自动清理过期数据

## 追踪的信息源

### A 类 — 直接抓取（13 个）

**工具更新（5 个）**
- Figma Blog
- Lovable Blog
- Cursor Blog
- Framer Blog
- VS Code Updates

**AI 动态（2 个）**
- Anthropic News
- Anthropic Research

**设计系统（2 个）**
- Zeroheight Blog
- Supernova Blog

**设计深度（3 个）**
- NNGroup Articles
- Smashing Magazine
- Creativerly

**灵感发现（1 个）**
- Sidebar.io

### B 类 — 搜索补充（6 个）

- Product Hunt
- The Rundown AI
- Ben's Bites
- UX Collective
- TLDR Design
- Google Stitch

数据源列表更新频率：**按需**（用户提 issue 或发现新源时更新）

## 支持的平台

| 平台 | 状态 | 说明 |
|-------|------|------|
| OpenClaw | ✅ 推荐 | 原生支持 |
| Claude Code | ✅ 支持 | 通过 skill 目录加载 |

## 安装

### OpenClaw（推荐）

```bash
clawhub install design-daily-insights
```

### 手动安装

```bash
# Clone 到 skills 目录
git clone https://github.com/yourusername/design-digest.git \
  ~/.openclaw/workspace/skills/design-digest
```

## 快速开始

安装后，在 OpenClaw 聊天窗口输入：

```
/design
```

第一次运行会自动初始化配置和去重状态文件。

## 命令

| 命令 | 说明 |
|--------|------|
| `/design` | 手动触发摘要 |
| `/design setup` | 初始化配置 |
| `/design sources` | 查看信息源 |
| `/design add <URL>` | 添加新源 |

## 贡献指南

### 添加新数据源

1. Fork 本仓库
2. 编辑 `SKILL.md`，在"数据源"部分添加新 URL
3. 测试抓取是否正常
4. 提交 Pull Request

### 提 Issue

- **源失效**：标题格式 `[源失效] 站点名称`
- **新源建议**：标题格式 `[新源建议] 站点名称`
- **Bug 报告**：描述问题、复现步骤、错误日志

### 摘要质量优化

如需调整摘要风格，可编辑：
- `SKILL.md` - 摘要规则和输出模板
- 未来版本将支持独立的 `style.md` 配置文件

## 维护计划

### 数据源有效性检查

- **频率**：每月
- **方式**：运行一轮 web_fetch 验证，移除失效源
- **触发**：手动或自动化脚本

### 技能兼容性

- **频率**：每季度
- **方式**：跟进 OpenClaw 最新版本
- **测试**：确保 skill API 兼容

### 版本更新

- **功能更新**：按需
- **Bug 修复**：紧急时立即发布
- **数据源更新**：随 issue/PR 同步

## 路线图

- [ ] 支持更多平台（Telegram、Discord 等）
- [ ] 用户自定义摘要风格（独立 style.md）
- [ ] 更多数据源（Twitter/X、Reddit、Hacker News）
- [ ] Web UI 配置界面
- [ ] 统计分析（阅读量、热门主题）

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

感谢所有提供设计和 AI 资讯的博客、网站和社区。

---

**问题或建议？** [提交 Issue](https://github.com/yourusername/design-digest/issues)
