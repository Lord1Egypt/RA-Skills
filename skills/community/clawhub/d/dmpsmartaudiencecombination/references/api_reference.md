# api_reference.md（明日DMP OPENAPI｜本技能用到的端点）

> 本文档用于避免“接口参数/结构靠猜导致幻觉”。
> 
> 说明：本技能只覆盖【组合人群】相关端点与必要的通用端点。

---

## 0. 环境地址
- 测试环境：`https://dmp-dev.mingdata.com`  
- 生产环境：`https://open.mingdata.com`

> 环境选择以项目约定为准。

---

## 1. 鉴权（所有端点通用）
### 1.1 URL Query 参数
调用任意 OPENAPI 时，必须在 URL 上拼接：
- `ts`：10位 Unix 时间戳（**3分钟内有效**）
- `randStr`：4位随机数字
- `accessKey`：应用标识
- `sign`：签名

URL 示例（以人群列表为例）：
```
.../api/open-api/audience/manage/list?ts=1752479467&randStr=1234&accessKey=xxx&sign=XXXXXXXX...
```

### 1.2 sign 计算
- `sign = MD5(ts + randStr + secret_key).upper()`（32位大写）

---

## 2. 标签列表查询（tag/list）
### 2.1 端点
- Method：GET
- Path：`/api/open-api/tag/list`

### 2.2 请求参数
- Query：鉴权参数（ts/randStr/accessKey/sign）
- Body：文档示例中出现 `tagType`（但该端点为 GET，是否支持 body 依赖服务端实现；建议优先不传 body，或作为 query 参数尝试）。

可选字段（若支持）：
| 字段 | 类型 | 说明 |
|---|---|---|
| tagType | integer | 1：明略标签；3：合作伙伴标签 |

### 2.3 响应字段（关键字段）
| 字段 | 类型 | 说明 |
|---|---|---|
| tagId | integer | 标签ID |
| tagName | string | 标签名称 |
| parentId | integer | 父级标签ID |
| tagType | integer | 1明略/3合作伙伴 |
| isDirectory | integer | 0目录 / 1标签（**仅1可用于组合**） |

---

## 3. 创建组合人群（combine/create）
### 3.1 端点
- Method：POST
- Path：`/api/open-api/audience/manage/combine/create`
- Header：`Content-Type: application/json`

### 3.2 Body 字段
| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| name | string | 是 | 人群名称（文档：≤100字符；UI可能更严，按产品侧约束） |
| trackType | string | 是 | MOBILE / PC / OTT |
| idTypes | string[] | 是 | 随 trackType 枚举：MOBILE（MD5_IDFA/MD5_IMEI/MD5_OAID/IDFA/OAID/CAID/MD5_CAID）；PC（MZID）；OTT（MD5_MAC） |
| data | list | 是 | 规则列表（见 3.3） |

### 3.3 data 结构（最重要）
每个元素：
```json
{
  "op": "and | not | noop",
  "rule": {
    "audience": [123456],
    "tag": [14351, 14352]
  }
}
```

**语义约束**：
1) `rule.tag` 或 `rule.audience` 内的多个 ID 为 **OR** 关系。
2) `op` 表示“当前 rule 与下一个 rule 的关系”。
3) **最后一个元素的 op 必须是 `noop`**。

**规模约束**：
- 单个 rule 组：最多 100 个标签/人群数据（tag+audience 合计）。
- 单个组合人群任务：最多 50 个 rule。

**可用性/权限约束**：
- `tag` 仅可使用 `isDirectory=1` 的标签。
- `rule` 中的 `audience/tag` ID 必须与当前应用租户“有权限可用”的 ID 匹配，否则创建失败。

### 3.4 请求示例（简）
含义：`(tag:A) AND NOT (tag:B)`
```json
{
  "name": "示例_组合人群",
  "trackType": "MOBILE",
  "idTypes": ["MD5_OAID"],
  "data": [
    {"op": "not", "rule": {"audience": [], "tag": [111]}},
    {"op": "noop", "rule": {"audience": [], "tag": [222]}}
  ]
}
```

---

## 4. 查询人群任务状态（taskList）
### 4.1 端点
- Method：POST
- Path：`/api/open-api/audience/manage/taskList`
- Header：`Content-Type: application/json`

### 4.2 Body
| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| audienceIds | integer[] | 否 | 需要查询的人群ID列表 |

### 4.3 响应字段（关键字段）
| 字段 | 类型 | 说明 |
|---|---|---|
| audienceId | integer | 人群ID |
| audienceName | string | 人群名称 |
| audienceStatus | integer | 0失败 / 1成功 / 2等待中 / 3计算中 |
| audienceAmount | string | 人群量级（字符串） |
| createTime | string | 创建时间 |

---

## 5. 人群列表查询（manage/list）
### 5.1 端点
- Method：POST
- Path：`/api/open-api/audience/manage/list`

### 5.2 Body（常用过滤字段）
| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| audienceType | integer | 否 | 1上传 2组合 3规则 4拓展 5打通 |
| audienceStatus | integer | 否 | 0失败 1成功 2等待 3计算中 |
| audienceIds | integer[] | 否 | 指定人群ID列表 |
| current | integer | 否 | 页码 |
| pageSize | integer | 否 | 每页条数 |

---

## 6. 错误码与频控
### 6.1 错误码
文档示例中仅出现：
- `code = "0"`：成功
- `code != "0"`：失败（失败原因见 `msg`）

> 更细的错误码枚举表：**文档未覆盖 / 待确认**。

### 6.2 频次限制（Rate Limit）
- API 调用 QPS、并发上限、轮询建议间隔：**文档未覆盖 / 待确认**。

---

## 7. 与本技能脚本的对应关系（便于排查）
- `query_tag_list.py` → tag/list
- `create_combined_crowd.py` / `create_must_baseline.py` / `calc_overlap.py` → combine/create + taskList
- `query_crowd_task.py` → taskList
