# geo-event-router

宏观地缘事件路由与评分技能。负责新闻事件的分析、分类、评分和推送决策。

## 功能

- **事件检测**: 识别军事、地缘政治、央行政策、商品价格、市场异动等事件类型
- **多因子评分**: 基于事件类型、来源权威度、市场联动、噪声检测进行综合评分
- **事件指纹**: 生成多维度事件指纹（区域 | 主题 | 资产 | 行为），支持事件演化追踪
- **LLM 语义分析**: 对高价值候选新闻进行深度语义分析（可选）
- **推送决策**: 根据评分阈值和冷却期策略决定是否推送

## 事件类型

| 类型 | 基础分 | 关键词示例 |
|:---|:---:|:---|
| military | 35 | 导弹、空袭、军事行动、战争、袭击 |
| central_bank | 30 | 美联储、央行、加息、降息、利率决议 |
| geopolitics | 28 | 制裁、外交、霍尔木兹、中东、俄乌 |
| commodity | 25 | 原油、黄金、大宗商品、油价、金价 |
| market | 25 | 熔断、暴涨、暴跌、跳水、崩盘 |

## 评分机制

```
总分 = 基础分 + 置信度加分 + 市场映射加分 + LLM 加分 - 降噪扣分
```

| 因子 | 说明 | 分值 |
|:---|:---|:---:|
| 基础分 | 事件类型决定 | 10-35 |
| 置信度 | 权威来源（财联社） | +10 |
| 市场映射 | 原油/黄金异动联动 | +8~15 |
| LLM 分析 | 高紧急度判定 | +5~15 |
| 降噪 | 不确定词汇（传闻、或、可能） | -20 |

## 推送阈值

- **≥70 分**: 高优先级，立即推送
- **50-69 分**: 观察池，等待确认
- **<50 分**: 忽略

## 使用方法

### Python API

```python
from geo_event_router import (
    detect_event_type,
    score_news_item,
    generate_event_fingerprint,
    should_push_event,
    Event,
    EventScore,
    NewsItem,
)

# 创建新闻对象
news = NewsItem(
    title="伊朗总统：伊朗将继续进行正当防御",
    content="伊朗总统发表讲话...",
    source="财联社",
    time_str="15:00",
    time_ts=1711555200,
)

# 检测事件类型
event_type = detect_event_type(news)  # → "military"

# 评分
market = MarketImpact(oil_pct=2.5, gold_pct=1.2)
score = score_news_item(news, market, state)  # → EventScore(total=68.0)

# 生成指纹
fingerprint = generate_event_fingerprint(news, event_type)
# → "middle-east|military|oil|attack"

# 推送决策
should_push, reason = should_push_event(event, state)
```

### 配置

```python
# 推送阈值
PUSH_THRESHOLD_HIGH = 70
PUSH_THRESHOLD_WATCH = 50

# 冷却时间（分钟）
COOLDOWN_HIGH = 90
COOLDOWN_MEDIUM = 180
```

## 依赖

- `llm_news_analyzer` (可选): LLM 语义分析模块
- `geo_market_impact_mapper`: 市场影响数据

## 相关文件

- 主脚本：`geo_event_router.py`
- 配置：同目录 `config.py`

## 版本

- **v1.0.0**: 初始版本，从 smart-geo-push.py v2.0 拆分
