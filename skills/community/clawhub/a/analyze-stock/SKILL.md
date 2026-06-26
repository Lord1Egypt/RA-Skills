---
name: stock-analysis
description: 股票分析技能，提供买卖点判断、仓位管理、基本面分析。使用当用户需要分析股票投资价值时。
triggers:
  - "分析股票"
  - "股票分析"
  - "看股票"
  - "stock"
  - "买点"
  - "卖点"
  - "仓位"
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"], "env":["TUSHARE_TOKEN","BAIDU_API_KEY"] } } }
---

# 股票分析技能

使用 Tushare 获取实时财务数据，结合百度搜索和全局大模型进行深度分析。

## 功能

1. **核心价格区间与买卖点** - 基于 PE 分位计算 5 档估值区间
2. **仓位管理策略** - 三步建仓法 + 止损止盈
3. **关键观察信号** - 量能、均线、消息面实时分析
4. **基本面分析** - 近三年财务数据 + 申万行业分类 + 同花顺概念
5. **BCG 业务矩阵** - 现金牛、明星、问题、瘦狗分析
6. **利好与风险** - 使用全局大模型深度分析

## 使用方法

### 方式 1：命令行
```bash
python3 scripts/analyze_stock.py --stock 601117
python3 scripts/analyze_stock.py --stock 601117 --style balanced
```

### 方式 2：OpenClaw 标准调用
```python
ctx.claw.skills.run("stock-analysis", {
    "stock_code": "601117",
    "style": "balanced"  # conservative/balanced/aggressive
})
```

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stock_code | str | ✅ | 股票代码（6 位数字） |
| style | str | ❌ | 投资风格（conservative/balanced/aggressive） |

## 输出格式

```json
{
  "stock": "601117",
  "name": "中国化学",
  "report": "完整分析报告",
  "analysis": "大模型分析的利好与风险因素",
  "model": "阿里云 Coding Plan(全局自动调用)"
}
```

## 依赖配置

### 方式 1：环境变量（推荐）

复制 `.env.example` 为 `.env` 并填入你的 API key：

```bash
cd ~/.openclaw/workspace/skills/stock-analysis
cp .env.example .env
# 编辑 .env 文件，填入真实的 API key
```

### 方式 2：OpenClaw 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "stock-analysis": {
        "env": {
          "TUSHARE_TOKEN": "your_tushare_token",
          "BAIDU_API_KEY": "your_baidu_api_key",
          "TAVILY_API_KEY": "your_tavily_api_key"
        }
      }
    }
  }
}
```

### API Key 获取方式

| API | 用途 | 获取方式 | 必需 |
|-----|------|----------|------|
| TUSHARE_TOKEN | 获取财务数据 | https://tushare.pro (免费注册) | ✅ |
| BAIDU_API_KEY | 百度搜索新闻 | 百度智能云控制台 | ❌ 可选 |
| TAVILY_API_KEY | 深度分析 | https://tavily.com | ❌ 可选 |

## 示例

### 输入
```json
{
  "stock_code": "601117",
  "style": "balanced"
}
```

### 输出
```json
{
  "stock": "601117",
  "name": "中国化学",
  "report": "# 📈 中国化学 (601117) 分析报告\n\n...",
  "analysis": "利好因素：\n1. 行业地位领先...\n风险因素：\n1. 行业竞争加剧...",
  "model": "阿里云 Coding Plan(全局自动调用)"
}
```
