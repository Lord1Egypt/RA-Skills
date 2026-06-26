---
name: cn-ai-search
description: 中文AI Agent专用多平台聚合搜索工具，开箱即用，国内网络友好
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"]}}}
---

# 🔍 cn-ai-search - 中文AI聚合搜索Skill（轻量版）

专为中文AI Agent/智能体优化的多平台聚合搜索工具，一次查询覆盖全网主流中文平台，自动去重过滤广告，输出干净结构化结果。

## 🧠 设计理念：AI-First 搜索范式

传统搜索是给人用的——充满广告、SEO垃圾、重复内容。cn-ai-search 是专门为 AI Agent 设计的搜索：

- **无广告污染**：专为大模型设计的干净输出，没有任何广告干扰
- **结构化数据**：直接输出结构化结果，Agent 不用自己解析
- **多源融合**：一次查询覆盖多个平台，AI 获得的是全网视角

## ✨ 核心特点

| 特点 | 说明 |
|------|------|
| 📦 **开箱即用** | 无需API密钥，安装就能用 |
| 🇨🇳 **中文全覆盖** | 百度、微信公众号、知乎、B站全覆盖 |
| 🧹 **自动净化** | 过滤广告、SEO垃圾、重复内容，结果干净直接喂大模型 |
| 🌏 **国内友好** | 对国内网络优化，海外服务器也能正常访问 |

## 🚀 支持平台

✅ 基础可用（无需配置）：
- 百度搜索
- 微信公众号搜索（搜狗）
- 知乎搜索
- B站搜索
- 必应中国
- 360搜索
- 搜狗搜索
- 头条搜索

## 📖 快速使用

```bash
# 同时搜索所有默认平台
cn-ai-search "AI Agent 商业化"

# 指定平台搜索（多个用逗号分隔）
cn-ai-search --platforms baidu,zhihu "你的搜索关键词"

# 按最新排序
cn-ai-search --sort latest "热点事件"

# 指定结果数量
cn-ai-search --count 30 "你的关键词"

# 输出纯文本
cn-ai-search --format plain "你的关键词"
```

## 🔧 安装

```bash
# 安装Python依赖
pip install -r requirements.txt

# 创建命令链接
ln -s $(pwd)/index.py /usr/local/bin/cn-ai-search
chmod +x /usr/local/bin/cn-ai-search
```

## 🎯 适用场景

- AI Agent需要获取实时中文信息
- 商业情报搜集、商机挖掘
- 多平台内容聚合调研
- 市场分析、竞品分析
- 新闻热点追踪

## 📝 许可证

MIT License
