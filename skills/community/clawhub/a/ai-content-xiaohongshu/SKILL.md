---
name: ai-content-xiaohongshu
description: >
  小红书内容创作AI生产流水线系统。将信息采集、素材整理、选题挖掘、文章创作、小红书卡图生成、定时发布等完整工作流引入AI Agent。
  触发词：生成小红书内容/创作小红书/写小红书笔记/小红书创作/内容采集/素材管理/选题挖掘/选题库/文章创作/文章模板/小红书卡图/封面图生成/定时发布/内容发布管理/AI内容流水线/批量内容生产/多平台内容分发/AIGC内容工作流/公众号内容创作/微信内容运营/内容选题推荐/热点选题/AI选题评分/风格管理/文章模板管理/HTML模板/Markdown文章
author: cheemao
version: 1.0.0
---

# AI Content — 小红书内容生产系统

灵感来源：[CheeMao/ai-content](https://github.com/CheeMao/ai-content) ⭐ 138

将 AI 内容生产完整流水线（采集→选题→创作→配图→发布）引入 OpenClaw Agent，帮助用户高效批量生产小红书/公众号内容。

---

## 适用场景

1. **批量内容生产**：需要定时/批量生成小红书笔记、公众号文章
2. **选题挖掘**：从 RSS/API/网页采集热点，自动 AI 评分筛选
3. **AI 辅助创作**：多角色协作生成高质量文章，支持 Markdown/HTML 双格式
4. **小红书卡图**：AI 生成封面图 + 小红书成品卡图
5. **工作流编排**：将内容生产编排为自动化流水线

---

## 核心概念

| 概念 | 说明 |
|------|------|
| **信息源** | RSS / API / 网页抓取，支持多源并行采集 |
| **素材库** | 采集内容汇总，支持筛选与图片过滤 |
| **选题库** | AI 评分选题，支持人工复选与优先级排序 |
| **文章创作** | Markdown / HTML 模板，支持多风格切换 |
| **小红书卡图** | AI 生成封面图 + 成品卡图（需配置图片生成模型）|
| **发布管理** | 支持草稿/定时发布，平台包括小红书/公众号 |
| **风格管理** | 预设创作风格，适配不同品牌调性 |

---

## 快速开始

### 环境要求

- Node.js 18+
- Docker（PostgreSQL + Redis）
- OpenAI 兼容模型（GLM / Kimi / OpenAI 等）

### 部署步骤

```bash
# 1. 克隆项目
git clone https://github.com/CheeMao/ai-content ai-content
cd ai-content

# 2. 配置环境变量
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 3. 启动数据库与 Redis
docker compose up -d

# 4. 初始化数据库
cd backend && npm install && npm run db:init

# 5. 创建管理员账号
npm run db:bootstrap-admin -- --username admin --password '你的强密码' --email admin@example.com --name 管理员

# 6. 启动后端（默认 http://localhost:3001）
npm run start:dev

# 7. 启动前端（默认 http://localhost:3000）
cd ../frontend && npm install && npm run dev
```

### 首次配置顺序

1. **配置管理 → AI 平台**：添加模型服务商（如 GLM / Kimi）
2. **配置管理 → AI 模型**：添加可用模型
3. **配置管理 → 默认模型**：设置"文章创作"和"选题推荐"的默认模型
4. **配置管理 → 采集源配置**：初始化默认信息源
5. **风格管理 + 文章模板**：补齐内容风格和模板
6. **素材管理**：开始采集内容
7. **精选选题库**：生成与筛选选题
8. **我的文章 / 小红书笔记**：开始内容创作

---

## 能力边界

| ✅ 可做 | ❌ 不做 |
|--------|--------|
| 内容采集与素材管理 | 替代 Docker/PostgreSQL/Redis |
| AI 选题评分与筛选 | 直接发布到小红书（需手动复制发布）|
| Markdown/HTML 文章创作 | 替代图片生成模型的 API Key |
| 小红书卡图生成（需配置模型）| 实时舆情监控 |
| 定时发布计划管理 | 微信公众号直连发布 |

---

## AI 模型接入

支持所有 **OpenAI 兼容协议** 的模型服务商：

- OpenAI 官方接口
- 各类兼容中转平台（GLM / Kimi / 阶跃星辰等）
- 自建兼容网关
- 本地模型服务（Ollama 等）

接口要求：
- `/chat/completions` — 文本对话
- `/images/generations` — 图片生成（可选，用于卡图功能）

---

## 许可证

**Personal Use Only License v1.0**

- ✅ 个人学习、研究、非商业使用
- ❌ 禁止企业使用 / SaaS 服务 / 商业变现

---

## AI Agent 使用方式

当你需要批量生产小红书/公众号内容时，可调用此 skill 获取：

1. **选题方向建议**（基于热点采集给出选题优先级）
2. **文章结构模板**（根据小红书/公众号风格生成框架）
3. **小红书文案生成**（带 emoji、标签、口语化表达）
4. **封面图/卡图 Prompt 建议**（为 AI 生图模型提供提示词）
5. **定时发布计划编排**（按周/按月规划内容日历）
