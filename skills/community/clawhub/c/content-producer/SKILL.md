---
name: content-producer-v1
description: 多平台内容分发器 v1.0。一次输入，自动适配小红书/知乎/公众号/抖音四种平台格式，直接输出可发布内容。
version: 1.0.0
tags: [content, writing, social-media, copywriting, chinese, xiaohongshu, zhihu, wechat, douyin]
author: AI Skill 商业生产
price: ¥29.9
---

# 📝 多平台内容分发器 v1.0 (付费版)

## 一句话卖点

> **写一篇内容，自动适配4个平台。不用再为每个平台重写一遍。**

## 核心能力

1. **多平台适配** — 小红书/知乎/公众号/抖音，一次输入四端输出
2. **平台原生格式** — 每个平台的内容规范、语气、结构自动匹配
3. **批量生成** — 一条主题，所有平台全覆盖
4. **历史管理** — 已生成内容自动存档，可随时查看和复用
5. **OpenAI驱动** — 默认用 gpt-4o-mini，便宜够用（可换其他兼容API）

## 使用方式

### 生成指定平台

```bash
python3 content_producer.py --topic "2026年AI工具推荐" --platform xiaohongshu
```

### 一键生成全部平台

```bash
python3 content_producer.py --topic "普通人如何用AI副业赚钱" --platform all
```

### 带要点

```bash
python3 content_producer.py \
  --topic "为什么程序员需要学AI" \
  --points "AI不是取代,涨薪30%,现在入局最佳" \
  --platform all
```

### 查看历史

```bash
python3 content_producer.py --topic "" --history
```

## 输出示例

```
content_output/20260425/
├── [小红书] AI工具推荐_20260425_143000.md
├── [知乎] AI工具推荐_20260425_143005.md
├── [公众号] AI工具推荐_20260425_143010.md
└── [抖音] AI工具推荐_20260425_143015.md
```

## 平台对照

| 平台 | 字数 | 风格 | 适合 |
|------|------|------|------|
| 小红书 | 300-800字 | 口语化、emoji | 种草/测评/攻略 |
| 知乎 | 1000-2000字 | 专业、数据支撑 | 干货回答/分析 |
| 公众号 | 1500-3000字 | 深度、故事感 | 深度文章/洞察 |
| 抖音 | 200-500字 | 节奏快、钩子强 | 口播脚本/带货 |

## 环境要求

- Python 3.8+
- OpenAI API Key (或兼容API)
- `pip install requests`

## 配置

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_MODEL="gpt-4o-mini"  # 可选，默认即可
export CONTENT_OUTPUT_DIR="./content_output"  # 输出目录
```

---

## 上架物料

### 卖点文案 (朋友圈)

> **还在为每个平台重写一遍内容？**
>
> 写一篇小红书、改一篇知乎、再写一篇公众号…
> 一个主题写4遍，太浪费时间了。
>
> 📝 这个工具，一次输入，四个平台自动输出
> ✅ 小红书 → 种草笔记直接发
> ✅ 知乎 → 高赞回答格式
> ✅ 公众号 → 深度文章
> ✅ 抖音 → 口播脚本
>
> 写一篇 = 发四个平台
> 29.9，永久使用，后续更新免费
> 👇 想矩阵输出的，上车

### 关键词标签

`内容生成` `自媒体` `多平台分发` `小红书笔记` `知乎回答` `公众号文章` `抖音脚本` `AI写作` `内容矩阵` `运营工具`

### 适用场景

- 自媒体博主多平台分发
- 企业新媒体矩阵运营
- 知识IP内容批量生产
- 带货文案多平台适配
- 个人品牌内容沉淀
