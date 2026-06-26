---
name: chinese-content-generator
description: 中文社交媒体内容生成器。一键生成适合掘金/知乎/公众号/小红书的文章、标题、摘要。支持热点追踪、SEO优化。
version: 1.0.0
author: OpenClaw CN
tags:
  - content
  - chinese
  - writing
  - juejin
  - zhihu
  - xiaohongshu
---

# 中文社交媒体内容生成器

专为中文内容创作者设计。一键生成适合各大平台的高质量内容，提升写作效率 10x。

## 功能

- ✍️ **多平台适配** - 掘金/知乎/公众号/小红书一键切换
- 🔥 **热点追踪** - 抓取实时热点，快速产出
- 📊 **SEO优化** - 标题/关键词自动优化
- 💡 **创意建议** - 不知道写什么？给你灵感

## 安装

```bash
npx clawhub@latest install chinese-content-generator
```

## 使用方法

### 1. 生成文章

```bash
node ~/.openclaw/skills/chinese-content-generator/generate.js --topic "DeepSeek V3 实战" --platform juejin
```

输出示例：
```
📝 标题：DeepSeek V3 实战：我用 1 块钱完成了 100 块钱的活
📊 分类：后端 / AI
🏷️ 标签：DeepSeek, AI, 降本增效

摘要（50字）：
DeepSeek V3 比GPT-4便宜100倍，我用它完成了代码生成、文档写作、数据分析等任务，真实体验分享。

正文大纲：
1. 背景：为什么尝试 DeepSeek
2. 实战：3个真实场景
   - 代码生成：重构一个 React 组件
   - 文档写作：API 文档自动生成
   - 数据分析：Excel 数据清洗
3. 成本对比：¥1 vs ¥100
4. 总结：适合什么场景

💡 建议：
- 标题加数字更吸引点击
- 开头 50 字决定打开率
- 配图建议：对比图表、代码截图
```

### 2. 抓取热点

```bash
node ~/.openclaw/skills/chinese-content-generator/trending.js
```

输出：
```
🔥 今日热点（掘金）
1. DeepSeek V3 发布 - 热度 9800
2. Claude 3.7 新功能 - 热度 7500
3. React 19 正式版 - 热度 6200
4. Tailwind CSS v4 - 热度 5400

🔥 今日热点（知乎）
1. AI 会取代程序员吗？
2. 2026 年前端方向
3. DeepSeek vs GPT-4
```

### 3. 标题优化

```bash
node ~/.openclaw/skills/chinese-content-generator/optimize-title.js "DeepSeek V3 使用教程"
```

输出：
```
📊 原标题：DeepSeek V3 使用教程
❌ 问题：太平淡，无吸引力

✅ 优化建议：
1. DeepSeek V3 教程：省下 90% API 费用（强调收益）
2. 我用 DeepSeek V3 替代了 GPT-4，真香（故事性）
3. DeepSeek V3 完整指南：从入门到精通（权威感）
4. 程序员必备：DeepSeek V3 踩坑实录（痛点）

💡 推荐选择：标题 2（故事性强，点击率高）
```

### 4. 平台适配

```bash
node ~/.openclaw/skills/chinese-content-generator/adapt.js --input article.md --platform xiaohongshu
```

自动调整：
- 标题长度（小红书 ≤ 20 字）
- 正文结构（小红书分段 + emoji）
- 标签数量（小红书 5-10 个）

## 平台特性

| 平台 | 标题长度 | 正文字数 | 特点 |
|------|----------|----------|------|
| 掘金 | ≤ 50字 | 800-3000 | 技术深度，代码示例 |
| 知乎 | ≤ 40字 | 1500-5000 | 长文，专业感 |
| 公众号 | ≤ 30字 | 1500-3000 | 标题党，开头 50 字关键 |
| 小红书 | ≤ 20字 | 500-1000 | emoji，分段，图片 |

## 实战案例

### 案例 1：技术文章（掘金）
**输入**：DeepSeek V3 体验
**输出**：
- 标题：DeepSeek V3 深度体验：比 GPT-4 便宜 100 倍，效果如何？
- 阅读量预测：5000-10000
- 推荐时间：工作日 9:00-11:00

### 案例 2：知识分享（知乎）
**输入**：AI 编程工具对比
**输出**：
- 标题：2026 年 AI 编程工具横评：Cursor、Copilot、DeepSeek 谁最强？
- 阅读量预测：10000-30000
- 推荐时间：周末 20:00-22:00

## 配置

编辑 `~/.openclaw/skills/chinese-content-generator/config.json`：

```json
{
  "default_platform": "juejin",
  "api_provider": "deepseek",
  "language": "zh-CN",
  "style": "professional",
  "max_title_length": 50
}
```

## API 提供商

支持以下 AI 模型生成内容：
- DeepSeek V3（推荐，性价比最高）
- 智谱 GLM-4（中文能力强）
- 通义千问（多模态）

---

## 💬 Pro 版本（¥199）

### 免费版（当前）
- 基础内容生成
- 平台适配
- 标题优化

### Pro 版（¥199）
- ✅ 批量生成（100+ 篇/天）
- ✅ 热点自动追踪
- ✅ 数据分析（阅读量预测）
- ✅ SEO 关键词优化
- ✅ 图片生成建议
- ✅ 1年更新支持

### 联系方式
- **QQ**: 1002378395（中国用户）
- **Telegram**: `待注册`（海外用户）

> 添加 QQ 1002378395，发送"内容生成"获取 Pro 版信息

---

## License

MIT（免费版）
Pro 版：付费后可用
