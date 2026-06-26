---
name: bocha-search
description: 博查 AI 搜索工具。调用 https://api.bocha.cn 进行网页搜索，返回带摘要的中文结果。不依赖 OpenClaw 内置 web_search。
---

# 🔍 Bocha Search Skill

博查 AI 搜索工具 - 调用 api.bocha.cn 进行网页搜索。

## ⚡ 快速开始

### 1. 配置 API Key

```bash
# 替换 YOUR_API_KEY 为你的博查 API Key
~/.openclaw/skills/bocha-search/scripts/setup.sh YOUR_API_KEY
```

获取 API Key: [https://open.bocha.cn](https://open.bocha.cn)

### 2. 执行搜索

```bash
# 搜索（默认 5 条结果）
~/.openclaw/skills/bocha-search/scripts/search.sh "搜索关键词"

# 指定结果数量
~/.openclaw/skills/bocha-search/scripts/search.sh "搜索关键词" 10
```

## 📋 使用方法

### 通过环境变量

```bash
export BOCHA_API_KEY="sk-你的APIKey"
~/.openclaw/skills/bocha-search/scripts/search.sh "关键词"
```

### 直接用 curl

```bash
curl -s "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"关键词",
    "summary": true,
    "freshness": "noLimit",
    "count": 5
  }'
```

## 📝 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词 | 必填 |
| `summary` | true 返回 AI 摘要 | true |
| `freshness` | 时间筛选: noLimit/pd/pw/pm/py | noLimit |
| `count` | 结果数量 (1-10) | 5 |

## 📤 输出格式

每条结果包含：
- **📌 标题** - 页面标题
- **🔗 链接** - 页面 URL  
- **📝 摘要** - AI 生成的摘要

## ⚙️ 配置说明

### 配置文件位置

首次配置后，API Key 保存在：
```
~/.openclaw/skills-config/bocha-search.json
```

### 更新 API Key

```bash
# 重新运行 setup 脚本
~/.openclaw/skills/bocha-search/scripts/setup.sh 新的APIKey
```

## 🔒 安全说明

- ✅ API Key 存储在本地配置文件中，不暴露在代码中
- ✅ 支持环境变量方式，避免配置文件泄露
- ❌ 不要将包含 API Key 的配置提交到代码仓库

## 📂 文件结构

```
bocha-search/
├── SKILL.md              # 本文档
├── _meta.json            # 元数据
└── scripts/
    ├── setup.sh          # 配置 API Key
    └── search.sh         # 搜索脚本
```

## ❓ 常见问题

**Q: 搜索返回错误怎么办？**
A: 检查 API Key 是否正确，可访问 https://open.bocha.cn 查看配额

**Q: 结果数量可以更多吗？**
A: 当前支持 1-10 条，API 限制

**Q: 如何切换搜索时间？**
A: 修改 freshness 参数: pd(天)、pw(周)、pm(月)、py(年)、noLimit(不限)

## 🔗 相关链接

- [博查官网](https://www.bocha.cn)
- [博查开放平台](https://open.bocha.cn)
- [API 文档](https://bocha.com/documents/web-search-api)
