# API 参考文档 — 36kr AI 测评笔记

## 接口基础信息

| 属性 | 值 |
|------|----|
| Base URL | `https://openclaw.36krcdn.com` |
| 路径模板 | `/media/ainotes/{date}/ai_notes.json` |
| 方法 | `GET` |
| 认证 | 无需认证 |
| 响应格式 | `application/json` |
| 更新周期 | 每日更新 |
| 数据量上限 | 每日最多 **20** 条已发布测评笔记 |

## 路径参数

| 参数 | 位置 | 类型 | 必须 | 说明 |
|------|------|------|------|------|
| `date` | path | string | 是 | 日期，格式 `YYYY-MM-DD`，如 `2026-03-18` |

## 请求示例

```
GET https://openclaw.36krcdn.com/media/ainotes/2026-03-18/ai_notes.json
```

## 响应结构

响应为 JSON 数组，每个元素为一条测评笔记：

### 数组元素字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `noteId` | long | 笔记唯一 ID | `3568010593718423` |
| `title` | string | 笔记标题 | `"WPS AI测评"` |
| `authorName` | string | 作者名称 | `"氪友5sc4"` |
| `content` | string | 正文摘要，可为 null | `"简短介绍..."`  |
| `imgUrl` | string | 封面图片链接 | `"https://img.36dianping.com/..."` |
| `noteUrl` | string | 笔记详情链接，带 `?channel=skills` 参数 | `"https://36aidianping.com/note-detail/xxxx?channel=skills"` |
| `circleNames` | array | 所属圈子列表，每项含 `circleName`、`circleUrl`，可为空数组 | `[{"circleName":"营销辅助","circleUrl":"..."}]` |
| `productNames` | array | 关联产品列表，每项含 `productName`、`productUrl`，可为空数组 | `[{"productName":"美图设计室","productUrl":"..."}]` |
| `publishTime` | long | 发布时间戳（毫秒） | `1758525280903` |

## 完整响应示例

```json
[
  {
    "noteId": 3568010593718423,
    "title": "WPS AI测评",
    "authorName": "aaaaaal",
    "content": null,
    "imgUrl": "https://img.36dianping.com/hsossms/36dianping/img/20260319/v2_b512d444820e41d9b4fdebac06ad5683@534797_img_jpeg",
    "noteUrl": "https://36aidianping.com/note-detail/3568010593718423?channel=skills",
    "circleNames": [
      { "circleName": "办公辅助", "circleUrl": "https://36aidianping.com/circle/6?channel=skills" }
    ],
    "productNames": [
      { "productName": "WPS AI", "productUrl": "https://36aidianping.com/product-detail/14554?channel=skills" }
    ],
    "publishTime": 1773917737506
  },
  {
    "noteId": 3568010593718421,
    "title": "小悟空：AI工具的集合口袋",
    "authorName": "70KI",
    "content": null,
    "imgUrl": "https://img.36dianping.com/hsossms/36dianping/img/20260319/v2_4fb45afca8084a85a8e195dbdb65279c@534524_img_png",
    "noteUrl": "https://36aidianping.com/note-detail/3568010593718421?channel=skills",
    "circleNames": [
      { "circleName": "办公辅助", "circleUrl": "https://36aidianping.com/circle/6?channel=skills" }
    ],
    "productNames": [
      { "productName": "小悟空", "productUrl": "https://36aidianping.com/product-detail/14639?channel=skills" }
    ],
    "publishTime": 1773910511010
  }
]
```

## 错误处理

| HTTP 状态 | 说明 | 处理建议 |
|-----------|------|----------|
| `200` | 成功，返回 JSON 数组 | 正常解析 |
| `403` | 访问被拒绝 | 检查请求来源 |
| `404` | 文件不存在 | 当天任务未运行，可尝试查询前一天日期 |
| `503` / 网络超时 | CDN 暂时不可用 | 等待 30s 后重试，最多 3 次 |

### 防御性处理示例（Python 标准库）

```python
import urllib.request
import urllib.error
import json
import datetime

def fetch_ainotes(date: str = None, fallback_days: int = 3):
    """
    查询 AI 测评笔记，若当日无数据则自动回退到前 N 天。

    Args:
        date: 日期字符串 YYYY-MM-DD，默认今日
        fallback_days: 最多回退天数，默认 3 天
    Returns:
        list | None
    """
    BASE_URL = "https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"

    if date is None:
        check_date = datetime.date.today()
    else:
        check_date = datetime.date.fromisoformat(date)

    for i in range(fallback_days + 1):
        query_date = check_date - datetime.timedelta(days=i)
        url = BASE_URL.format(date=query_date.isoformat())
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"[WARN] {query_date} 无数据，尝试前一天...")
                continue
            print(f"[ERROR] HTTP {e.code}: {url}")
            return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None

    print("[ERROR] 所有回退日期均无数据")
    return None

# Demo
notes = fetch_ainotes()
if notes:
    for i, note in enumerate(notes, 1):
        pub_ts = note.get("publishTime", 0)
        pub_str = datetime.datetime.fromtimestamp(pub_ts / 1000).strftime("%Y-%m-%d %H:%M") if pub_ts else "?"
        circles  = "\u3001".join(c.get("circleName", "") for c in (note.get("circleNames") or [])) or "—"
        products = "\u3001".join(p.get("productName", "") for p in (note.get("productNames") or [])) or "—"
        print(f"#{i}  [{pub_str}] {note['title']} — {note['authorName']}")
        print(f"   圈子: {circles}  产品: {products}")
        print(f"   {note['noteUrl']}\n")
```

## 数据来源说明

该接口数据由定时任务生成：

1. 从数据库查询每日已发布测评笔记（`status = published`）
2. 按 `publishTime` 降序取前 20 条
3. 拼接笔记详情链接：`https://36aidianping.com/note-detail/{noteId}?channel=skills`
4. 生成 JSON 数组并上传至 CDN
5. CDN 路径：`media/ainotes/{YYYY-MM-DD}/ai_notes.json`

## URL 构造规则速查

```
BASE_CDN  = "https://openclaw.36krcdn.com"
OSS_PATH  = "media/ainotes"
FILE_NAME = "ai_notes.json"

完整 URL = BASE_CDN + "/" + OSS_PATH + "/" + DATE + "/" + FILE_NAME
示  例  = "https://openclaw.36krcdn.com/media/ainotes/2026-03-18/ai_notes.json"
```
