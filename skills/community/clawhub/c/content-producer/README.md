# 📝 多平台内容分发器 v1.0 (标准付费版)

> **写一篇内容，自动适配4个平台。小红书、知乎、公众号、抖音一键输出。**

## 📦 包含文件

```
content-producer-v1/
├── content_producer.py    # 主程序 (直接运行)
├── SKILL.md               # OpenClaw 配置
└── README.md              # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 设置 API Key

```bash
export OPENAI_API_KEY="sk-xxx"
# 可选: 用便宜模型省钱
export OPENAI_MODEL="gpt-4o-mini"
```

### 3. 一键生成所有平台

```bash
python3 content_producer.py \
  --topic "2026年普通人如何用AI赚钱" \
  --platform all
```

## 📖 详细用法

### 生成指定平台

```bash
# 只生成小红书
python3 content_producer.py --topic "AI工具推荐" --platform xiaohongshu

# 只生成知乎
python3 content_producer.py --topic "为什么AI会改变打工方式" --platform zhihu
```

### 带要点生成（推荐）

```bash
python3 content_producer.py \
  --topic "程序员为什么要学AI" \
  --points "AI不是取代工具,涨薪30%,现在入局最佳,10年后的基本技能" \
  --platform all
```

### 不同写作风格

```bash
--style professional   # 专业风（适合知乎、公众号）
--style casual         # 口语风（适合小红书、抖音）[默认]
--style educational    # 教育风
--style promotional    # 营销风
```

### 指定输出目录

```bash
--output ./my_content
```

### 查看历史内容

```bash
python3 content_producer.py --topic "" --history
```

## 🔧 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENAI_API_KEY` | - | **必填** OpenAI API Key |
| `OPENAI_BASE` | `https://api.openai.com/v1` | API地址（可换代理/第三方兼容API） |
| `OPENAI_MODEL` | `gpt-4o-mini` | 模型（推荐 gpt-4o-mini，便宜够用） |
| `CONTENT_OUTPUT_DIR` | `./content_output` | 输出目录 |

## 📂 输出格式

```
content_output/YYYYMMDD/
├── [小红书]_主题_时间戳.md
├── [知乎]_主题_时间戳.md
├── [公众号]_主题_时间戳.md
└── [抖音]_主题_时间戳.md
```

每个文件头部有元数据：

```yaml
---
title: 主题
platform: xiaohongshu
generated: 2026-04-25 14:30
model: gpt-4o-mini
---
```

## 💰 成本估算

使用 gpt-4o-mini（每百万 token 约 ¥1.5）：
- 生成4个平台全部内容 ≈ ¥0.1-0.3
- 每天用10次 ≈ ¥1-3
- 对比请一个文案月薪5000 → 省大了

## 💡 常见问题

**Q: 支持其他平台吗？**
A: 目前支持小红书/知乎/公众号/抖音。后续会根据需求增加。

**Q: 内容质量怎么样？**
A: 质量取决于模型和提示词。gpt-4o-mini 性价比最高，gpt-4o 质量更好但贵一些。

**Q: 生成的内容可以直接发吗？**
A: 建议根据个人风格微调后再发布。AI生成内容作为初稿和框架非常高效。

**Q: 没有 OpenAI Key 怎么办？**
A: 可以使用任何兼容 OpenAI 格式的 API（DeepSeek、Claude、智谱等），改 `OPENAI_BASE` 地址即可。

---

**版本:** 1.0.0 | **类型:** 标准付费款 | **定价:** ¥29.9
