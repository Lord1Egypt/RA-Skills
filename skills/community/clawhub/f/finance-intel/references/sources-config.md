# 数据源配置

## 目录
- [快讯类（实时）](#快讯类实时)
- [深度类（分析）](#深度类分析)
- [宏观/政策](#宏观政策)
- [港美股](#港美股)

---

## 快讯类（实时）

| 源 Key | 名称 | URL | 更新频率 |
|--------|------|-----|---------|
| cls | 财联社 | https://www.cls.cn/telegraph | 5 分钟 |
| wallstreet | 华尔街见闻 | https://www.wallstreetcn.com/live | 5 分钟 |
| eastmoney | 东方财富 | https://news.eastmoney.com/kx/ | 10 分钟 |
| xueqiu | 雪球 | https://xueqiu.com/hots | 10 分钟 |

## 深度类（分析）

| 源 Key | 名称 | URL | 更新频率 |
|--------|------|-----|---------|
| caixin | 财新 | https://www.caixin.com/ | 60 分钟 |
| yicai | 第一财经 | https://www.yicai.com/ | 60 分钟 |
| jiemian | 界面新闻 | https://www.jiemian.com/ | 60 分钟 |
| latepost | 晚点 LatePost | https://www.postlate.cn/ | 120 分钟 |

## 宏观/政策

| 源 Key | 名称 | URL | 更新频率 |
|--------|------|-----|---------|
| pbc | 央行官网 | http://www.pbc.gov.cn/ | 天级 |
| csrc | 证监会 | http://www.csrc.gov.cn/ | 天级 |
| stats | 国家统计局 | http://www.stats.gov.cn/ | 天级 |

## 港美股

| 源 Key | 名称 | URL | 更新频率 |
|--------|------|-----|---------|
| futunn | 富途牛牛 | https://www.futunn.com/learn | 30 分钟 |
| tiger | 老虎证券 | https://www.tigerbrokers.com/ | 30 分钟 |
| seekingalpha | Seeking Alpha | https://seekingalpha.com/ | 30 分钟 |

---

## 数据源类型映射

```python
SOURCES = {
    "cls": {"type": "fast", "cache_minutes": 5},
    "wallstreet": {"type": "fast", "cache_minutes": 5},
    "eastmoney": {"type": "fast", "cache_minutes": 10},
    "xueqiu": {"type": "fast", "cache_minutes": 10},
    "caixin": {"type": "deep", "cache_minutes": 60},
    "yicai": {"type": "deep", "cache_minutes": 60},
    "jiemian": {"type": "deep", "cache_minutes": 60},
    "latepost": {"type": "deep", "cache_minutes": 120},
    "pbc": {"type": "policy", "cache_minutes": 1440},
    "csrc": {"type": "policy", "cache_minutes": 1440},
    "futunn": {"type": "us_hk", "cache_minutes": 30},
    "seekingalpha": {"type": "us_hk", "cache_minutes": 30},
}
```

---

## 添加新数据源

在 `fetch_news.py` 的 `SOURCES` 字典中添加：

```python
"new_source": {
    "name": "新源名称",
    "url": "https://example.com",
    "type": "fast|deep|policy|us_hk",
    "cache_minutes": 10
}
```

然后在 `fetch_news()` 函数中添加对应的抓取函数：

```python
def fetch_new_source_news(browser, limit: int = 15) -> List[Dict]:
    """抓取新源"""
    news_list = []
    # 实现抓取逻辑
    return news_list
```
