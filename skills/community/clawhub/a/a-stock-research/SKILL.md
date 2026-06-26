---
name: a-stock-research
description: Comprehensive A-share (A 股) information gathering and analysis skills for Chinese stock market. Use when you need to query stock prices, analyze financial data, track portfolios, or monitor market trends.
metadata: {author: "托马斯", version: "1.0.0"}
---

# 📈 A 股信息搜集与分析报告

## 已安装的技能套件

### 1️⃣ **akshare-stock** - A 股量化数据分析 ⭐⭐⭐⭐⭐
- **评分**: 1.086 (新安装)
- **数据源**: AkShare（免费开源）
- **功能**: A 股行情、财务数据、板块信息
- **作者**: mbpz

### 2️⃣ **china-stock-analysis** - 中国股票分析 ⭐⭐⭐⭐
- **评分**: 3.590 (新安装)
- **功能**: A 股/港股价格分析、投资建议
- **数据源**: 中国金融市场数据
- **作者**: paulshe

### 3️⃣ **stock-watcher** - 自选股监控 ⭐⭐⭐⭐
- **评分**: 3.649 (新安装)
- **功能**: 自选股管理、性能总结
- **数据源**: 10jqka.com.cn（东方财富网）
- **作者**: Robin797860

### 4️⃣ **stock-analysis** - 股票综合分析 ⭐⭐⭐⭐
- **评分**: 3.699
- **功能**: Yahoo Finance 数据分析、投资组合管理
- **数据源**: Yahoo Finance, Hot Scanner
- **作者**: udiedrichsen

---

## 🚀 核心功能

### AkShare - A 股量化分析
```bash
# 获取股票实时行情
akshare stock_zh_a_spot_em()

# 获取财务数据
akshare stock_financial_analysis_indicator(stock="000001")

# 获取板块信息
akshare sector_info_category()
```

### China Stock Analysis - 中国股票分析
- ✅ A 股价格查询
- ✅ 港股数据分析
- ✅ 投资建议生成
- ✅ 市场趋势预测

### Stock Watcher - 自选股监控
- ✅ 添加/删除自选股
- ✅ 查看自选股列表
- ✅ 获取性能总结
- ✅ 实时监控预警

---

## 💡 使用场景

### 1. **查询股票实时行情**
```bash
# 使用 akshare-stock
npx akshare-stock get_price stock_code="600519"

# 或者使用 china-stock-analysis
npx china-stock-analysis query "贵州茅台"
```

### 2. **分析财务数据**
```bash
# 获取财务指标
npx akshare-stock get_financials stock_code="000001"

# 分析盈利能力
npx china-stock-analysis financial_analysis "600519"
```

### 3. **监控自选股**
```bash
# 添加自选股
npx stock-watcher add 600519 000001

# 查看自选股列表
npx stock-watcher list

# 获取性能总结
npx stock-watcher summary
```

### 4. **投资组合管理**
```bash
# 使用 stock-analysis
npx stock-analysis portfolio add "贵州茅台"
npx stock-analysis portfolio performance
```

---

## 📊 数据源说明

| 技能 | 主要数据源 | 特点 |
|------|-----------|------|
| **akshare-stock** | AkShare (开源) | 免费、全量 A 股数据 |
| **china-stock-analysis** | 中国金融市场 | 专注 A 股/港股 |
| **stock-watcher** | 10jqka.com.cn | 东方财富网，实时性强 |
| **stock-analysis** | Yahoo Finance | 全球市场覆盖 |

---

## 🎯 推荐工作流

### 日常监控流程
```bash
# 1. 查看自选股表现
npx stock-watcher summary

# 2. 查询热门板块
npx akshare-stock get_sector_info

# 3. 分析重点股票
npx china-stock-analysis analyze "600519"

# 4. 生成投资组合报告
npx stock-analysis portfolio report
```

### 深度研究流程
```bash
# 1. 获取财务数据
npx akshare-stock get_financials stock_code="000001"

# 2. 分析技术指标
npx china-stock-analysis technical_analysis "600519"

# 3. 查看市场情绪
npx stock-analysis sentiment "贵州茅台"

# 4. 生成综合报告
npx china-stock-analysis full_report "600519"
```

---

## 📝 常用命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `npx akshare-stock get_price` | 获取价格数据 | `stock_code="600519"` |
| `npx china-stock-analysis query` | 查询股票信息 | `"贵州茅台"` |
| `npx stock-watcher add` | 添加自选股 | `600519 000001` |
| `npx stock-watcher list` | 查看自选股列表 | - |
| `npx stock-watcher summary` | 获取性能总结 | - |
| `npx stock-analysis portfolio` | 投资组合管理 | `add/remove/performance` |

---

## ⚠️ 注意事项

### 数据更新频率
- **AkShare**: 实时/分钟级更新
- **10jqka**: 实时行情，T+1 交易数据
- **Yahoo Finance**: 可能有延迟

### 使用建议
- ✅ 适合短线：stock-watcher + akshare-stock
- ✅ 适合长线：china-stock-analysis + stock-analysis
- ⚠️ 投资有风险，分析仅供参考

---

## 🎓 学习路径

### 初级用户
1. 先学 `stock-watcher` - 管理自选股
2. 使用 `china-stock-analysis query` - 查询基本信息

### 中级用户
1. 学习 `akshare-stock` - 获取详细财务数据
2. 使用 `stock-analysis portfolio` - 投资组合管理

### 高级用户
1. 结合所有技能进行深度分析
2. 自定义数据源和分析策略
3. 建立自己的投资模型

---

## 📂 文件位置

```
/home/anubis/.openclaw/workspace/skills/
├── akshare-stock/        # A 股量化数据分析
├── china-stock-analysis/ # 中国股票分析
├── stock-watcher/        # 自选股监控
└── stock-analysis/       # 股票综合分析（已存在）
```

---

**投资有风险，入市需谨慎！** 📈
