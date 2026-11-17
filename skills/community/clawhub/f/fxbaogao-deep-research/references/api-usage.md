# 发现报告接口调用说明

本文件说明如何调用发现报告接口。搜索、段落和下载都通过 API 完成。

## 统一规范

- API Base URL：`https://api.fxbaogao.com`
- 鉴权 Header：`Authorization: Bearer $FXBAOGAO_API_KEY`
- `Content-Type`：`application/json`
- `FXBAOGAO_API_KEY` 从环境变量获取。
- 若未设置，先提示用户：`export FXBAOGAO_API_KEY=<你的apikey>`
- 搜索、段落和下载接口都需要鉴权。

```bash
export FXBAOGAO_API_KEY=<your_api_key>
```

## 报告搜索

接口：

```text
POST /mofoun/agent/search
```

请求数据类型：`application/json`

请求参数：

| 参数 | 类型 | 必填 | 说明                                                                          |
| --- | --- | --- |-----------------------------------------------------------------------------|
| `keywords` | string | 否 | 搜索关键词。关键词、机构至少提供一个                                                          |
| `orgNames` | array | 否 | 机构列表                                                                        |
| `startTime` | string | 否 | 开始时间。支持毫秒时间戳字符串，也可传 `last3day`、`last7day`、`last1mon`、`last3mon`、`last1year` |
| `endTime` | string | 否 | 结束时间。毫秒时间戳字符串                                                               |


示例：

```bash
curl -X POST "https://api.fxbaogao.com/mofoun/agent/search" \
  -H "Authorization: Bearer $FXBAOGAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keywords":"光模块 800G AI算力","orgNames":[],"endTime":"last1year"}'
```

重点回包字段：

| 字段                                       | 说明                |
|------------------------------------------|-------------------|
| `code`                                   | `0` 表示成功          |
| `msg`                                    | 错误或提示信息           |
| `data[]`                                 | 报告列表              |
| `data[].reportId`                        | 报告 ID             |
| `data[].title`                           | 报告标题，可能包含 <em> 标签 |
| `data[].orgName`                         | 机构名称，可能包含 <em> 标签 |
| `data[].pubTime` / `pubTimeStr`          | 发布时间              |
| `data[].industryName`                    | 行业                |
| `data[].pageNum`                         | 页数                |
| `data[].paragraphs`                      | 命中的正文片段           |
| `data[].paragraphs[].content`            | 命中段落正文            |
| `data[].paragraphs[].pageNum`            | 命中段落页码            |

展示搜索结果时，优先展示标题、机构、作者、日期、报告 ID、官网阅读链接：

```text
https://www.fxbaogao.com/view?id=<reportId>
```

## 报告段落

接口：

```text
POST /mofoun/agent/paragraph
```

请求数据类型：`application/json`

请求参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `reportId` | integer(int64) | 否 | 报告 ID |
| `keyword` | string | 否 | 搜索关键词，用于命中上下文 |

示例：

```bash
curl -X POST "https://api.fxbaogao.com/mofoun/agent/paragraph" \
  -H "Authorization: Bearer $FXBAOGAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"reportId":5339478,"keyword":"光模块 800G"}'
```

重点回包字段：

| 字段 | 说明   |
| --- |------|
| `code` | `0` 表示成功 |
| `msg` | 错误或提示信息 |
| `data.title` | 报告标题 |
| `data.summary` | 摘要 |
| `data.paragraphs[]` | 命中的正文段落 |
| `data.paragraphs[].content` | 命中段落正文 |
| `data.paragraphs[].pageNum` | 命中段落页码 |


注意：paragraph 回包适合快速初筛和轻量研究。正式精读或需要引用原文时，应下载 PDF 并基于 PDF 原文核对。

## PDF 下载

接口：

```text
GET /mofoun/agent/download?reportId=<reportId>
```

示例：

```bash
curl -L "https://api.fxbaogao.com/mofoun/agent/download?reportId=5339478" \
  -H "Authorization: Bearer $FXBAOGAO_API_KEY"
```

重点回包字段：

| 字段 | 说明            |
| --- |---------------|
| `data` | PDF 下载 URL |
