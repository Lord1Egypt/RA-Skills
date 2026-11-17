# bbc-skill 设计文档

**目的**：获取 B 站视频评论并生成可被 Claude Code 进一步分析的数据，供 UP 主自助分析自己视频。

**状态**：设计确认 · 2026-04-19

---

## 1. 范围与非目标

**范围**
- 按 BV 号或视频 URL 拉取单个视频全部评论（顶级 + 楼中楼 + 置顶）
- 按 UID 批量拉取 UP 主所有视频的评论
- 输出适合 Claude Code 分析的结构化文件
- 同时抓取视频元数据（标题、播放、点赞、标签等）

**非目标**
- 不做情感分析、关键词提取等 NLP（留给 Claude Code 在 JSONL 上做）
- 不写入 / 删除任何数据（纯读操作）
- 不做浏览器自动化登录（认证委托给人/系统）

## 2. 运行环境

- Python 3.9+（stdlib 唯一依赖）
- macOS / Linux / Windows
- 零 pip install；解密 Chrome cookie 时通过 subprocess 调用系统自带的 `security` / `openssl` / `secret-tool` / `PowerShell`

## 3. Agent-Native CLI 契约

### 3.1 stdout / stderr / exit code

- **stdout**：永远是稳定的 JSON envelope（TTY 时默认切表格，非 TTY 自动 JSON；`--format json|table` 显式覆盖）
- **stderr**：人类可读日志 + 长任务的 NDJSON 进度事件
- **exit codes**：
  - `0` 成功
  - `1` 运行时 / API 错误
  - `2` 认证错误（cookie 失效/过期/缺失）
  - `3` 参数校验错误（BV 格式错等）
  - `4` 网络错误（超时/重试耗尽）

### 3.2 Envelope 格式

**成功**
```json
{
  "ok": true,
  "data": { ... },
  "meta": {
    "request_id": "req_xxx",
    "latency_ms": 12345,
    "schema_version": "1.0.0"
  }
}
```

**失败**
```json
{
  "ok": false,
  "error": {
    "code": "auth_expired",
    "message": "SESSDATA cookie 已过期或无效",
    "retryable": true,
    "retry_after_auth": true
  },
  "meta": { ... }
}
```

**错误码映射**

| code | exit | 含义 |
|---|---|---|
| `validation_error` | 3 | BV 格式错、参数范围越界 |
| `auth_required` | 2 | 未配置 cookie 且无法自动检测 |
| `auth_expired` | 2 | cookie 存在但被 B 站拒绝（code=-101） |
| `not_found` | 1 | 视频不存在 / 已删除 |
| `rate_limited` | 1 | 触发风控（HTTP 412 / code=-352） |
| `network_error` | 4 | 网络超时、DNS、重试耗尽 |
| `api_error` | 1 | 其他 B 站返回的非零 code |

### 3.3 子命令

```
bbc fetch <BV|URL> [--max N] [--since DATE] [--output DIR]
                    [--cookie-file PATH] [--dry-run] [--force]
                    [--format json|table]
bbc fetch-user <UID> [--output DIR] ...
bbc summarize <dir>                     # 从已有 comments.jsonl 重建 summary
bbc cookie-check                        # 验证 cookie，打印登录用户
bbc schema [command]                    # 返回参数/类型/exit code 契约
bbc --help | bbc <sub> --help
```

### 3.4 Dry-run

```
$ bbc fetch BV1NjA7zjEAU --dry-run
{
  "ok": true,
  "dry_run": true,
  "would": {
    "bvid": "BV1NjA7zjEAU",
    "aid": 116258406143402,
    "estimated_top_pages": 3,
    "estimated_sub_calls": 10,
    "estimated_duration_seconds": 15,
    "output_dir": "/abs/path/bilibili-comments/BV1NjA7zjEAU"
  }
}
```

### 3.5 长任务进度事件（stderr，NDJSON）

```
{"event":"start","command":"fetch","bvid":"BV1xx","request_id":"req_abc"}
{"event":"progress","phase":"meta","message":"video meta fetched","title":"..."}
{"event":"progress","phase":"top_level","page":1,"done":19,"declared_total":59}
{"event":"progress","phase":"top_level","page":2,"done":39,"declared_total":59}
{"event":"progress","phase":"nested","thread":1,"total":10}
{"event":"complete","request_id":"req_abc","elapsed_ms":12345}
```

## 4. 认证模型

### 4.1 优先级（先到者胜）

1. `--cookie-file <path>`（Netscape 格式）
2. `$BBC_COOKIE_FILE` 环境变量
3. `$BBC_SESSDATA` 环境变量（直接传 SESSDATA 值，轻量场景）
4. 自动探测浏览器（按操作系统）
5. 默认配置路径 `~/.config/bbc-skill/cookie.json`（登录后缓存）

### 4.2 浏览器自动探测矩阵

| OS | 浏览器 | 路径 | 解密 |
|---|---|---|---|
| macOS | Firefox | `~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite` | 明文 |
| macOS | Chrome/Edge | `~/Library/Application Support/Google/Chrome/<profile>/Cookies` | `security find-generic-password` + `openssl enc -aes-128-cbc` |
| macOS | Safari | `~/Library/Cookies/Cookies.binarycookies` | 明文（binary plist） |
| Linux | Firefox | `~/.mozilla/firefox/*/cookies.sqlite` | 明文 |
| Linux | Chrome | `~/.config/google-chrome/<profile>/Cookies` | `secret-tool` 取 key |
| Windows | Firefox | `%APPDATA%/Mozilla/Firefox/Profiles/*/cookies.sqlite` | 明文 |
| Windows | Chrome/Edge | `%LOCALAPPDATA%/Google/Chrome/User Data/<profile>/Network/Cookies` | `ctypes` + DPAPI + PowerShell AES-GCM |

失败处理：所有候选都失败时，若 stdin 是 TTY 则提示用户粘贴 SESSDATA；非 TTY 则返回 `auth_required` envelope 立即退出。

### 4.3 需要的 cookie 字段

必需：`SESSDATA`
推荐：`bili_jct`（CSRF，某些接口要）、`DedeUserID`、`buvid3`
无需：刷新 token / OAuth

## 5. 抓取流程

```
1. 解析输入 → bvid
2. GET /x/web-interface/view?bvid=<BV>   → aid, title, stat, owner, tags 等 video meta
3. GET /x/web-interface/nav              → 登录校验（可选，用于 cookie-check）
4. LOOP GET /x/v2/reply/main?type=1&oid=<aid>&mode=3&next=<cursor>&ps=20
     - 每页提取 replies[] 和 cursor
     - 同时合并 top_replies[]（置顶）仅在第 1 页处理
     - is_end=True 或 replies=[] 停止
5. FOR EACH top-level where rcount > 0:
     LOOP GET /x/v2/reply/reply?type=1&oid=<aid>&root=<rpid>&pn=<n>&ps=20
6. Flatten → JSONL（每行一条，含 parent/root 指针）
7. 生成 summary.json（视频元数据 + 统计 + Top-N）
```

### 5.1 速率与重试

- 每请求间隔 1s（顶级）/ 0.5s（楼中楼）
- HTTP 412 或 code=-352：指数退避 2s→4s→8s，重试 3 次
- 其他 HTTP 错误：立即失败，返回 `api_error` / `network_error`
- 进度 & 断点写入 `<output_dir>/.bbc-state.json`，再次运行自动续传

### 5.2 --since 增量

`.bbc-state.json` 记录上次 `latest_ctime`。传 `--since` 时，拉到 ctime 早于该阈值即停。

## 6. 输出布局

```
<output_dir>/                           # 默认 ./bilibili-comments/<BV>/
├── comments.jsonl                      # 主数据，每行一条评论（含楼中楼）
├── summary.json                        # 视频元数据 + 统计
├── raw/                                # API 原始响应归档（便于 schema 回溯）
│   ├── main-page-001.json
│   ├── main-page-002.json
│   └── reply-<rpid>-page-001.json
├── .bbc-state.json                     # 断点 & --since 用
└── fetch.log                           # 人类可读日志
```

### 6.1 comments.jsonl 单条 schema

```json
{
  "rpid": 296636680849,
  "rpid_str": "296636680849",
  "oid": 116258406143402,
  "bvid": "BV1NjA7zjEAU",
  "parent": 0,
  "root": 0,
  "mid": 71171081,
  "uname": "蓝忘今宵-_-YS",
  "user_level": 4,
  "vip": false,
  "sex": "保密",
  "ctime": 1776521119,
  "ctime_iso": "2026-04-18T06:25:19+00:00",
  "message": "已关注 求指教'",
  "like": 1,
  "rcount": 0,
  "ip_location": "河北",
  "is_up_reply": false,
  "top_type": 0,
  "mentioned_users": [],
  "jump_urls": []
}
```

字段：
- `parent=0` 表示顶级；否则指向父评论 rpid
- `root=0` 表示顶级；否则指向根评论 rpid（跨层回复）
- `top_type`：0=普通，1=UP 置顶，2=热评置顶
- `is_up_reply`：UP 主本人回复（mid == 视频 owner.mid）
- `ip_location`：剥掉 `IP属地：` 前缀后的省份

### 6.2 summary.json schema

```json
{
  "schema_version": "1.0.0",
  "fetched_at": "2026-04-19T08:30:00+00:00",
  "fetch_range": {"mode": "full", "since": null, "max": null, "resumed": false},
  "video": {
    "bvid": "BV1NjA7zjEAU",
    "aid": 116258406143402,
    "title": "...",
    "desc": "...",
    "pubdate_iso": "2026-03-01T...",
    "duration_seconds": 42,
    "cover_url": "https://...",
    "owner": {"mid": 441831884, "name": "探索未至之境"},
    "stat": {"view": 7287, "like": 97, "coin": 70, "favorite": 116,
             "reply": 59, "danmaku": 3, "share": 4},
    "tags": ["魔法", "学习", "教程", ...]
  },
  "counts": {
    "total": 59, "top_level": 44, "nested": 14, "pinned": 1,
    "declared_all_count": 59,
    "completeness": 1.0,
    "unique_users": 47, "up_replies": 0
  },
  "time_distribution": {
    "earliest_iso": "...",
    "latest_iso": "...",
    "by_day": [{"date": "2026-03-01", "count": 12}, ...]
  },
  "top_liked": [{"rpid": 123, "uname": "...", "like": 50,
                  "message_preview": "...", "parent": 0}],
  "top_replied": [{"rpid": 124, "uname": "...", "rcount": 8, ...}],
  "ip_distribution": {"浙江": 5, "广东": 4, ...}
}
```

## 7. 目录结构

```
bbc-skill/
├── SKILL.md                          # skill 入口（Claude 读这个）
├── DESIGN.md                         # 本文档
├── README.md                         # 中文 README（发布用）
├── README_EN.md                      # 英文 README（发布用）
├── scripts/
│   └── bbc                           # shim：调用 python3 -m bbc
├── src/
│   └── bbc/
│       ├── __init__.py               # 版本号
│       ├── __main__.py               # python3 -m bbc 入口
│       ├── cli.py                    # argparse + dispatch
│       ├── envelope.py               # JSON envelope + TTY detect + exit codes
│       ├── progress.py               # stderr NDJSON 进度事件
│       ├── schema.py                 # 每条命令的参数 schema
│       ├── api.py                    # HTTP client (stdlib) + 重试 + rate limit
│       ├── fetch.py                  # fetch 子命令核心逻辑
│       ├── fetch_user.py             # fetch-user 子命令
│       ├── summarize.py              # summarize / 在 fetch 末尾调用
│       ├── flatten.py                # API 响应 → JSONL 行
│       └── cookie/
│           ├── __init__.py           # 自动探测 orchestrator
│           ├── netscape.py           # 解析 Netscape cookie.txt
│           ├── firefox.py            # sqlite3 stdlib
│           ├── chrome_macos.py       # security + openssl subprocess
│           ├── chrome_linux.py       # secret-tool subprocess
│           ├── chrome_windows.py     # ctypes DPAPI + PowerShell
│           └── safari.py             # binarycookies 解析
├── references/
│   ├── api-endpoints.md              # 所用 B 站 API 字段文档
│   ├── cookie-extraction.md          # 各浏览器 cookie 位置与解密
│   └── agent-contract.md             # envelope / exit code / schema 契约
├── examples/
│   └── BV1NjA7zjEAU/                 # 真实样本输出
│       ├── comments.jsonl
│       ├── summary.json
│       └── README.md                 # 讲解如何用 Claude 分析它
└── spike/                            # spike 阶段的代码和样本，保留参考
    └── ...
```

## 8. 不做的事（YAGNI）

- 不内置情感分析 / 关键词提取 / 词云
- 不做 Excel / CSV 导出（Claude 可按需转）
- 不做 Web UI
- 不支持匿名抓取（UP 主分析场景一定有 cookie）
- 不做弹幕 / 私信 / 投稿等其他 B 站数据

## 9. 发布准备（后续）

- GitHub topics: `claude-code, claude-code-skill, claude-skills, agent-skills, skillsmp, openclaw, openclaw-skills, skill-md, bilibili`
- SKILL.md frontmatter 含 `metadata.openclaw.requires.bins`
- 双语 README + 样本输出
