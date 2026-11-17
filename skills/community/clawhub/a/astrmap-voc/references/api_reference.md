# AstrMap API 参考文档

## 概述

本文档详细介绍 AstrMap 开放 API 的所有端点、请求格式、响应格式和错误码。

> 真相源：本文档字段以服务端 `server/src/api/v1/routes/route_external.py` 与其对应服务实现为准。

## 认证方式

所有 API 请求需要在 HTTP 头中携带认证信息：

```
Authorization: Bearer {api_key}
Content-Type: application/json
```

> 注意：API Key 格式为 `sk_live_xxxxxxxxxxxxxxxx`

---

## 端点清单

### 1. 端点在线查询

**端点**: `POST /api/v1/external/device/status`

查询当前 API Key 绑定的用户端点是否在线。

> 说明（v2.2）：底层模型已从 `device` 迁移为 `client_endpoint`。响应字段已对齐
> 新命名（`online` → `is_alive`、`device_id` → `endpoint_id`，新增 `endpoint_type`）。

**请求体**:
```json
{}
```

**响应（在线）**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "is_alive": true,
    "endpoint_id": "endpoint_xxx",
    "endpoint_type": "desktop",
    "status": "idle"
  }
}
```

**响应（离线）**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "is_alive": false,
    "endpoint_id": null,
    "endpoint_type": null,
    "status": "offline"
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| is_alive | bool | 端点是否在线 |
| endpoint_id | string \| null | 端点 ID（离线时为 null） |
| endpoint_type | string \| null | 端点类型：`desktop` / `extension` / `web_session` |
| status | string | 端点状态：`idle` / `busy` / `offline` |

---

### 2. 创建任务

**端点**: `POST /api/v1/external/task/create`

创建任务，下发到当前账号绑定的设备。

**请求体**:
```json
{
  "platform": "amazon",
  "site": "US",
  "submit_content": "B09V3KXJPB",
  "is_auto": true
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| platform | 否 | amazon | 平台名称 |
| site | 否 | US | 站点 |
| submit_content | 是 | - | 输入内容，支持 URL 或 ASIN |
| is_auto | 否 | true | 是否自动模式，true=自动分析，false=仅采集 |

**站点说明**:
| site | 语言 |
|------|------|
| US | 英语 |
| CA | 英语 |
| UK | 英语 |
| DE | 德语 |
| FR | 法语 |
| IT | 意大利语 |
| ES | 西班牙语 |
| JP | 日语 |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx"
  }
}
```

> 提示：创建接口仅返回 `task_id`；如需任务名称/状态等其它字段，请随后调用 `POST /task/detail`。

---

### 3. 任务状态查询

**端点**: `POST /api/v1/external/task/detail`

查询任务详情和状态。

**请求体**:
```json
{
  "task_id": "TSK_xxx"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "TSK_xxx",
    "user_id": "user_xxx",
    "name": "任务名称",
    "status": "SUCCESS",
    "platform": "amazon",
    "site": "US",
    "submit_content": "B09V3KXJPB",
    "parse_content": ["B09V3KXJPB"],
    "create_time": "2025-03-22 10:30:00",
    "update_time": "2025-03-22 10:35:00",
    "monitoring": false,
    "is_auto": true
  }
}
```

**任务状态说明**:
| 状态 | 说明 |
|------|------|
| PENDING | 待处理 |
| DISPATCHING | 分发中 |
| COLLECTING | 采集中 |
| COLLECTED | 采集完成（仅 `is_auto=false` 会停在此状态） |
| PROCESSING | 处理中 |
| ANALYZING | 分析中 |
| SUCCESS | 完成 |
| FAILED | 失败 |
| CANCELLED | 已取消 |

---

### 4. 任务列表查询

**端点**: `POST /api/v1/external/task/list`

查询任务列表。

**请求体**:
```json
{
  "page": 1,
  "page_size": 20,
  "search_keyword": "B09",
  "filter_monitoring": false
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| page | 否 | 1 | 页码（等同于 `current_page`） |
| page_size | 否 | 10 | 每页数量（上限 100） |
| search_keyword | 否 | "" | 搜索关键词（匹配任务名/ASIN） |
| filter_monitoring | 否 | false | 是否只返回监控中的任务 |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total": 100,
    "page_max": 5,
    "page": 1,
    "page_size": 20,
    "filter_monitoring": false,
    "search_keyword": "B09",
    "items": [
      {
        "id": "TSK_xxx",
        "name": "任务名称",
        "status": "SUCCESS",
        "platform": "amazon",
        "site": "US",
        "asin_count": 1,
        "total_reviews": 335,
        "negative_reviews": 169,
        "create_time": "2026-07-05 22:33",
        "update_time": "2026-07-05 23:28",
        "monitoring": false
      }
    ]
  }
}
```

> 与 `/task/detail` 的差异：列表 items 是**精简版**（含数量汇总 `asin_count/total_reviews/negative_reviews`，**不含** `submit_content / parse_content / is_auto / user_id`）。如需完整字段，用 `/task/detail` 单查。

> ⚠️ **常见误读警示**：`negative_reviews` 字段的**取值语义随 `status` 而变**——
> - `status="SUCCESS"` 时：`negative_reviews=0` 表示 AI 分析确认**真无差评**
> - `status="COLLECTED"` / `PENDING` / `DISPATCHING` / `COLLECTING` 时：AI 尚未跑，字段固定为 `0`，**不等于**无差评
>
> AI Agent 使用此字段做筛选/排序前**必须先判断 `status`**，避免把"未分析"当"零差评好产品"。

> 排序规则（实测）：默认按 `update_time` 倒序，不是 `create_time`——最近有增量/分析/重命名的任务会排在最前。

---

### 4.1 增量获取

**端点**: `POST /api/v1/external/task/incremental`

为**已就绪任务**（SUCCESS / CANCELLED / COLLECTED）创建增量获取，获取自上次获取后的新增评论。FAILED 状态**不允许**增量。

**请求体**:
```json
{
  "task_id": "TSK_xxx"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID；必须处于允许状态：`SUCCESS` / `CANCELLED` / `COLLECTED`（**不含 FAILED**） |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx",
    "job_id": "JOB_xxx"
  }
}
```

**适用场景**：
- 已完成的任务需要更新最新评论数据
- 与创建新任务的区别：输入是已有的任务 ID（无需重复输入 ASIN），自动获取增量
- 增量获取会触发完整的获取+分析流程，数据分析会扣除积分

---

### 4.2 任务重命名

**端点**: `POST /api/v1/external/task/rename`

重命名任务。仅更新任务显示名称，不修改其它字段或状态。

**请求体**:
```json
{
  "task_id": "TSK_xxx",
  "name": "新任务名称"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |
| name | 是 | 新任务名称 |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "TSK_xxx"
  }
}
```

> 提示：接口仅返回被更新的任务 ID。如需完整任务字段，请随后调用 `POST /task/detail`。

**说明**：
- 任务必须归属当前账号（服务端强制归属校验）
- 不扣积分，无前置条件

**错误码**（服务端内部 code，响应外传时会被统一包装为 HTTP 400 + `detail.code = -1`，具体判断请匹配 msg 关键词；详见文末"错误处理契约"）:
| 服务端内部 code | 典型 msg |
|------|-------------|
| MissingRequiredParam | 未提供任务ID |
| VALIDATION_ERROR | 验证失败（缺少 name 或全部更新字段为空） |
| TaskNotFound | 找不到任务或权限不足 |
| TaskUpdateError | 更新任务失败 |

---

### 4.3 手动触发分析

**端点**: `POST /api/v1/external/task/{task_id}/trigger-analysis`

手动触发仅采集任务的 AI 分析流程。适用于 `is_auto=false` 的任务，采集完成后停在 COLLECTED 状态，需要手动触发 AI 分析。

**路径参数**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID，任务状态必须为 COLLECTED |

**请求体**:
```json
{}
```

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx",
    "job_id": "JOB_xxx"
  }
}
```

**触发后状态流转**：`COLLECTED` → `PROCESSING` → `ANALYZING` → `SUCCESS`

**错误码**（服务端内部 code；外传时统一为 HTTP 400 + `detail.code = -1`，详见文末"错误处理契约"）:
| 服务端内部 code | 典型 msg |
|------|------|
| MissingTaskId | 未提供任务 ID |
| TaskNotFound | 任务不存在 |
| InvalidTaskStatus | 任务状态不是 COLLECTED，无法触发分析 |
| JobNotFound | 关联 Job 不存在 |
| JobStatusUpdateFailed | 更新 Job 状态失败 |

---

### 4.4 浏览器扩展下载配置

**端点**: `GET /download-config.json`

这是一个公开的配置文件（无需 API Key 认证），用于获取浏览器扩展的下载链接。
注：网站已不再提供桌面客户端下载，`downloads` 中现仅有 `extension` 一项。

**响应**:
```json
{
  "version": "1.5.1",
  "last_updated": "2026-09-19T00:00:00Z",
  "downloads": {
    "extension": {
      "name_zh": "Chrome 扩展",
      "name_en": "Chrome Extension",
      "url": "<实际下载地址>",
      "version": "0.6.11",
      "size": "150.8 KB",
      "requirements": {
        "min_chrome_version": "88"
      }
    }
  }
}
```

---

### 5. AI 洞察查询

**端点**: `POST /api/v1/external/analysis/insights`

获取 AI 洞察结果。按 **三大场景**（competitor / improvement / marketing）平铺返回，每个场景下是若干 `insight_type → content(纯字符串)` 的键值对。

**请求体**:
```json
{
  "task_id": "TSK_xxx"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "competitor_insights": {
      "<insight_type_a>": "<洞察正文字符串>",
      "<insight_type_b>": "..."
    },
    "improvement_insights": {
      "<insight_type_x>": "...",
      "<insight_type_y>": "..."
    },
    "marketing_insights": {
      "<insight_type_1>": "...",
      "<insight_type_2>": "..."
    }
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| competitor_insights | object | 竞品分析场景的洞察（键为 insight_type，值为洞察正文纯字符串） |
| improvement_insights | object | 产品改进场景的洞察 |
| marketing_insights | object | 营销文案场景的洞察 |

> 数据缺失时三个字段均返回 `{}`（空对象）。`insight_type` 键名由服务端 AI 生成流水线定义，可能随版本演进而扩充；调用方应按"存在即读取、缺失即跳过"处理，不要硬编码具体 key。

**典型 insight_type 参考清单**（截至 2026-07 实测；不承诺完整/固定，仅供了解结构）:

| 场景 | 常见 insight_type |
|------|------------------|
| competitor_insights | `executive_summary` / `key_strength` / `key_problem` / `strategy_guide` |
| improvement_insights | `executive_summary` / `key_strength` / `key_problem` / `recommendation` / `priority_ranking` / `root_cause` |
| marketing_insights | `executive_summary` / `key_strength` / `word_of_mouth` / `material_library` |

---

### 6. 分类标签分布查询

**端点**: `POST /api/v1/external/analysis/category-tag-distribution/{task_id}`

获取分类标签分布——**三层嵌套结构**（Dimension → Category → Tags）。支持 polarity 参数筛选（negative/positive/all）。

**路径参数**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |

**请求体**:
```json
{
  "polarity": "negative"
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| polarity | 否 | negative | 极性筛选：`negative` / `positive` / `all` |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "category_tag_distribution": {
      "polarity": "negative",
      "dimensions": {
        "product": {
          "total_count": 42,
          "total_rate": "28.0%",
          "categories": {
            "quality": {
              "total_count": 20,
              "total_rate": "13.3%",
              "tags": [
                {"tag": "做工问题", "count": 12, "rate": "8.0%"},
                {"tag": "外观瑕疵", "count": 8, "rate": "5.3%"}
              ]
            }
          }
        },
        "service": { "total_count": 15, "total_rate": "10.0%", "categories": { "...": {} } },
        "experience": { "total_count": 8, "total_rate": "5.3%", "categories": { "...": {} } }
      }
    }
  }
}
```

> ⚠️ 注意：`data` 顶层套了一层 `category_tag_distribution` 键，实际数据从 `data.category_tag_distribution.dimensions` 开始读。

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| category_tag_distribution.polarity | string | 请求时的 polarity 参数原样回显 |
| category_tag_distribution.dimensions | object | 三维模型（`product` / `service` / `experience`）→ Category → Tags |
| dimensions.*.total_count | int | 该维度评论数 |
| dimensions.*.total_rate | string | 该维度评论占比（百分号字符串） |
| dimensions.*.categories | object | 分类映射 |
| dimensions.*.categories.*.tags | array | 该分类下的标签列表，含 `tag / count / rate` |

> 无数据时 `dimensions` 为空对象 `{}`。

---

### 7. 基础统计查询

**端点**: `POST /api/v1/external/analysis/statistics`

获取基础统计数据（评论总数、正负评数量与占比、最后分析时间）。

**请求体**:
```json
{
  "task_id": "TSK_xxx"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total_comments": 150,
    "negative_comments": 23,
    "negative_rate": "15.33%",
    "positive_comments": 120,
    "positive_rate": "80.0%",
    "last_analyzed_at": "2025-03-22 10:35"
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| total_comments | int | 评论总数 |
| negative_comments | int | 差评数量 |
| negative_rate | string | 差评占比（百分号字符串） |
| positive_comments | int | 好评数量 |
| positive_rate | string | 好评占比（百分号字符串） |
| last_analyzed_at | string | 最后分析时间（`YYYY-MM-DD HH:MM`，无数据时为空串） |

> 若任务从未分析，本接口不会失败，会返回全零结构且 `last_analyzed_at` 为空字符串。

> ⚠️ **正负评占比不互斥（重要语义）**：`positive_rate + negative_rate` **允许 > 100%**（实测 62.4% + 50.4% = 112.8%）。原因是 AstrMap 的语义分类**不是互斥二分类**——同一条评论可以**同时**包含正面情感（如"产品耐用"）和负面情感（如"物流慢"），两侧同时计数。**因此 `total_comments - negative_comments ≠ positive_comments`**，不能用减法推算，两个字段各自独立读取。

---

### 8. 代表性评论查询

**端点**: `POST /api/v1/external/analysis/representative-reviews`

获取代表性评论（按维度已选出的 Top-N 典型评论）。

**请求体**:
```json
{
  "task_id": "TSK_xxx",
  "polarity": "negative",
  "limit": 5
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| task_id | 是 | - | 任务 ID |
| polarity | 否 | negative | 极性筛选：`negative` / `positive` |
| limit | 否 | 5 | 单维度返回数量上限（实测建议 ≤ 5） |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": "AMAZON_R28FJKGLXXQJCQ",
        "content": "评论正文...",
        "title": "评论标题",
        "star": "1",
        "time": "2026-06-15",
        "reviewer": "Peyton",
        "avatar": "https://images-na.ssl-images-amazon.com/...",
        "region": "the United States",
        "is_purchase": true,
        "helpful_votes": 3,
        "images": [],
        "dimension": "product",
        "dimension_name": "产品",
        "rank_in_dimension": 1,
        "url": "https://www.amazon.com/..."
      }
    ]
  }
}
```

**items 字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 评论 ID |
| content | string | 评论正文 |
| title | string | 评论标题 |
| star | string | 评分（字符串形式的数字） |
| time | string | 评论时间 |
| reviewer | string | 评论者昵称 |
| avatar | string | 评论者头像 URL |
| region | string | 评论者地区 |
| is_purchase | bool | 是否已购买 |
| helpful_votes | int / string | 有用票数 |
| images | array | 评论图片列表 |
| dimension | string | 所属维度：`product` / `service` / `experience` |
| dimension_name | string | 维度中文名 |
| rank_in_dimension | int | 该评论在其维度内的排名（1 为第一名） |
| url | string | 评论原链接 |

> 说明：`limit` 是**每个维度**返回上限；三个维度合并后 items 数量最多 = `3 × limit`。

---

### 9. 情感评论列表查询

**端点**: `POST /api/v1/external/analysis/sentiment-reviews`

获取情感评论列表——**同一端点支持差评 / 好评双向查询**，通过 `polarity` 参数切换。

> 兼容说明：`POST /api/v1/external/analysis/negative-reviews` 是本端点的历史别名（自动设置 `polarity="negative"`），行为完全一致。**新代码应统一使用 `/sentiment-reviews` + polarity**。

**请求体**:
```json
{
  "task_id": "TSK_xxx",
  "polarity": "negative",
  "page": 1,
  "page_size": 20
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| task_id | 是 | - | 任务 ID |
| polarity | 否 | negative | 极性：`negative` / `positive` |
| page | 否 | 1 | 页码 |
| page_size | 否 | 10 | 每页数量（上限 100） |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": "AMAZON_R28FJKGLXXQJCQ",
        "review_title": "评论标题",
        "review_content": "评论正文...",
        "review_star": "5",
        "review_time": "2026/06/15",
        "reviewer": "Peyton",
        "review_region": "the United States",
        "is_purchase": true,
        "review_vote": "0",
        "review_images": [],
        "review_videos": [],
        "asin": "B0C3L93F2Q",
        "tags": ["使用体验极佳", "兼容性好", "外观设计美观"],
        "normalized_tags": ["使用体验好", "兼容性好", "外观美观"]
      }
    ],
    "total": 226,
    "page": 1,
    "page_size": 20,
    "page_max": 12
  }
}
```

**⚠️ 好评侧关键陷阱**（实测 2026-06-23）：
- `polarity="positive"` 的 items **可能混入少量 1★/2★** 评论——服务端按 AI 综合情感切分而非 `review_star` 单值
- 做频次榜/文案摘录前**必须过滤 `review_star >= 4`**

**Python 调用**:
```python
from api_client import CustomerInsightsClient
client = CustomerInsightsClient(api_key="sk_live_...")

neg = client.get_sentiment_reviews(tid, polarity="negative", page=1, page_size=50)
pos = client.get_sentiment_reviews(tid, polarity="positive", page=1, page_size=50)
```

---

### 10. 评论趋势查询

**端点**: `POST /api/v1/external/analysis/trend`

获取每日评论趋势（以最新评论日期为锚点回溯 N 天）。

**请求体**:
```json
{
  "task_id": "TSK_xxx",
  "filter_data": "30",
  "filter_polarity": "all"
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| task_id | 是 | - | 任务 ID |
| filter_data | 否 | 30 | 回溯天数（`1-365`；越界或非法值自动回退到 30） |
| filter_polarity | 否 | all | 极性筛选：`all` / `negative` / `positive`（影响返回表头列数） |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "trend_reviews": {
      "source": [
        ["日期", "评论总数", "差评数量", "好评数量"],
        ["2025-03-01", 50, 8, 42],
        ["2025-03-02", 47, 6, 41]
      ],
      "filter_product_options": {"all": "全部商品"},
      "filter_data_options": {
        "30": "最近30天",
        "60": "最近60天",
        "90": "最近90天"
      }
    },
    "filter_product_options": {"all": "全部商品"},
    "filter_data_options": {
      "30": "最近30条",
      "60": "最近60条",
      "90": "最近90条"
    }
  }
}
```

**表头列数按 `filter_polarity` 变化**:
| filter_polarity | source 表头 |
|---|---|
| all（默认） | `["日期", "评论总数", "差评数量", "好评数量"]` |
| negative | `["日期", "评论总数", "差评数量"]` |
| positive | `["日期", "评论总数", "好评数量"]` |

> 无数据时 `trend_reviews.source` 仅包含表头行。

> ⚠️ **实际数据点数 ≤ N 天**：`filter_data=30` 是"以任务最新评论日期为锚点，回溯 30 天"，但**没有评论的日期会被跳过**（不返回 0-count 占位行）。实测 30 天窗口内可能只有 18 个数据点，取决于产品评论活跃度。前端画图时若需要连续时间轴，需自行补齐缺失日期为 0。

---

### 11. 原始评论概览查询

**端点**: `POST /api/v1/external/analysis/comments-overview`

获取原始评论的概览统计（评分分布、内容类型分布）。

**请求体**:
```json
{
  "task_id": "TSK_xxx"
}
```

**参数说明**:
| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 是 | 任务 ID |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx",
    "total_reviews": 335,
    "average_rating": 4.2,
    "star_distribution": [
      {"rating": 5, "count": 200, "percentage": 60},
      {"rating": 4, "count": 60,  "percentage": 18},
      {"rating": 3, "count": 30,  "percentage": 9},
      {"rating": 2, "count": 25,  "percentage": 7},
      {"rating": 1, "count": 20,  "percentage": 6}
    ],
    "content_type_data": [
      {"type": "text_only",  "name": "仅文本", "count": 329},
      {"type": "with_image", "name": "带图片", "count": 0},
      {"type": "with_video", "name": "带视频", "count": 6}
    ],
    "last_update_time": "2025-03-22 10:35:00"
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务 ID（回显） |
| total_reviews | int | 评论总数 |
| average_rating | float | 平均评分 |
| star_distribution | array | 评分分布数组，元素含 `rating / count / percentage`（**注意：字段名是 `rating` 不是 `star`；含百分比字段 `percentage`**） |
| content_type_data | array | 内容类型分布**数组**（非对象），元素含 `type / name / count`；`type` 取值：`text_only` / `with_image` / `with_video` |
| last_update_time | string | 最后更新时间 |

**错误码**（返回时被统一包装为 HTTP 400，具体 code 值参见文末"错误处理契约"）:
| 服务端内部 code | 说明 |
|------|------|
| TaskNotFound | 任务不存在 |
| AccessDenied | 无权访问该任务 |
| GetReviewStatisticsError | 获取评论统计失败 |
| GetContentTypeStatisticsError | 获取内容类型统计失败 |

---

### 12. 原始评论列表查询

**端点**: `POST /api/v1/external/analysis/comments`

获取原始评论列表（支持评分/内容类型/商品/认证多维筛选）。

**请求体**:
```json
{
  "task_id": "TSK_xxx",
  "page": 1,
  "page_size": 20,
  "filter_star": "all",
  "filter_verified": "all",
  "filter_content_type": "all",
  "filter_product": "all",
  "search_keyword": "",
  "sort_field": "latest"
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| task_id | 是 | - | 任务 ID |
| page | 否 | 1 | 页码（等同于 `current_page`） |
| page_size | 否 | 20 | 每页数量（上限 100） |
| filter_star | 否 | all | 评分筛选：`1` / `2` / `3` / `4` / `5` / `all` |
| filter_verified | 否 | all | 认证购买筛选：`all` / `true` / `false` |
| filter_content_type | 否 | all | 内容类型筛选：`all` / `text_only` / `with_image` / `with_video` |
| filter_product | 否 | all | ASIN 筛选（精确匹配 ASIN 或 `all`） |
| search_keyword | 否 | "" | 关键词搜索 |
| sort_field | 否 | latest | 排序：`latest` / 其它由服务端支持的字段 |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": "AMAZON_R28FJKGLXXQJCQ",
        "review_time": "2026-06-15",
        "asin": "B0C3L93F2Q",
        "reviewer": "Peyton",
        "is_purchase": true,
        "review_star": 5,
        "review_title": "评论标题",
        "review_content": "评论正文...",
        "content_type": "text_only",
        "review_url": "https://www.amazon.com/...",
        "review_vote": "0",
        "review_region": "the United States",
        "variant": ""
      }
    ],
    "total": 150,
    "page": 1,
    "page_size": 20,
    "page_max": 8,
    "filter_product_options": {"all": "全部商品", "B0C3L93F2Q": "B0C3L93F2Q"}
  }
}
```

> `filter_product_options` 仅在**第一页**返回（用于前端渲染 ASIN 筛选下拉），后续页为空。

**`content_type` 取值**：`text_only` / `with_image` / `with_video`

**错误码**（服务端内部 code；外传时统一为 HTTP 400 + `detail.code = -1`，详见文末"错误处理契约"）:
| 服务端内部 code | 说明 |
|------|------|
| InvalidPaginationParams | 无效的分页参数 |
| TaskNotFound | 任务不存在 |
| AccessDenied | 无权访问该任务 |
| GetCommentsListError | 获取评论列表失败 |

---

### 13. 获取相关评论

**端点**: `POST /api/v1/external/analysis/related-comments`

按**标签**或**分类**维度钻取评论。`association_type` 决定使用哪个子模式。

**请求体（tag 模式）**:
```json
{
  "task_id": "TSK_xxx",
  "association_type": "tag",
  "normalized_tag": "物流问题",
  "category": "service",
  "polarity": "negative",
  "current_page": 1,
  "page_size": 20
}
```

**请求体（category 模式）**:
```json
{
  "task_id": "TSK_xxx",
  "association_type": "category",
  "dimension": "product",
  "category": "quality",
  "polarity": "negative",
  "current_page": 1,
  "page_size": 20
}
```

**参数说明**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| task_id | 是 | - | 任务 ID |
| association_type | 是 | - | 关联类型：`tag` / `category`（**不支持 `issue`**） |
| normalized_tag | tag 模式 | - | 归一化后的标签名 |
| category | 可选 | - | 分类；`category` 模式下服务端会内部映射为 `issue_type` 过滤 |
| dimension | category 模式 | - | 三维之一：`product` / `service` / `experience` |
| polarity | 否 | negative | 极性：`negative` / `positive` / `all` |
| current_page | 否 | 1 | 页码（也可用 `page`） |
| page_size | 否 | 20 | 每页数量 |
| sort_field | 否 | - | 排序字段（由服务端支持） |

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": "AMAZON_R28FJKGLXXQJCQ",
        "content": "评论正文...",
        "title": "评论标题",
        "rating": 1,
        "review_time": "2026-06-15",
        "reviewer": "Peyton",
        "verified_purchase": true,
        "helpful_votes": 3,
        "total_votes": 5,
        "images": [],
        "videos": [],
        "tags": ["下巴带子问题"],
        "variant": "",
        "asin": "B0C3L93F2Q",
        "platform": "amazon",
        "dimension": "experience",
        "issue_type": null
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20,
    "page_max": 3,
    "association_type": "tag",
    "task_id": "TSK_xxx"
  }
}
```

**items 字段说明**（**注意与 §12/§9 命名风格不同**——本接口使用 `rating / verified_purchase / content / title` 而非 `review_star / is_purchase / review_content / review_title`）:

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 评论 ID |
| content | string | 评论正文 |
| title | string | 评论标题 |
| rating | int / null | 评分（1-5，可能为 null） |
| review_time | string | 评论时间 |
| reviewer | string | 评论者昵称 |
| verified_purchase | bool | 是否已认证购买 |
| helpful_votes | int | 有用票数 |
| total_votes | int | 总票数 |
| images | array | 图片 URL 列表 |
| videos | array | 视频 URL 列表 |
| tags | array | 原始标签列表 |
| variant | string | 商品变体 |
| asin | string | ASIN |
| platform | string | 平台 |
| dimension | string | 所属维度（category 模式下必有） |
| issue_type | string / null | 问题类型（category 模式下可能有值） |

> ⚠️ **字段命名不一致的现实**：本接口的 items 字段风格与 `/analysis/comments` / `/analysis/sentiment-reviews` 不同——本接口用 `rating / verified_purchase / content / title`，那两个接口用 `review_star / is_purchase / review_content / review_title`。这是历史遗留（不同 CRUD 源），文档如实记录，请调用方按接口使用对应命名。tag 模式和 category 模式返回结构一致。

---

### 14. 商品信息查询

**端点**: `POST /api/v1/external/product/detail`

获取商品信息（完整字段，含 bullets / product_description / A+ 图片，供 Agent 二次分析）。

两种查询方式（二选一）：
- **task_id**：按任务查，返回该任务下所有商品
- **asin + site**：按商品直查，无需先建任务

**请求体（方式一）**:
```json
{
  "task_id": "TSK_xxx"
}
```

**请求体（方式二）**:
```json
{
  "asin": "B0XXXXXXXX",
  "site": "US",
  "platform": "amazon"
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | string | 与 asin 二选一 | 按任务查，返回该任务下所有商品 |
| asin | string | 与 task_id 二选一 | 按商品直查 |
| site | string | 否（asin 直查时建议传） | 站点码，默认 `US` |
| platform | string | 否 | 平台，默认 `amazon` |

**响应**:
```json
{
  "code": 0,
  "msg": "获取 1 个商品信息",
  "data": {
    "asin": "B0XXXXXXXX",
    "site": "US",
    "queried_by": "asin",
    "products": [
      {
        "asin": "B0XXXXXXXX",
        "site": "US",
        "product_title": "...",
        "brand": "...",
        "image_main": "https://...",
        "rating_average": 4.3,
        "rating_count": 1250,
        "rating_distribution": {"5": 62, "4": 18, "3": 8, "2": 5, "1": 7},
        "rating_health": "healthy",
        "category_path": "...",
        "category_levels": 4,
        "category_node_ids": [...],
        "category_leaf_id": "...",
        "price_current": 29.99,
        "price_original": 39.99,
        "price_discount": 25,
        "price_off_amount": 10.0,
        "currency": "USD",
        "bullets": ["卖点1", "卖点2", "..."],
        "product_description": "...或 null（见下方提示）",
        "has_aplus_content": false,
        "aplus_image_urls": null,
        "availability": "In Stock",
        "date_first_available": "2024-01-15",
        "featured_badge": null,
        "is_active": true,
        "fetched_at": "..."
      }
    ]
  }
}
```

**响应字段说明**:
| 字段 | 说明 |
|------|------|
| queried_by | `task_id` 或 `asin`，标识本次查询方式 |
| rating_distribution | 5→1 星占比（key 为字符串数字）；无数据时为 `null` |
| rating_health | 口碑健康度：`healthy`（5星≥80%）/ `polarized`（5星≥40% 且 1星≥10%，平均分掩盖两极分化）/ `poor`（5星<40%）/ `moderate`；无法计算时为 `null` |
| price_off_amount | 派生字段：`price_original - price_current`（任一缺失则为 `null`） |
| bullets / product_description / aplus_image_urls | 完整返回，供「差评 vs 卖点」语义对齐等二次分析 |

> ⚠️ **归属校验（asin 直查）**：product 表按 `(platform, site, asin)` 全局存储、无 user_id。
> asin 直查要求该 ASIN 出现在**当前用户某个任务**的 `parse_content` 中，否则返回
> `PRODUCT_NOT_ACCESSIBLE`（防止跨用户数据泄露）。
>
> 提示：`product_description` 可能为 `null` 且**不代表采集失败**——品牌备案卖家常把描述
> 做成纯图片（A+ 内容），此时 `has_aplus_content=true`，可展示 `aplus_image_urls`。

**错误码**:
| 内部 code | 典型 msg |
|------|-------------|
| INVALID_TASK_ID_ERROR | 请提供 task_id 或 asin |
| MISSING_REQUIRED_PARAM | 缺少必需参数 |
| PRODUCT_NOT_ACCESSIBLE | 无权访问该商品信息（该 ASIN 不在您的任何任务中） |

---

### 15. 积分余额查询

**端点**: `POST /api/v1/external/account/points`

查询当前账号可用积分总额（所有来源汇总：订阅 + 购买 + 赠送 + 补偿）。

**请求体**:
```json
{}
```

**响应**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "available_points": 1000
  }
}
```

---

## 错误处理契约

### 统一失败响应格式

所有业务失败响应的**真实结构**（实测 2026-07-06）：

- **HTTP 状态码**：一律 `400`（不区分未认证/未找到/参数错误——全部 400）
- **响应体**：外层被 FastAPI `HTTPException.detail` 包裹一层：

```json
{
  "detail": {
    "code": -1,
    "msg": "<中文错误消息>",
    "data": null
  }
}
```

**⚠️ 关键契约事实**：
1. **`code` 恒为 `-1`**——服务端内部的字符串错误码（`TaskNotFound / VALIDATION_ERROR / InvalidTaskStatus` 等）**不会通过响应外传**，仅出现在服务端日志中
2. 调用方**无法通过 `code` 编程式区分错误类型**，必须靠 `msg` 关键词匹配
3. 成功响应是**平铺**结构 `{code, msg, data}`；失败响应是**内嵌**结构 `{detail: {code, msg, data}}`——调用方在解析前应先判断 HTTP 状态码

### 建议的错误处理模式

```python
import requests

resp = requests.post(url, headers=headers, json=payload)
if resp.status_code == 400:
    err = resp.json().get("detail", {})
    msg = err.get("msg", "")
    if "API Key" in msg or "认证" in msg:
        # 认证/授权类错误
        ...
    elif "找不到任务" in msg or "任务不存在" in msg:
        # 任务不存在或越权
        ...
    elif "状态" in msg:
        # 任务状态不允许当前操作
        ...
    else:
        # 其它业务错误
        raise Exception(f"API 调用失败: {msg}")
elif resp.status_code == 429:
    # 触发限流
    retry_after = resp.headers.get("Retry-After", "60")
    ...
else:
    data = resp.json().get("data")
```

### 常见错误 msg 关键词参考

按语义分组，供 `msg` 关键词匹配参考。这些是**服务端内部错误分类**在日志中的常量名，虽不会出现在响应里，但对应的中文 msg 会：

| 服务端内部 code | 典型 msg | 触发场景 |
|---|---|---|
| MISSING_API_KEY | 认证失败: 缺少 API Key | 请求头未带 `Authorization: Bearer` |
| INVALID_API_KEY | 认证失败: 无效的 API Key: API Key 不存在 | API Key 值错误或已删除 |
| API_KEY_EXPIRED | API Key 已过期 | Key 超过 `expires_at` |
| API_KEY_DISABLED | API Key 已禁用 | 用户主动禁用 |
| API_KEY_READ_ONLY | API Key 为只读模式 | 只读 Key 尝试写操作（create/rename/incremental/trigger） |
| MISSING_REQUIRED_PARAM | - | 缺少必需参数（task_id 等） |
| VALIDATION_ERROR | 验证失败 | 参数校验不通过（如 rename 缺 name） |
| INVALID_PARAMETER | 无效参数 | 参数值非法 |
| TaskNotFound | 找不到任务或权限不足: TSK_xxx | 任务不存在或不属于当前账号 |
| InvalidTaskStatus | 只有待分析状态的任务可以触发分析，当前状态: xxx | trigger-analysis 时任务非 COLLECTED |
| InvalidTaskStatus | 只有成功/已取消/待分析状态的任务才能进行增量获取 | incremental 时任务状态不在 SUCCESS/CANCELLED/COLLECTED |
| InvalidPaginationParams | 无效的分页参数 | comments 列表 page/page_size 非法 |
| AccessDenied | 无权访问该任务 | 任务不属于当前账号（部分接口用此码） |
| INSUFFICIENT_POINTS | 积分余额不足 | 分析类操作扣积分失败 |
| DEVICE_NOT_FOUND | 设备未找到 | 端点未绑定或不在线（部分接口） |
| PRODUCT_NOT_ACCESSIBLE | 无权访问该商品信息（该 ASIN 不在您的任何任务中） | asin 直查商品信息时，该 ASIN 不在当前用户的任何任务中 |
| API_RATE_LIMIT | 请求过于频繁，请稍后再试 | 触发速率限制（默认 100/min） |
| UNKNOWN | 未知错误，请稍后重试 | 兜底 |

> 完整字符串常量集中定义在服务端 `configs/config_domain/infrastructure/config_error_codes.py`，但**不作为对外契约**——上表仅供理解服务端错误分类语义。

---

## 速率限制

- 默认限制：100 次/分钟
- 超出限制时 `code` 返回 `API_RATE_LIMIT`，并在响应头 `Retry-After` 中给出退避时间

---

## 常见问题

### 积分规则

- **创建任务（自动模式）**：免费获取亚马逊评论，AI 分析会扣除账户积分
- **创建任务（仅采集模式）**：免费获取亚马逊评论，不扣除积分
- **增量获取**：获取最新评论并重新分析，扣除积分
- **查询结果**：查看已完成任务的分析结果，不扣积分，也无前置条件限制

### 前置条件（仅创建任务时需要）

创建任务前，需确保满足以下条件：

1. 采集通道在线（Chrome 扩展已安装并连接）
2. 已在浏览器中登录亚马逊买家账号（勿使用正在做业务的卖家账号）
3. 确保亚马逊访问畅通

### 错误处理建议
1. 端点不在线（`is_alive: false` 或 msg 含“设备”）：提示用户安装并登录浏览器扩展
2. 积分不足（msg 含"积分"）：提示用户充值积分
3. API Key 无效（HTTP 400 + msg 含"API Key"）：检查 API Key 是否正确
4. 写操作被拒（msg 含"只读"）：只读 Key 不能创建任务/触发分析/增量/重命名
5. **通用规则**：所有失败均为 `HTTP 400 + {detail: {code: -1, msg, data: null}}`；靠 `msg` 关键词区分（详见"错误处理契约"章节）
