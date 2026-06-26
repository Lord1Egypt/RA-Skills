# Stock Analyst - 智能股票分析系统

港股/美股/A股智能股票分析工具，采用富途(Futu)作为港股主要数据源。

## 数据源

| 市场 | 数据源 | 状态 |
|------|--------|------|
| 港股 | 富途牛牛 (futunn.com) | ✅ 推荐 |
| 美股 | Finnhub API | ✅ |
| A股 | 腾讯财经API | ✅ |

## 安装

```bash
# 克隆仓库
git clone https://github.com/gaoren36-arch/stock-analyst.git
cd stock-analyst

# 安装依赖
pip install requests
```

## 使用方法

### 港股分析 (推荐)

使用浏览器访问富途获取实时数据:

```
股票代码: 03998 (波司登)
富途URL: https://www.futunn.com/stock/03998-HK
```

### 命令行

```bash
python analyze_stock.py 03998
python futu_hk.py 03998
```

## 功能

- ✅ 实时行情查询
- ✅ 技术指标分析 (RSI, MACD, 均线)
- ✅ 分析师评级和目标价
- ✅ 资金流向
- ✅ 综合分析报告 (7大板块)

## 股票代码示例

### 港股
- 03998 波司登
- 01833 平安好医生
- 06060 众安在线
- 00700 腾讯
- 09988 阿里巴巴

### 美股
- JD 京东
- BABA 阿里巴巴
- TSLA 特斯拉
- AAPL 苹果

### A股
- 601857 中国石油
- 600519 贵州茅台
- 300750 宁德时代

## 版本

- v2.1.0 - 富途数据源，港股数据准确可靠
- v2.0.0 - 整合技术指标和新闻分析
- v1.0.0 - 初始版本

## 作者

- GitHub: gaoren36
- Email: (略)

## 许可证

MIT
