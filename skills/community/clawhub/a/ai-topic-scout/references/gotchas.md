# 踩坑记录

## 钉钉 AI 表格 MCP

### 1. create_records 返回空 `{}`

`create_records` 成功时返回 `{"newRecordIds":[...]}` 。如果返回空 `{}`，说明某个字段值格式有问题被静默拒绝了。常见原因：

- **日期字段**传了不支持的格式。推荐 `"YYYY-MM-DD"` 或 `"YYYY-MM-DD HH:mm"`
- **singleSelect 字段**传了 option ID 字符串而非 option name 字符串（创建记录时应传 name）
- 记录中包含关联字段值（见下条）

### 2. 关联字段不能在 create_records 中同时写入

`create_records` 时如果 cells 里带了关联字段（unidirectionalLink/bidirectionalLink），**整条记录会静默失败**，不报错但也不返回 newRecordIds。

**正确做法**：先 `create_records` 不带关联字段 → 拿到 recordId → 再 `update_records` 单独写关联。

### 3. 关联字段写入格式

关联字段 **不能直接传 recordId 数组**，必须用对象格式：

```json
// ❌ 错误
{"fieldId": ["recXXX", "recYYY"]}

// ✅ 正确
{"fieldId": {"linkedRecordIds": ["recXXX", "recYYY"]}}
```

### 4. update_records 返回值差异

- 成功：返回 `{"recordIds":["rec1","rec2"]}`
- 静默失败：返回 `{}`（没有 recordIds 字段）

### 5. query_records 返回空记录

`query_records` 不带任何过滤条件时可能返回 `{}`（没有 records 字段）。确保至少传一个条件（`limit`、`keyword`、`recordIds` 或 `filters`）。

> 实测发现新创建的记录可能需要短暂延迟才能被查到。

### 6. singleSelect 过滤必须传 option ID

`query_records` 的 `filters` 里过滤 singleSelect 字段时，**必须传 option ID，不是 option name**。option ID 需要先通过 `get_fields` 获取。

但 `create_records` / `update_records` 写入时可以直接传 option name。

### 7. bidirectionalLink vs unidirectionalLink

两种关联字段在 API 层面写入方式完全相同。但 `bidirectionalLink` 创建时会在目标表自动生成反向字段。推荐使用 `unidirectionalLink`，更简单可控。

### 8. MCP Schema 版本检查

首次使用钉钉 AI 表格 skill 时，先跑一次 schema 检查：

```bash
mcporter list dingtalk-ai-table --schema
```

确认返回的是新版 schema（`list_bases`、`get_base`、`create_records` 等），而非旧版（`get_root_node_of_my_document`、`create_base_app` 等）。如果是旧版，需要去 MCP 广场获取新的 Server 地址。

## bird (Twitter CLI)

### 1. 服务器环境没有浏览器 cookie

在无头服务器上，bird 无法从浏览器提取 cookie。必须通过参数传入：

```bash
bird user-tweets @handle -n 5 --plain --auth-token "<token>" --ct0 "<ct0>"
```

或在 `~/.config/bird/config.json5` 中配置：

```json5
{
  authToken: "<token>",
  ct0: "<ct0>"
}
```

> ⚠️ bird 不会自动读取 config.json5 中的 authToken/ct0（截至当前版本），**必须通过 CLI 参数传入**。

### 2. 推文中夹杂广告/推广

`user-tweets` 返回的结果中可能包含日文/其他语言的广告推文（Twitter 插入的推广内容）。分析时需要识别并过滤掉非目标博主的内容——检查推文作者 handle 是否匹配请求的 handle。

### 3. 速率限制

频繁抓取可能触发 Twitter 速率限制。建议：
- 每个博主之间间隔 2-3 秒
- 每次只取最新 5 条
- 如果遇到 429 错误，等待后重试

## yt-dlp / YouTube

### 1. 获取频道最新视频列表

```bash
yt-dlp --flat-playlist --print "%(id)s %(title)s" -I 1:3 "https://www.youtube.com/@handle/videos"
```

`-I 1:3` 表示只取前3个。

### 2. 部分视频没有字幕

`get_transcript.py` 对没有 CC 字幕或自动字幕的视频会失败。遇到这种情况，跳过该视频，在 fetch 表中不创建记录（或只记录标题不记录摘要）。

### 3. 频道 ID vs Handle

YouTube 频道有两种标识：
- **Handle**: `@TwoMinutePapers`（用于 URL）
- **Channel ID**: `UCbfYPyITQ-7l4uLBPZmTCg`（用于 API）

抓取视频列表用 Handle 更方便：`https://www.youtube.com/@handle/videos`

## 背景搜索

分析选题时需要搜索背景信息来补充上下文和验证热度。使用任何可用的搜索工具即可（Tavily、web search 等），不限定具体工具。

搜索建议：
- 关键词 + 当前年份，取新闻类结果
- 每个选题搜 3-5 条补充信息即可
- 搜索结果是辅助手段，不要完全依赖搜索结果判断热度
