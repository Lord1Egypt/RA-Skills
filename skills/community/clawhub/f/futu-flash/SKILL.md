---
name: futu-flash
description: 抓取富途官网资讯「快讯」频道最新消息。用于用户要求“去富途快讯找最新N条（最多10条）”、“更新快讯”、“滚动刷新快讯”等场景；通过富途接口 /news-site-api/main/get-flash-list 获取并格式化返回。
---

# Futu Flash Skill

使用这个 skill 时，按以下流程执行。

## 1) 获取最新快讯

调用接口：

- `GET https://news.futunn.com/news-site-api/main/get-flash-list?pageSize=<N>`
- `N` 默认 10，最大 10。

请求头至少带：

- `User-Agent: Mozilla/5.0`
- `Referer: https://news.futunn.com/main/live`
- `Accept: application/json, text/plain, */*`
- `Accept-Language: zh-CN,zh;q=0.9`

优先用脚本：`scripts/fetch_futu_flash.py`。

## 2) 解析字段

从响应中读取：

- 顶层：`code`（应为 0）
- 列表：`data.data.news`（数组）

每条快讯常用字段：

- `id`
- `time`（Unix 秒级时间戳）
- `title`（常为空）
- `content`（主要内容）
- `detailUrl`（详情页）

显示文本时使用：

- `text = title or content`

## 3) 时间与输出

- 将 `time` 转为北京时间（UTC+8）输出。
- 按接口顺序返回（通常已是最新在前）。
- 输出条数：默认 10；若用户指定条数，返回 `min(用户要求, 10)`。

建议输出格式：

1. `YYYY-MM-DD HH:mm:ss` + 文本
2. 保留原顺序编号

## 4) 异常处理

- HTTP 非 200：返回抓取失败与状态码。
- JSON 解析失败：返回“接口返回非 JSON”。
- `code != 0` 或列表为空：返回“暂无快讯/接口异常”。
- 若用户要求 >10 条，明确说明“富途接口当前流程按最多10条返回”。

## 5) 备注

- 页面 `https://news.futunn.com/main/live` 本身可能被反爬或返回无效内容，优先直连接口。
- 不要编造快讯内容；只返回接口真实数据。