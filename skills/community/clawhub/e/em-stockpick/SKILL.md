---
name: "DFCF_StockPick"
description: "Use eastmoney official website to perform conditional stock selection with natural language. Invoke when user asks to select stocks based on conditions, analyze market trends, or query specific stock selection criteria."
---
# 东方财富条件选股

## 功能描述

使用Python访问东方财富官网，通过自然语言描述执行条件选股，支持各种技术指标和基本面条件的组合查询。  
支持以下类型：

- **A股**、**港股**、
- **ETF**、**可转债**、**板块**

### **查询示例**

query | select-type |

\----------|----------|

股价大于1000元的股票、创业板市盈率最低的50只 | A股 |

港股的科技龙头 | 港股 |

今天涨幅最大板块 | 板块 |

规模超2亿的电力ETF | ETF |

价格低于110元、溢价率超5个点的可转债 | 可转债 |

## 快速开始

### 1\. 命令行调用

```bash
python -m scripts.em_stock_selector --query 股价大于100元的股票；涨跌幅；所属板块 --select-type A股
```

**参数说明：**

| 参数 | 说明 | 必填 |

|------|------|------|

| `--query` | 自然语言查询条件 | ✅ |

| `--select-type` | 查询领域 | ✅ |