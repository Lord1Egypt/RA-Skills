---
name: dao3-statistics
description: 当用户想按 userId 或 mapId 查询神岛平台数据时使用此技能，例如用户资料、地图详情、地图评论、粉丝/好友/关注列表、收藏/最近游玩、关键词搜索等。当用户需要“需要认证”的消息/统计数据（评论/点赞/系统消息、地图统计、玩家统计、留存、行为等）并且能够提供 神岛token 和 user-agent 时，也使用此技能。即使用户没有明确说“神岛数据”，但描述的是这些神岛相关诉求，也优先触发此技能。
compatibility: 需要 python3 和联网环境。部分命令需要有效的 神岛token 和 user-agent。
metadata:
  author: box3lab
  version: "1.0"
  openclaw:
    emoji: "📊"
    os:
      - darwin
      - linux
    primaryEnv: ""
    requires:
      bins:
        - python3
      env: []
    install: []
---

## 这个技能做什么

这个技能提供一个命令行接口，用于从官方 API 获取 DAO3（神岛）平台数据。

覆盖两类能力：

- 公开接口（无需认证）
- 认证接口（需要 token + user-agent）

所有命令都会向 stdout 输出一个 JSON 对象。

## 如何运行

在 `scripts/` 目录下运行：

```bash
python3 -m dao3_statistics --help
```

## 命令

### 公开接口（无需认证）

#### `user-profile --user-id <id>`

用途：通过用户 ID 获取用户个人资料。

参数：

- `--user-id <id>`：用户 ID。

#### `map-info --map-id <id>`

用途：通过地图/内容 ID 获取地图详情。

参数：

- `--map-id <id>`：地图（content）ID。

#### `map-comments --content-id <id> --limit <n> --offset <n> --order-by <n> --content-type <n>`

用途：获取地图/模型的评论列表。

参数：

- `--content-id <id>`：内容 ID（地图/模型 ID）。
- `--limit <n>`：返回数量（上游通常限制最大 100）。
- `--offset <n>`：偏移量（分页用）。
- `--order-by <n>`：排序方式（例如 1=创建时间倒序；4=热度等，具体以接口为准）。
- `--content-type <n>`：内容类型（例如 1=地图；2=模型）。

#### `map-release --content-id <id> --limit <n> --offset <n>`

用途：获取地图发布信息。

参数：

- `--content-id <id>`：地图 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-maps --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户发布/关联的地图列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-models --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户的模型列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-favorites --user-id <id> --limit <n> --offset <n> --content-type <n>`

用途：获取某个用户的收藏列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。
- `--content-type <n>`：收藏内容类型（例如 1=地图；2=模型）。

#### `user-recent --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户最近游玩列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-followers --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户的粉丝列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-friends --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户的好友列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `user-following --user-id <id> --limit <n> --offset <n>`

用途：获取某个用户的关注列表。

参数：

- `--user-id <id>`：用户 ID。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。

#### `search --keyword <kw> --limit <n> --offset <n> --order-by <n>`

用途：通过关键字搜索地图/模型列表。

参数：

- `--keyword <kw>`：关键词。
- `--limit <n>`：返回数量。
- `--offset <n>`：偏移量。
- `--order-by <n>`：排序方式（例如 0=推荐/最热；1=最新；具体以接口为准）。

示例：

```bash
python3 -m dao3_statistics user-profile --user-id 83354
python3 -m dao3_statistics map-info --map-id 100131463
python3 -m dao3_statistics search --keyword "test" --limit 10 --offset 0 --order-by 0
```

### 认证接口（token + user-agent）

必须同时提供：

- `--token`: DAO3 认证 token
- `--user-agent`: 类浏览器的 UA 字符串

命令：

#### `msg-comments --offset <n> --limit <n> --token <t> --user-agent <ua>`

用途：获取“评论消息”列表（站内消息/通知类）。

参数：

- `--offset <n>`：偏移量。
- `--limit <n>`：返回数量。
- `--token <t>`：认证 token。
- `--user-agent <ua>`：UA 字符串（会同时用于 `user-agent` 和 `x-dao-ua` 请求头）。

#### `msg-likes --offset <n> --limit <n> --token <t> --user-agent <ua>`

用途：获取“点赞消息”列表。

参数：同 `msg-comments`。

#### `msg-sys --offset <n> --limit <n> --token <t> --user-agent <ua>`

用途：获取“系统消息”列表。

参数：同 `msg-comments`。

#### `stats-maps --start-time <YYYY-MM-DD> --end-time <YYYY-MM-DD> --token <t> --user-agent <ua>`

用途：获取当前用户的地图统计列表（按日期范围）。

参数：

- `--start-time <YYYY-MM-DD>`：开始日期。
- `--end-time <YYYY-MM-DD>`：结束日期。
- `--token <t>`：认证 token。
- `--user-agent <ua>`：UA 字符串。

#### `stats-player --start-time <YYYY-MM-DD> --end-time <YYYY-MM-DD> --map-id <id> --token <t> --user-agent <ua>`

用途：获取指定地图的玩家统计数据（按日期范围）。

参数：

- `--start-time <YYYY-MM-DD>`：开始日期。
- `--end-time <YYYY-MM-DD>`：结束日期。
- `--map-id <id>`：地图 ID。
- `--token <t>`：认证 token。
- `--user-agent <ua>`：UA 字符串。

#### `stats-retention --start-time <YYYY-MM-DD> --end-time <YYYY-MM-DD> --map-id <id> --token <t> --user-agent <ua>`

用途：获取指定地图的玩家留存数据（按日期范围）。

参数：同 `stats-player`。

#### `stats-behavior --start-time <YYYY-MM-DD> --end-time <YYYY-MM-DD> --map-id <id> --token <t> --user-agent <ua>`

用途：获取指定地图的玩家行为分析数据（按日期范围）。

参数：同 `stats-player`。

示例：

```bash
python3 -m dao3_statistics stats-player \
  --start-time 2025-03-29 \
  --end-time 2025-04-04 \
  --map-id 100131463 \
  --token "YOUR_TOKEN" \
  --user-agent "Mozilla/5.0 ..."
```

### Raw 端点逃生口

如果你需要调用尚未映射为专用命令的端点：

- `raw --endpoint <path-or-query> [--token <t> --user-agent <ua>]`

用途：直接请求任意上游 API 端点（适合临时验证/调试/未映射的新端点）。

参数：

- `--endpoint <path-or-query>`：以 `/` 开头的端点路径（可带 querystring）。
- `--token <t>` 与 `--user-agent <ua>`：可选；如果该端点需要认证则必须同时提供。

示例：

```bash
python3 -m dao3_statistics raw --endpoint "/user/profile/83354"
```

## 输出

- 成功：输出 API 的 JSON 响应
- 失败：输出包含 `error`、`endpoint` 的 JSON；并可能包含 `status_code`、`response`

## 备注 / 边界情况

- `--limit` 的取值最大为100。
- 网络失败/超时会以错误 JSON 形式返回。
