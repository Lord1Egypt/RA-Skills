
# A股日报 - 接口设计文档

&gt; 本文档详细定义各模块的接口签名、输入输出参数和异常处理机制

---

## 🏗️ 接口设计原则

| 原则 | 说明 |
|------|------|
| **返回结构统一** | 所有接口返回统一的 `{success, data, error}` 结构 |
| **降级透明** | 数据源降级对上层透明，通过配置优先级链 |
| **缓存策略** | 接口级缓存，TTL可配置 |
| **异常处理** | 非致命异常返回部分数据，致命异常返回错误 |

---

## 📊 统一返回结构

```python
{
    "success": bool,      # 是否成功
    "data": dict/list,    # 数据内容
    "error": str,         # 错误信息（如果有）
    "source": str,        # 实际使用的数据源（用于调试）
    "cached": bool        # 是否来自缓存
}
```

---

## 🔌 数据采集模块接口（DataFetcher）

### 1. 指数数据接口

```python
def get_index_data(index_code: str, date: str) -&gt; dict:
    """
    获取指数数据（四大指数）

    Args:
        index_code: 指数代码
            - "000001.SH"  上证综指
            - "399001.SZ"  深证成指
            - "399006.SZ"  创业板指
            - "000688.SH"  科创50
        date: 日期，格式 "YYYY-MM-DD"

    Returns:
        {
            "success": True,
            "data": {
                "ts_code": "000001.SH",
                "name": "上证指数",
                "trade_date": "2026-03-28",
                "close": 3050.25,
                "open": 3045.10,
                "high": 3065.80,
                "low": 3038.50,
                "pre_close": 3040.00,
                "change": 10.25,
                "change_pct": 0.34,  # 百分比
                "vol": 125600000000,   # 成交量
                "amount": 1856000000000  # 成交额
            },
            "source": "akshare",
            "cached": False
        }
    """
    pass
```

### 2. 市场情绪数据接口

```python
def get_market_sentiment(date: str) -&gt; dict:
    """
    获取市场情绪数据

    Args:
        date: 日期 "YYYY-MM-DD"

    Returns:
        {
            "success": True,
            "data": {
                "trade_date": "2026-03-28",
                # 涨跌家数
                "up_count": 2850,
                "down_count": 1650,
                "flat_count": 150,
                # 涨跌停
                "limit_up_count": 85,
                "limit_down_count": 12,
                # 连板
                "consec_up_2": 25,    # 2连板
                "consec_up_3": 12,    # 3连板
                "consec_up_5plus": 3, # 5板及以上
                "max_consec_up": 7,   # 最高连板
                # 炸板
                "failed_limit_up": 18,
                "failed_rate": 17.5,  # 炸板率 %
                # 昨日涨停今日表现
                "prev_limit_up_avg_return": 2.8,
                # 成交额
                "total_turnover": 1856000000000,
                "turnover_change_pct": -5.2  # 较昨日变化 %
            },
            "source": "akshare",
            "cached": False
        }
    """
    pass
```

### 3. 资金流向数据接口

```python
def get_money_flow(date: str) -&gt; dict:
    """
    获取资金流向数据

    Args:
        date: 日期 "YYYY-MM-DD"

    Returns:
        {
            "success": True,
            "data": {
                "trade_date": "2026-03-28",
                # 北向资金
                "northbound": {
                    "hk_to_sh": 2580000000,    # 沪股通
                    "hk_to_sz": 1850000000,    # 深股通
                    "total_net_inflow": 4430000000,
                    "buy_amount": 85600000000,
                    "sell_amount": 81170000000,
                    "net_inflow_3d": 12500000000,
                    "net_inflow_5d": 18700000000
                },
                # 主力资金
                "main_capital": {
                    "super_large_net_inflow": 2850000000,  # 超大单
                    "large_net_inflow": 1560000000,         # 大单
                    "medium_net_inflow": -850000000,        # 中单
                    "small_net_inflow": -3560000000,        # 小单
                    "total_net_inflow": 800000000
                }
            },
            "source": "akshare",
            "cached": False
        }
    """
    pass
```

### 4. 板块数据接口

```python
def get_sector_data(date: str) -&gt; dict:
    """
    获取板块数据

    Args:
        date: 日期 "YYYY-MM-DD"

    Returns:
        {
            "success": True,
            "data": {
                "trade_date": "2026-03-28",
                # 涨幅榜前5
                "top_up_sectors": [
                    {
                        "name": "ChatGPT概念",
                        "code": "BK0980",
                        "change_pct": 5.82,
                        "lead_stock": "三六零",
                        "lead_change_pct": 10.02,
                        "fund_inflow": 1580000000,
                        "turnover_rate": 12.5
                    },
                    # ... 更多板块
                ],
                # 跌幅榜前5
                "top_down_sectors": [
                    {
                        "name": "银行",
                        "code": "BK0465",
                        "change_pct": -2.15,
                        "lead_stock": "招商银行",
                        "lead_change_pct": -3.25,
                        "fund_outflow": 850000000,
                        "turnover_rate": 1.8
                    },
                    # ... 更多板块
                ],
                # 热点概念
                "hot_concepts": [
                    {"name": "AI芯片", "change_pct": 4.25, "stock_count": 35},
                    {"name": "算力", "change_pct": 3.85, "stock_count": 42}
                ]
            },
            "source": "akshare",
            "cached": False
        }
    """
    pass
```

### 5. 龙虎榜数据接口

```python
def get_longhubang(date: str) -&gt; dict:
    """
    获取龙虎榜数据

    Args:
        date: 日期 "YYYY-MM-DD"

    Returns:
        {
            "success": True,
            "data": {
                "trade_date": "2026-03-28",
                "total_stocks": 35,  # 上榜个股数
                "stocks": [
                    {
                        "ts_code": "601360.SH",
                        "name": "三六零",
                        "close": 18.56,
                        "change_pct": 10.02,
                        "turnover_rate": 25.8,
                        "reason": "日涨幅偏离值达7%",
                        "buy_seats": [
                            {
                                "name": "机构专用",
                                "buy_amount": 258000000,
                                "sell_amount": 25000000,
                                "net_buy": 233000000
                            },
                            # ... 更多买席
                        ],
                        "sell_seats": [
                            # ... 卖席
                        ],
                        "total_net_buy": 856000000
                    },
                    # ... 更多个股
                ]
            },
            "source": "akshare",
            "cached": False
        }
    """
    pass
```

### 6. 美股数据接口

```python
def get_us_market() -&gt; dict:
    """
    获取美股数据

    Returns:
        {
            "success": True,
            "data": {
                "update_time": "2026-03-28 07:30:00",
                "indices": {
                    "nasdaq": {
                        "name": "纳斯达克",
                        "code": "IXIC",
                        "close": 16258.56,
                        "change": 85.25,
                        "change_pct": 0.53,
                        "high": 16325.80,
                        "low": 16185.20
                    },
                    "sp500": {
                        "name": "标普500",
                        "code": "INX",
                        "close": 5125.80,
                        "change": 18.56,
                        "change_pct": 0.36,
                        "high": 5142.20,
                        "low": 5105.50
                    },
                    "dow": {
                        "name": "道琼斯",
                        "code": "DJI",
                        "close": 38856.25,
                        "change": -45.80,
                        "change_pct": -0.12,
                        "high": 38985.50,
                        "low": 38725.80
                    }
                },
                "chinadotcom": {
                    "tencent": {
                        "name": "腾讯",
                        "code": "TCEHY",
                        "close": 58.25,
                        "change": 2.85,
                        "change_pct": 5.15
                    },
                    "alibaba": {
                        "name": "阿里巴巴",
                        "code": "BABA",
                        "close": 78.56,
                        "change": 3.25,
                        "change_pct": 4.32
                    },
                    "pdd": {
                        "name": "拼多多",
                        "code": "PDD",
                        "close": 145.80,
                        "change": -2.85,
                        "change_pct": -1.92
                    }
                }
            },
            "source": "sina",
            "cached": False
        }
    """
    pass
```

### 7. 商品数据接口

```python
def get_commodities() -&gt; dict:
    """
    获取大宗商品数据

    Returns:
        {
            "success": True,
            "data": {
                "update_time": "2026-03-28 07:30:00",
                "crude_oil": {
                    "name": "WTI原油",
                    "code": "CL",
                    "close": 85.62,
                    "change": 1.25,
                    "change_pct": 1.48
                },
                "gold": {
                    "name": "黄金",
                    "code": "GC",
                    "close": 2185.60,
                    "change": -8.25,
                    "change_pct": -0.38
                },
                "copper": {
                    "name": "铜",
                    "code": "HG",
                    "close": 4.258,
                    "change": 0.052,
                    "change_pct": 1.24
                }
            },
            "source": "sina",
            "cached": False
        }
    """
    pass
```

### 8. 外汇数据接口

```python
def get_forex() -&gt; dict:
    """
    获取外汇数据

    Returns:
        {
            "success": True,
            "data": {
                "update_time": "2026-03-28 07:30:00",
                "dollar_index": {
                    "name": "美元指数",
                    "code": "DXY",
                    "close": 104.52,
                    "change": 0.15,
                    "change_pct": 0.14
                },
                "usdcny": {
                    "name": "美元兑人民币",
                    "code": "USDCNY",
                    "close": 7.2456,
                    "change": 0.0085,
                    "change_pct": 0.12
                },
                "eurusd": {
                    "name": "欧元兑美元",
                    "code": "EURUSD",
                    "close": 1.0825,
                    "change": -0.0015,
                    "change_pct": -0.14
                }
            },
            "source": "sina",
            "cached": False
        }
    """
    pass
```

### 9. 期指数据接口

```python
def get_index_futures() -&gt; dict:
    """
    获取期指数据（A50、沪深300）

    Returns:
        {
            "success": True,
            "data": {
                "update_time": "2026-03-28 07:30:00",
                "a50": {
                    "name": "富时A50期指",
                    "code": "CN",
                    "last": 11856.25,
                    "change": 45.80,
                    "change_pct": 0.39,
                    "session": "夜盘"
                },
                "hs300": {
                    "name": "沪深300期指",
                    "code": "IF",
                    "last": 3525.80,
                    "change": 18.56,
                    "change_pct": 0.53,
                    "session": "夜盘"
                }
            },
            "source": "sina",
            "cached": False
        }
    """
    pass
```

### 10. 新闻数据接口

```python
def get_news(date: str, limit: int = 10) -&gt; list:
    """
    获取财经新闻

    Args:
        date: 日期 "YYYY-MM-DD"
        limit: 新闻条数

    Returns:
        {
            "success": True,
            "data": [
                {
                    "title": "央行宣布降准0.5个百分点",
                    "content": "中国人民银行决定...",
                    "source": "财联社",
                    "publish_time": "2026-03-28 07:25:00",
                    "importance": "high",  # high/medium/low
                    "related_sectors": ["银行", "房地产"],
                    "related_stocks": ["招商银行", "万科A"]
                },
                # ... 更多新闻
            ],
            "source": "mx-search",
            "cached": False
        }
    """
    pass
```

---

## 📊 分析模块接口（Analyzer）

### 1. 30秒总览生成

```python
def generate_summary(data: dict, mode: str) -&gt; dict:
    """
    生成30秒总览

    Args:
        data: 完整数据字典
        mode: "morning" 或 "evening"

    Returns:
        {
            "success": True,
            "data": {
                "one_sentence": "今日市场整体偏暖，AI概念领涨，关注科技主线",
                "core_opportunities": [
                    "AI算力产业链持续受益",
                    "ChatGPT概念龙头有望连板"
                ],
                "risk_warnings": [
                    {"level": "high", "content": "美股波动可能传导"},
                    {"level": "medium", "content": "北向资金流入放缓"},
                    {"level": "low", "content": "部分板块获利了结压力"}
                ]
            }
        }
    """
    pass
```

### 2. 自选股分析（早报）

```python
def analyze_watchlist_morning(data: dict, watchlist: list) -&gt; list:
    """
    早报：自选股简洁预测

    Args:
        data: 市场数据
        watchlist: 自选股列表

    Returns:
        {
            "success": True,
            "data": [
                {
                    "code": "600519.SH",
                    "name": "贵州茅台",
                    "view": "震荡",  # bullish/bearish/sideways
                    "reason": "白酒板块整体平稳，关注一季报预期"
                },
                {
                    "code": "300750.SZ",
                    "name": "宁德时代",
                    "view": "看涨",
                    "reason": "新能源赛道反弹，北向持续加仓"
                }
            ]
        }
    """
    pass
```

### 3. 自选股分析（晚报）

```python
def analyze_watchlist_evening(data: dict, watchlist: list) -&gt; dict:
    """
    晚报：自选股复盘

    Args:
        data: 市场数据
        watchlist: 自选股列表

    Returns:
        {
            "success": True,
            "data": {
                "overall": {
                    "up_count": 3,
                    "down_count": 2,
                    "avg_return": 1.25
                },
                "best": {
                    "code": "300750.SZ",
                    "name": "宁德时代",
                    "change_pct": 5.82,
                    "reason": "新能源板块领涨，公司发布超预期业绩预告"
                },
                "worst": {
                    "code": "601318.SH",
                    "name": "中国平安",
                    "change_pct": -2.15,
                    "reason": "保险板块整体调整"
                },
                "tomorrow_strategy": "继续持有新能源龙头，金融股观望"
            }
        }
    """
    pass
```

### 4. 交易策略生成

```python
def generate_trading_strategy(data: dict) -&gt; dict:
    """
    生成交易策略（进攻/防守/观望）

    Args:
        data: 市场数据

    Returns:
        {
            "success": True,
            "data": {
                "strategy": "offensive",  # offensive/defensive/waiting
                "strategy_name": "进攻",
                "logic": "市场情绪回暖，AI主线明确，建议适度进攻",
                "confidence": 0.75  # 置信度 0-1
            }
        }
    """
    pass
```

---

## 📝 渲染模块接口（Renderer）

```python
def render_morning_report(analysis_result: dict) -&gt; str:
    """
    渲染早报预测版Markdown

    Args:
        analysis_result: 分析结果

    Returns:
        完整的Markdown字符串
    """
    pass

def render_evening_report(analysis_result: dict) -&gt; str:
    """
    渲染晚报复盘版Markdown
    """
    pass
```

---

## 🚀 发布模块接口（Publisher）

```python
def publish_report(markdown_content: str, mode: str, date: str) -&gt; dict:
    """
    完整发布流程

    Returns:
        {
            "success": True,
            "data": {
                "doc_url": "https://xxx.feishu.cn/docx/xxx",
                "pdf_path": "/path/to/report.pdf",
                "message_sent": True
            }
        }
    """
    pass
```

---

## 🛠️ 工具函数接口

### 缓存工具

```python
def get_cache(key: str, ttl: int = 3600) -&gt; any:
    """获取缓存"""
    pass

def set_cache(key: str, value: any, ttl: int = 3600) -&gt; None:
    """设置缓存"""
    pass
```

### 交易日历

```python
def is_trade_day(date: str) -&gt; bool:
    """判断是否为交易日"""
    pass

def prev_trade_day(date: str) -&gt; str:
    """获取前一个交易日"""
    pass

def next_trade_day(date: str) -&gt; str:
    """获取后一个交易日"""
    pass
```

---

*本文档定义了所有接口的详细设计，后续开发严格按照此接口执行*

