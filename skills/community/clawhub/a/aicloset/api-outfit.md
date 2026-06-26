# 搭配与 OOTD API

## POST /skill/outfit/list

查询用户搭配列表，支持分页。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，默认 10 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/outfit/list \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "page=1&page_size=10"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "list": [
      {
        "id": 1,
        "canvas_image": "https://...",
        "canvas_data": "...",
        "created_at": "2026-03-20 10:00:00"
      }
    ],
    "total": 20,
    "page": 1
  }
}
```

---

## POST /skill/outfit/recommend

推荐搭配方案，按使用频率降序排列，最多返回 10 条。

### 请求参数

无需参数。

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/outfit/recommend \
  -H "x-api-key: $AICLOSET_API_KEY"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "list": [
      {
        "id": 1,
        "canvas_image": "https://...",
        "canvas_data": "...",
        "created_at": "2026-03-20 10:00:00"
      }
    ],
    "message": "推荐搭配（按使用频率排序）"
  }
}
```

---

## POST /skill/ootd/record-photo

记录每日穿搭（OOTD），通过上传照片方式。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期，格式 `2006-01-02` |
| image_url | string | 是 | 穿搭照片 URL |
| city | string | 否 | 城市 |
| weather | string | 否 | 天气 |
| temperature | string | 否 | 温度 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/ootd/record-photo \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "date=2026-03-23&image_url=https://example.com/ootd.jpg&city=北京&weather=晴"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "calendar_id": 10,
    "date": "2026-03-23"
  }
}
```

---

## POST /skill/ootd/record-outfit

记录每日穿搭（OOTD），关联已有搭配方案。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期，格式 `2006-01-02` |
| outfit_id | string | 是 | 搭配 ID |
| city | string | 否 | 城市 |
| weather | string | 否 | 天气 |
| temperature | string | 否 | 温度 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/ootd/record-outfit \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "date=2026-03-23&outfit_id=5&city=北京&weather=晴"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "calendar_id": 11,
    "date": "2026-03-23",
    "outfit_id": "5"
  }
}
```
