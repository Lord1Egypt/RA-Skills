---
version: 1.0.35
---

# 非毒·分析魄 (Fei Du - Analyst)

> **七魄之五·非毒**
> 职掌：洞察提炼、模式识别、数据分析

---

## 技能简介

「非毒·分析魄」是贫道的数据分析模块，职掌洞察提炼与模式识别。

**核心职责**：
- 从数据中提取洞察
- 识别规律与异常
- 生成分析报告

---

## 技能ID

```
fei-du
```

---

## 能力清单

### 1. 数据分析 (analyze)

分析给定数据，提取洞察。

**输入**：`data` (object) - 待分析数据
```yaml
data:
  type: text|number|list|table
  content: 数据内容
  context: 背景上下文
```

**输出**：
```yaml
insights:
  - key: 洞察主题
    value: 洞察内容
    confidence: 置信度(0-1)
  patterns: 发现的模式列表
  anomalies: 异常列表
```

---

### 2. 趋势识别 (trend)

识别数据趋势。

**输入**：`series` (array) - 时间序列数据

**输出**：
```yaml
trend:
  direction: ascending|descending|stable|volatile
  changeRate: 变化率
  forecast: 预测值
  confidence: 置信度
```

---

### 3. 对比分析 (compare)

对比两个或多个对象的差异。

**输入**：`items` (array) - 待对比项
**输出**：
```yaml
comparison:
  similarities: 共同点
  differences: 差异点
  recommendation: 推荐
```

---

---

## 聚合技能

本魄作为分析中枢，洞察提炼与模式识别：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `github` | 调用 | GitHub 数据分析 |
| `stock-monitor` | 调用 | 股票数据分析 |
| `eastmoney-stock` | 调用 | 东方财富股票分析 |
| `china-stock-analysis` | 调用 | 中国股市分析 |
| `new-akshare-stock` | 调用 | AkShare A股分析 |
| `tushare-finance` | 调用 | Tushare金融数据分析 |
| `summarize` | 调用 | 内容总结分析 |
| `multi-search-engine` | 调用 | 搜索结果分析 |
| `image-reader` | 调用 | 图像内容分析 |
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

非毒洞察，洞若观火——模式识别，洞察本质。
