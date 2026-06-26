# API 参考文档 — 36kr 24小时热榜

## 接口基础信息

| 属性 | 值 |
|------|----|
| Base URL | `https://openclaw.36krcdn.com` |
| 路径模板 | `/media/hotlist/{date}/24h_hot_list.json` |
| 方法 | `GET` |
| 认证 | 无需认证 |
| 响应格式 | `application/json` |
| 更新周期 | 每小时一次（由定时任务 `OpenClawHotListJobHandler` 驱动） |
| 数据量上限 | 每日最多 **15** 条 |

## 路径参数

| 参数 | 位置 | 类型 | 必须 | 说明 |
|------|------|------|------|------|
| `date` | path | string | 是 | 日期，格式 `YYYY-MM-DD`，如 `2026-03-17` |

## 请求示例

```
GET https://openclaw.36krcdn.com/media/hotlist/2026-03-17/24h_hot_list.json
```

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 榜单日期，格式 `YYYY-MM-DD` |
| `time` | long | 数据生成的时间戳（毫秒），对应 Java `System.currentTimeMillis()` |
| `data` | array | 文章列表，见下方 |

### data 数组元素字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `rank` | int | 排名，从 `1` 开始递增 | `1` |
| `title` | string | 文章标题 | `"交涉"` |
| `author` | string | 作者名称，对应 `WidgetArticle.authorName` | `"36kr编辑"` |
| `publishTime` | string | 发布时间，格式 `yyyy-MM-dd HH:mm:ss` | `"2025-12-04 10:30:22"` |
| `content` | string | 文章正文/摘要，对应 `WidgetArticle.content` | `"文章正文内容..."` |
| `url` | string | 文章线上链接，固定附带 `?channel=openclaw` | `"https://36kr.com/p/3580613567306880?channel=openclaw"` |

## 完整响应示例

```json
{
  "date": "2026-03-17",
  "time": 1773740922167,
  "data": [
    {
      "rank": 1,
      "title": "2026年最值得关注的AI创业方向",
      "author": "36氪研究院",
      "publishTime": "2026-03-17 08:00:00",
      "content": "随着大模型技术的成熟，AI应用层迎来新一轮爆发...",
      "url": "https://36kr.com/p/9876543210000000?channel=openclaw"
    },
    {
      "rank": 2,
      "title": "硬科技独角兽融资排行榜",
      "author": "投资编辑部",
      "publishTime": "2026-03-17 09:30:00",
      "content": "2026年第一季度，超过20家硬科技公司完成亿元级融资...",
      "url": "https://36kr.com/p/9876543210000001?channel=openclaw"
    }
  ]
}
```

## 错误处理

| HTTP 状态 | 说明 | 处理建议 |
|-----------|------|----------|
| `200` | 成功，返回 JSON | 正常解析 |
| `403` | 访问被拒绝 | 检查请求来源 |
| `404` | 文件不存在 | 当天任务未运行，可尝试查询前一天日期 |
| `503` / 网络超时 | CDN 暂时不可用 | 等待 30s 后重试，最多 3 次 |

### 防御性处理示例（Python）

```python
import httpx
import datetime

def fetch_hotlist(date: str = None, fallback_days: int = 3):
    """
    查询热榜，若当日无数据则自动回退到前 N 天。
    
    Args:
        date: 日期字符串 YYYY-MM-DD，默认今日
        fallback_days: 最多回退天数，默认 3 天
    Returns:
        dict | None
    """
    BASE_URL = "https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json"
    
    if date is None:
        check_date = datetime.date.today()
    else:
        check_date = datetime.date.fromisoformat(date)
    
    for i in range(fallback_days + 1):
        query_date = check_date - datetime.timedelta(days=i)
        url = BASE_URL.format(date=query_date.isoformat())
        try:
            resp = httpx.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                print(f"[WARN] {query_date} 无数据，尝试前一天...")
                continue
            else:
                print(f"[ERROR] 状态码: {resp.status_code}")
                return None
        except httpx.RequestError as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    print("[ERROR] 所有回退日期均无数据")
    return None

# Demo
result = fetch_hotlist()
if result:
    for article in result["data"]:
        print(f"#{article['rank']} [{article['publishTime']}] {article['title']} — {article['author']}")
        print(f"   {article['url']}\n")
```

## 数据来源说明

该接口数据由 `OpenClawHotListJobHandler` 定时任务生成：

1. 从数据库 `widget_rank_hot` 表查询综合热榜（取前 15 条）
2. 通过 `widgetId` 关联查询 `WidgetArticle` 文章详情
3. 拼接文章 URL：`itemUrlStrategy.getItemOnlineUrl(...) + "?channel=openclaw"`
4. 生成 JSON 并上传至火山云 OSS
5. OSS 路径：`media/hotlist/{YYYY-MM-DD}/24h_hot_list.json`

## URL 构造规则速查

```
BASE_CDN  = "https://openclaw.36krcdn.com"
OSS_PATH  = "media/hotlist"
FILE_NAME = "24h_hot_list.json"

完整 URL = BASE_CDN + "/" + OSS_PATH + "/" + DATE + "/" + FILE_NAME
示  例  = "https://openclaw.36krcdn.com/media/hotlist/2026-03-17/24h_hot_list.json"
```
