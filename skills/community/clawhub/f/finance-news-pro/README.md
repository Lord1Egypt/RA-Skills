# Finance News Pro - README

📈 **专业级财经新闻聚合与分析工具**

为投资决策提供信息优势 —— 情感分析、影响评估、个股关联、操作建议。

---

## 🚀 快速开始

### 1. 基础使用

```bash
# 获取今日财经简报
python fetch_news.py

# 指定数据源
python fetch_news.py --source cls,wallstreet

# 关键词过滤
python fetch_news.py --keyword "AI，算力"
```

### 2. 查看输出

报告自动保存到：
```
finance-news-pro/reports/YYYY-MM-DD/YYYY-MM-DD_briefing.md
```

---

## 📡 支持的数据源（12+）

| 类型 | 源 | 更新频率 |
|---|---|---|
| **快讯** | 财联社、华尔街见闻、东方财富、雪球 | 实时 |
| **深度** | 财新、第一财经、界面、晚点 | 小时级 |
| **政策** | 央行、证监会、统计局 | 天级 |
| **港美股** | 富途、老虎、Seeking Alpha | 分钟级 |

---

## 🎯 核心功能

### ✅ 情感分析
自动判断每条新闻是 **利好🟢** / **利空🔴** / **中性⚪**

### ✅ 影响评估
三级影响评估：**市场级** → **行业级** → **公司级**

### ✅ 个股关联
自动识别新闻中提及的股票（A 股/港股/美股）

### ✅ 操作建议
根据情感和影响给出：**关注** / **谨慎** / **观望**

---

## 📊 输出示例

```markdown
# 📈 财经简报 - 2026-03-13 15:00

## 🔥 头条焦点

### 1. [央行降准 0.25 个百分点](https://...) 🟢利好
- 来源：财联社 | 时间：14:15
- 影响：市场级
- 相关股票：招商银行、工商银行
- 操作建议：关注

## 📊 市场情绪
- 整体：偏多 (65% 利好)
```

---

## ⚙️ 配置

编辑 `config.json`：

```json
{
  "stocks": {
    "宁德时代": {"code": "300750.SZ", "sector": "新能源"}
  },
  "keywords": {
    "AI": ["AI", "LLM", "算力", "大模型"]
  }
}
```

---

## 📁 目录结构

```
finance-news-pro/
├── SKILL.md          # 技能说明（给 AI 看）
├── fetch_news.py     # 核心抓取脚本
├── config.json       # 配置文件
├── requirements.txt  # 依赖说明
├── README.md         # 本文件
├── reports/          # 生成的报告
│   └── 2026-03/
│       └── 2026-03-13_briefing.md
└── cache/            # 原始数据缓存
    └── 2026-03-13/
        ├── cls.json
        └── wallstreet.json
```

---

## 🔧 高级用法

### 定时任务（cron）

```bash
# 每天早上 8 点
0 8 * * 1-5 cd ~/workspace/skills/finance-news-pro && python fetch_news.py

# 收盘后复盘
30 15 * * 1-5 cd ~/workspace/skills/finance-news-pro && python fetch_news.py --summary
```

### 集成到 OpenClaw

在 OpenClaw 中直接使用：
```
/finance-news --keyword "新能源"
```

---

## 📝 更新日志

### v1.0.0 (2026-03-13)
- ✅ 12+ 财经源支持
- ✅ 情感分析（利好/利空/中性）
- ✅ 影响评估（市场/行业/公司）
- ✅ 个股关联（A 股/港股/美股）
- ✅ 操作建议
- ✅ Markdown 报告生成
- ✅ 缓存机制

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License

---

**Made with ❤️ by 夏夏 for 明**
