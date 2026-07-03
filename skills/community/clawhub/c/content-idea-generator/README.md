# Content Idea Generator

> 选题生成器 — 基于热点话题和用户偏好自动生成视频 / 图文选题

[![Skill Version](https://img.shields.io/badge/Skill%20Version-2026.06-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#)

## 截图预览

> 以下截图展示典型选题库输出效果，实际内容由 AI 根据当日热点动态生成。

| 选题列表 | 详细选题卡片 | 选题统计概览 |
|:---:|:---:|:---:|
| 平台 × 标题 × 预期热度 | 角度分析 + 脚本大纲 | TOP10 + 趋势分布 |

## 功能亮点

## 功能亮点

- ✅ **自动抓取热点** - 整合抖音、小红书、知乎、微博等平台热点
- ✅ **智能生成选题** - AI分析热点+用户偏好，生成高质量选题
- ✅ **多平台适配** - 支持抖音、小红书、B站、知乎等平台风格
- ✅ **批量生成** - 一次生成10-100个选题

## 使用场景

- 内容创作者每天找选题
- 营销团队需要内容规划
- 自媒体运营需要批量生产内容
- 企业需要做内容营销

## 安装方法

1. 下载 `content-idea-generator.skill` 文件
2. 在QClaw中安装：`Skills` → `Install Skill` → 选择文件
3. 重启QClaw Gateway
4. 开始使用！

## 使用方法

### 基础用法

```
帮我生成今天的视频选题，领域是AI工具测评
```

### 高级用法

```
使用content-idea-generator技能，生成一周的选题：
- 领域：科技数码
- 数量：7天 × 3个/天 = 21个
- 平台：抖音+小红书
- 保存到腾讯文档
```

## 工作流程

1. **抓取热点话题** - 自动抓取各平台今日热点
2. **分析用户偏好** - 分析历史表现和受众画像
3. **生成选题** - 结合热点和偏好，生成选题列表
4. **保存选题库** - 输出到本地/腾讯文档/Excel

## 选题示例

```json
{
  "title": "2026年最值得用的5个AI工具",
  "angle": "测评+干货",
  "platform": "douyin",
  "expected_views": "10万+",
  "difficulty": "中等",
  "reason": "AI工具是持续热点，测评类内容受欢迎"
}
```

## 定时自动化

配合 `qclaw-cron-skill` 实现每日自动生成选题：

```json
{
  "name": "每日选题生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "使用 content-idea-generator 技能，基于今日热点生成10个选题"
  }
}
```

## 与其他Skill配合

### + video-auto-generator

```
选题生成 → 视频生成 → 自动发布
```

### + hot-topic-tracker

```
热点追踪 → 选题生成 → 人工审核 → 执行
```

## 安装方法

### 方式一：SkillHub 在线安装（推荐）

```bash
skillhub install content-idea-generator
```

### 方式二：本地 Zip 安装

```bash
skillhub install /path/to/content-idea-generator-x.x.x.zip
```

### 方式三：手动安装

1. 下载 Skill 包，解压到 `~/.qclaw/skills/content-idea-generator/`
2. 重启 QClaw Gateway
3. 开始使用！

## 依赖说明

| 依赖 | 版本要求 | 用途 | 必选 |
|------|---------|------|------|
| Python | 3.8+ | 运行环境 | 必选 |
| web_search | 已内置 | 热点数据获取 | 必选 |
| hot-topic-tracker | 可选 | 深度热点追踪 | 可选 |
| 当前平台模型 | — | 选题生成（model route 自动选择） | 必选 |
| tencent-docs | 可选 | 在线文档保存 | 可选 |

## 常见问题

## 变现路径

### 方案A：在ClawHub上销售此Skill

- 基础版：99元（每日10个选题）
- 专业版：299元（无限选题 + 竞品分析）
- 企业版：999元（API接口 + 定制开发）

### 方案B：提供选题策划服务

- 按月订阅：199元/月（每日提供选题）
- 按选题收费：9.9元/个
- 全案策划：999元/月（选题+脚本+发布）

## 常见问题

**Q: 生成的选题质量如何？**
A: 基于热点数据和算法推荐，质量较高，但建议人工审核。

**Q: 可以指定平台风格吗？**
A: 可以，支持抖音、小红书、B站、知乎等平台。

**Q: 如何保存选题库？**
A: 支持本地Markdown、腾讯文档、Excel等多种格式。

## 更新日志

### v1.0 (2026-06-12)

- 支持基础选题生成
- 支持多平台风格

## 联系方式

- 作者：QClaw AI
- 支持：在QClaw中留言

---

### v1.1.0 (2026-06-14)

- 移除所有硬编码 AI 模型名，统一由 model route 自动选择
- 补充完整功能说明、使用示例、配置示例
- 新增 README.md（ClawHub 发布标准）

### v1.0.0 (2026-06-12)

- 初始版本
- 支持基础选题生成
- 支持多平台风格

## 许可证

MIT License

## 联系方式

- QClaw 官方支持
- ClawHub：https://clawhub.ai/skills/content-idea-generator

---

**立即安装，告别选题困难症！** 🚀
