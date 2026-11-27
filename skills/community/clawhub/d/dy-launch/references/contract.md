# 输出契约

> **何时读**：需要核对信封字段、`results` 形态，或写后处理脚本时再读。日常执行只需记住：stdout 是统一信封；向用户只摘关键字段；`empty` 不是失败。

## 统一信封

stdout 只有一份统一信封（成功 / 空结果 / 错误结构相同）：

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | INVALID_KEYWORD | INVALID_URL | INVALID_ARGS | AUTH_REQUIRED | AUTH_ERROR | PLAN_LIMIT | INSUFFICIENT_BALANCE | RATE_LIMITED | DAILY_LIMIT | TIMEOUT | NETWORK_ERROR | API_ERROR | HTTP_404 | HTTP_410 | HTTP_5xx | HTTP_* | ...",
  "message": "人类可读的说明",
  "timestamp": "2026/9/4 20:13:20",
  "request": {
    "command": "search",
    "keyword": "AI 教程",
    "sort": 1,
    "limit": 20
  },
  "metadata": {
    "skill_version": "1.5.2",
    "runtime_version": "22.x",
    "execution_time": 34210
  },
  "results": [],
  "cost": 0.08
}
```

- `status=error` 时 `results` 为 `null`，原因看 `error_code` + `message`。
- 可选顶层 `cost`（number）：取数成功 / empty 时可能出现，为**花费估算**（包月固定 `1`，按次按条数×单价）；错误、热榜、上游未返回时省略。
- 信封字段见 `assets/output_envelope.schema.json`。
- 条目字段见 `assets/*_cli_resp.schema.json`。

## `results` 形态（勿假设永远是数组）

| 命令 | 成功时 `results` |
| --- | --- |
| 视频搜索 / 用户搜索 / 评论 / 热榜 | **数组** |
| 博主作品 | **对象**：`{ post: 作品数组, user: 博主信息 }` |
| 作品详情 | **一条作品对象**（不是数组，不含评论） |

## 上游异步任务（Create → `/info`）

> CLI 入参/出参 schema **不含**任务 uuid：命令行仍只收 keyword/url 等；任务 id 由 Skill 内部从 Create 响应带到查询，**不出现在 stdout 信封**。

异步命令（热榜等同步 GET 除外）对 guaikei REST：

| 步骤 | 约定 |
| --- | --- |
| Create 成功出参 | 顶层 `id`：标准 36 字符 uuid；缺失或形态不符视为无 id |
| 查询 `/info` 有 id | **只传** `id`（请求层仍可附加 `_` / `skill_name`），**不带** keyword/url 等业务字段 |
| 查询无 id | 只传与 Create 相同的业务字段（兼容旧后端） |

有 id 时不带业务字段，是为避免上游「uuid 未命中则回落业务字段查他单」；未命中时按缺参/业务错误处理，由既有轮询与错误码承接。

## 向用户汇报

- **只摘关键字段**（视频：标题/作者/点赞/链接/时间；用户：昵称/粉丝/获赞/主页），不要把整份 JSON 原样粘贴——单条含大量封面与播放 URL，会撑爆上下文。
- 适合衔接：选题汇总、高赞对比、竞品风格总结、博主发文节奏、报告与表格。
- 需求挖掘：先读 [demand-mining.md](demand-mining.md)，按四段输出，不粘贴整份评论 JSON。
- 公域获客：先读 [customer-acquisition.md](customer-acquisition.md)，按线索表整理；不编造手机号/微信号。

错误应对全表见 [errors.md](errors.md)。
