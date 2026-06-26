# API 参考文档 — 36kr 自助报道栏目文章

## 接口基础信息

| 属性 | 值 |
|------|----|
| Base URL | `https://openclaw.36krcdn.com` |
| 路径模板 | `/media/aireport/{date}/ai_report_articles.json` |
| 方法 | `GET` |
| 认证 | 无需认证 |
| 响应格式 | `application/json` |
| 更新周期 | 每 **2 小时**一次（由定时任务 `OpenClawAiReportJobHandler` 驱动） |
| 数据量上限 | 每次最多 **15** 条 |

## 路径参数

| 参数 | 位置 | 类型 | 必须 | 说明 |
|------|------|------|------|------|
| `date` | path | string | 是 | 日期，格式 `YYYY-MM-DD`，如 `2026-03-17` |

## 请求示例

```
GET https://openclaw.36krcdn.com/media/aireport/2026-03-17/ai_report_articles.json
```

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 数据日期，格式 `YYYY-MM-DD` |
| `time` | long | 数据生成的时间戳（毫秒），对应 Java `System.currentTimeMillis()` |
| `data` | array | 文章列表，见下方 |

### data 数组元素字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `rank` | int | 排名，从 `1` 开始递增 | `1` |
| `title` | string | 文章标题 | `"我们的AI产品寻求报道"` |
| `author` | string | 作者名称，对应 `WidgetArticle.authorName` | `"某科技公司"` |
| `publishTime` | string | 发布时间，格式 `yyyy-MM-dd HH:mm:ss` | `"2026-03-17 10:30:22"` |
| `url` | string | 文章线上链接，固定附带 `?channel=openclaw` | `"https://36kr.com/p/3580613567306880?channel=openclaw"` |

## 完整响应示例

```json
{
  "date": "2026-03-17",
  "time": 1773740922167,
  "data": [
    {
      "rank": 1,
      "title": "我们正在研发下一代工业机器人，寻求媒体报道",
      "author": "智能制造科技",
      "publishTime": "2026-03-17 09:00:00",
      "url": "https://36kr.com/p/9876543210000010?channel=openclaw"
    },
    {
      "rank": 2,
      "title": "AI辅助医疗影像诊断系统完成B轮融资，寻求报道",
      "author": "医健科技",
      "publishTime": "2026-03-17 08:30:00",
      "url": "https://36kr.com/p/9876543210000011?channel=openclaw"
    },
    {
      "rank": 3,
      "title": "面向中小企业的低代码开发平台上线，诚邀媒体关注",
      "author": "云端软件",
      "publishTime": "2026-03-17 08:00:00",
      "url": "https://36kr.com/p/9876543210000012?channel=openclaw"
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

def fetch_aireport(date: str = None, fallback_days: int = 3):
    """
    查询自助报道文章，若当日无数据则自动回退到前 N 天。

    Args:
        date: 日期字符串 YYYY-MM-DD，默认今日
        fallback_days: 最多回退天数，默认 3 天
    Returns:
        dict | None
    """
    BASE_URL = "https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json"

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
result = fetch_aireport()
if result:
    for article in result["data"]:
        print(f"#{article['rank']} [{article['publishTime']}] {article['title']} — {article['author']}")
        print(f"   {article['url']}\n")
```

## 数据来源说明

该接口数据由 `OpenClawAiReportJobHandler` 定时任务生成：

1. 从数据库 `widget_article` 表查询自助报道文章（来源 `dictOrigin = 5`，即 `ArticleOriginEnum.ai_report`）
2. 筛选条件：`status = online`，按 `publish_time DESC` 取前 15 条
3. 拼接文章 URL：`itemUrlStrategy.getItemOnlineUrl(...) + "?channel=openclaw"`
4. 生成 JSON 并上传至火山云 OSS
5. OSS 路径：`media/aireport/{YYYY-MM-DD}/ai_report_articles.json`

## URL 构造规则速查

```
BASE_CDN  = "https://openclaw.36krcdn.com"
OSS_PATH  = "media/aireport"
FILE_NAME = "ai_report_articles.json"

完整 URL = BASE_CDN + "/" + OSS_PATH + "/" + DATE + "/" + FILE_NAME
示  例  = "https://openclaw.36krcdn.com/media/aireport/2026-03-17/ai_report_articles.json"
```
