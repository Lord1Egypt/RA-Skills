<!-- 本文件由生成器从后端源码导出,不要手改;改了下次生成就冲掉。 -->

# 端点参考(共 14 个,对外只读)

基址 `https://geo-analytics.info/api/reports`,鉴权 `Authorization: Bearer <access_token>`。

- 日期参数一律 `from` / `to`,格式 `YYYY-MM-DD`,**北京日口径**;
- `tag_id` 全部必填,取授权时返回的那个 —— token 只绑一个站,填别的会 **403**;
- 全部是 **GET**,全部只读。这套凭证下不存在任何写操作;
- 出错:401 = token 失效或被吊销(重走授权)/ 403 = 站点对不上 / 422 = 参数不合法 /
  429 = 触发限速(看 `Retry-After`)。**任何一种失败都直接说失败,不要补一个数字上去。**


| 端点 | 用途 | 参数(除 `tag_id`/`from`/`to`) |
|---|---|---|
| `/overview` | 概览卡片(访客/会话/浏览量/事件/互动会话占比) | — |
| `/timeseries` | 按天趋势(访客/会话/浏览量) | — |
| `/acquisition` | 来源拆分,维度可切 | `dimension` |
| `/pages` | 页面排行 | `limit`, `dimension` |
| `/pages_timeseries` | TopN 页面按天 | `top` |
| `/events` | 事件名汇总 | — |
| `/bots` | 爬虫视角(常规报表已排除爬虫) | — |
| `/engagement` | 参与度(互动会话、时长;时长看中位数) | — |
| `/conversions` | 转化(金额按币种分组,跨币种不相加) | — |
| `/realtime` | 近 30 分钟滚动窗 ⚠️**无日期参数** | — |
| `/engines` | 引擎侧(应答采样)× 站点侧(实测流量)并排 | — |
| `/probe-events` | 应答采样原始记录(含 answer_text 与 sources) | `limit` |
| `/ivt` | 无效流量报表(打标不拦截) | — |
| `/ivt/session-events` | 单会话事件序列(抽查下钻) ⚠️**无日期参数** | `session_id` |

## `GET /overview`

概览卡片(访客/会话/浏览量/事件/互动会话占比)

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `Overview`:

```
visitors: int
sessions: int
page_views: int
events: int
new_visitors: int
engaged_rate: float    # 互动会话占比(0-1)
engine_sessions: list[EngineSessions]
  engine: str
  sessions: int
```

## `GET /timeseries`

按天趋势(访客/会话/浏览量)

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `list[DayRow]`:

```
day: date
visitors: int
sessions: int
page_views: int
```

## `GET /acquisition`

来源拆分,维度可切

⚠️ `key` 里的「来源未知」桶保持原样,不因为引擎侧有数据就把它归给某个引擎。

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |
| `dimension` | `str` | 否 | `"engine"` | 取值:engine / referrer / utm_source / utm_term / utm_content / device / os / browser / country / city |

响应 `list[AcquisitionRow]`:

```
key: str
sessions: int
visitors: int
page_views: int
new_visitors: int
```

## `GET /pages`

页面排行

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |
| `limit` | `int` | 否 | `50` | 范围 1~200 |
| `dimension` | `str` | 否 | `"path"` | 取值:path / title |

响应 `list[PageRow]`:

```
page_path: str    # 维度 key(dimension=title 时为页面标题)
page_views: int
visitors: int
avg_engagement_sec: Optional[float]    # user_engagement 均值;老数据无采集为 None
events: int    # 该页面上所有事件数
```

## `GET /pages_timeseries`

TopN 页面按天

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |
| `top` | `int` | 否 | `5` | 范围 1~10 |

响应 `list[PageDayRow]`:

```
day: date
page_path: str
views: int
```

## `GET /events`

事件名汇总

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `list[EventRow]`:

```
event_name: str
count: int
visitors: int
```

## `GET /bots`

爬虫视角(常规报表已排除爬虫)

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `BotsReport`:

```
bots: list[BotRow]
  bot_name: str
  events: int
  page_views: int
  pages: int    # 抓取过的不同页面数
  last_seen: Optional[str]    # ISO 时间
pages: list[BotPageRow]
  page_path: str
  hits: int    # 该页上的爬虫事件总数
  bots: int    # 抓过该页的不同爬虫数
```

## `GET /engagement`

参与度(互动会话、时长;时长看中位数)

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `Engagement`:

```
sessions: int
engaged_sessions: int
engaged_rate: float
avg_engagement_sec: float
median_engagement_sec: float
pages_per_session: float
days: list[EngagementDay]
  day: date
  engaged_rate: float    # 互动会话占比(0-1)
  avg_engagement_sec: float    # 每会话平均互动秒数(受长尾扭曲,见 Engagement)
  median_engagement_sec: float    # 每会话互动秒数中位数
```

## `GET /conversions`

转化(金额按币种分组,跨币种不相加)

⚠️ 金额按币种分列,**跨币种不相加**;没报币种的不默认成人民币。

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `ConversionsReport`:

```
conversions: int
visitors: int
converting_sessions: int
sessions: int    # 分母:同时段全部非爬虫会话
rate: float    # converting_sessions / sessions
values: list[ConversionValue]
  currency: str    # '' = 客户没报 currency,单列一档,不假定人民币
  value: float
  conversions: int    # 该币种下**带有效金额**的转化数(≠ 该币种全部转化数)
names: list[ConversionNameRow]
  name: str    # conversion_name;客户没报 → '(not set)'
  conversions: int
  visitors: int
  sessions: int
  values: list[ConversionValue]
    currency: str    # '' = 客户没报 currency,单列一档,不假定人民币
    value: float
    conversions: int    # 该币种下**带有效金额**的转化数(≠ 该币种全部转化数)
sources: list[ConversionSourceRow]
  key: str    # 会话来源
  conversions: int
  converting_sessions: int
  sessions: int
  rate: Optional[float]    # 转化会话占比;sessions=0 时为 None,不出 0%
days: list[ConversionDay]
  day: date
  conversions: int
extra_params: list[str]    # 约定三字段以外、客户实际报过的参数键
```

## `GET /realtime`

近 30 分钟滚动窗

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |

响应 `Realtime`:

```
active_visitors: int
active_5min: int
page_views: int
page_views_5min: int
events: list[RealtimeEvent]
  ts: str
  event_name: str
  page_path: Optional[str]
  visitor_id: str
  session_engine: Optional[str]
  nav_site: Optional[str]
  device: Optional[str]
per_minute: list[MinuteRow]
  minute: str    # ISO 分钟(UTC),前端转北京时展示
  page_views: int
locations: list[LocationRow]
  country: Optional[str]    # ISO 码
  region: Optional[str]    # 省级行政区(DataV 标准名,中国地图 key)
  city: Optional[str]
  visitors: int
top_pages: list[NamedCount]    # 30 分钟窗浏览量榜(全量聚合,不受事件流 LIMIT 影响)
  name: str
  value: int
top_events: list[NamedCount]    # 30 分钟窗事件计数榜
  name: str
  value: int
```

## `GET /engines`

引擎侧(应答采样)× 站点侧(实测流量)并排

⚠️ 两列各讲各的事实,**不 join、不暗示因果**。`site_measurable="no"` 是「跳转不留痕,技术上测不到」,**不是 0**;`probes=0` 时各率是 `null`,**也不是 0%**。

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `list[EngineSideRow]`:

```
engine: str
probes: int    # 本期有效应答数(is_valid)
citation_rate: Optional[float]    # 文章引用率 cites_owned/is_valid
exposure_rate: Optional[float]    # 整体露出率(排除 brand/compare)
top3_rate: Optional[float]    # TOP3 露出率 rank≤3/brand_hit
last_probe_at: Optional[str]
site_sessions: int
site_conversions: int
site_measurable: str    # yes / no / untested
```

## `GET /probe-events`

应答采样原始记录(含 answer_text 与 sources)

⚠️ 这是原始记录,**不要自己拿它算指标** —— 要算就调 `/engines`,口径在服务端的 SQL 里。

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |
| `limit` | `int` | 否 | `200` | 范围 -~500 |

响应 `list[ProbeEventOut]`:

```
id: int
event_ts_bj: str
run_id: str
engine: str
query: str
scene_type: str
status: str
is_valid: bool
brand_hit: Optional[bool]
brand_rank: Optional[int]
citation_count: Optional[int]
cites_owned: Optional[bool]
answer_text: Optional[str]
sources: list[ProbeSourceOut]
  source_position: Optional[int]
  source_url: str
  source_domain: Optional[str]
  source_title: Optional[str]
  is_owned: bool
  is_brand_domain: bool
```

## `GET /ivt`

无效流量报表(打标不拦截)

⚠️ 数据质量账,不是安全账:打标不拦截,每条可复核到规则编号。

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `from` | `date` | 是 | — | — |
| `to` | `date` | 是 | — | — |

响应 `IvtReport`:

```
notes: list[IvtNoteCount]
  ivt: int    # 1=GIVT / 2=SIVT
  note: str    # 原因码
  events: int
  sessions: int
daily: list[IvtDay]
  day: date
  total: int    # 当日全部事件(含有效)
  givt: int
  sivt: int
sivt_sessions: list[IvtSession]
  session_id: str
  note: str
  events: int
  pages: int
  first_ts: str
  last_ts: str
  engine: Optional[str]
  device: Optional[str]
  ua: Optional[str]    # 截断展示;08-01 前的历史无 UA
```

## `GET /ivt/session-events`

单会话事件序列(抽查下钻)

参数:

| 名称 | 类型 | 必填 | 默认 | 约束 |
|---|---|---|---|---|
| `tag_id` | `str` | 是 | — | — |
| `session_id` | `str` | 是 | — | — |

响应 `list[IvtSessionEvent]`:

```
event_ts: str
event_name: str
page_path: Optional[str]
ivt: int
ivt_note: Optional[str]
```

