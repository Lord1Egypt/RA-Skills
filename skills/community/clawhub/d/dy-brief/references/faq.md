# 常见问题与环境配置

> **何时读**：排障、配 TOKEN、查落盘路径或计费口径时再读。日常执行不必每次打开。

## 环境

- Node.js 16.14.0+，Windows / Linux / macOS；必需环境变量 `GUAIKEI_API_TOKEN`（16–256 位字母、数字、下划线或连字符）。
- Windows cmd：`set GUAIKEI_API_TOKEN=你的TOKEN`
- Windows PowerShell：`$env:GUAIKEI_API_TOKEN="你的TOKEN"`
- Linux/macOS：`export GUAIKEI_API_TOKEN=你的TOKEN`

## Windows 引号 / 拆参

Agent 在 Windows 上最常见的失败不是业务错，而是 **shell 把参数拆坏**，技能报 `INVALID_ARGS` / `INVALID_KEYWORD` / `INVALID_URL`。

**硬规则**

- **cmd.exe：只用双引号** `"` 包含空格、中文、URL 的参数；**不要用单引号** `'`（cmd 不把单引号当字符串定界符）。
- PowerShell：含空格/中文参数也优先双引号；勿照搬 bash 的 `'...'` 习惯去 cmd。
- **Windows / 弱模型优先 `--json-args`**：业务字段放进一个 JSON 对象，避免壳按空格/`?`/`&` 拆碎；**不可**与传统 flag 混用。
- 关键词以 `-` 开头：写成 `--keyword=-AI`，或 `node src/douyin/search-cli.js -- -AI`，或 JSON 里 `"keyword":"-AI"`。

**症状 → 处理**

| 症状 | 先做什么 |
| --- | --- |
| `INVALID_ARGS` / 参数解析错误，且命令里有空格中文或 URL | 整段改成双引号包参数后 **只重试一次**；仍失败 → `--json-args` |
| 关键词被拆成多段、或 URL 的 `?`/`&` 丢失 | 同上；或直接 `--json-args` |
| 混用了 bash 示例里的单引号 | 全部换成双引号，或改用 `--json-args` |

**可复制例（已 cd 到技能目录）**

```bat
REM cmd
node src\douyin\search-cli.js --keyword "AI 教程" --sort 1 --limit 10
node src\douyin\detail-cli.js --url "https://www.douyin.com/video/7123456789012345678"
```

```powershell
# PowerShell
node src/douyin/search-cli.js --keyword "AI 教程" --sort 1 --limit 10
node src/douyin/detail-cli.js --url "https://www.douyin.com/video/7123456789012345678"
```

**`--json-args`（与其它 flag 互斥）**

键名用 schema 字段名（`keyword` / `url` / `sort` / `limit`…），不要写 `--keyword`。热榜命令无业务参数，不必用。

```bat
REM cmd：外层双引号，JSON 内双引号写成 \"
node src\douyin\search-cli.js --json-args "{\"keyword\":\"AI 教程\",\"sort\":1,\"limit\":10}"
```

```powershell
# PowerShell：外层单引号包整段 JSON（最稳）
node src/douyin/search-cli.js --json-args '{"keyword":"AI 教程","sort":1,"limit":10}'
node src/douyin/detail-cli.js --json-args '{"url":"https://www.douyin.com/video/7123456789012345678"}'
```

**绝对路径（未 cd / 工作目录是别的仓库时）**

把下面路径换成本机 Agent 已安装的技能根目录（含 `SKILL.md` 的那一层）。示例按常见 Workbuddy 安装布局书写：

```bat
REM cmd
node "C:\Users\Administrator\.workbuddy\skills\douyin-search-keyword\src\douyin\search-cli.js" --keyword "AI 教程" --sort 1 --limit 10
```

```powershell
# PowerShell
node "C:\Users\Administrator\.workbuddy\skills\douyin-search-keyword\src\douyin\search-cli.js" --keyword "AI 教程" --sort 1 --limit 10
```

> 默认不落盘。需要留底时加 `--save` 或设 `GUAIKEI_ENABLE_LOG=1`，写入系统临时目录 `douyin-guaikei/logs/当天日期/`（与 cwd 无关；热榜除外）。

## 合规

- 仅处理抖音公开数据；调用会把关键词/链接发送至第三方 API（ www.guaikei.com ）。
- 不上传本地文件、不登录、无写操作。数据仅限个人/团队内部分析，禁止违规分发。
- 更多帮助：[抖音选品API常见问题](https://www.guaikei.com)

## FAQ

- **没结果**：放宽关键词或减少限定（`--time 0`），换更常用的词；空结果退出码是 0，属正常。
- **结果太多**：补场景/人群/品牌/时间/账号，并控制 `--limit`。
- **调用失败**：先看退出码——3 = token 问题；2 = 参数问题；1 = 关键词/链接/网络/服务端。完整码表见 [errors.md](errors.md)。
- **`Cannot find module`**：先 `cd` 到本技能目录（含 `SKILL.md` 的那一层），再执行 `node src/douyin/...`；或用上一节绝对路径。
- **播放地址和分享链接有时效**，过期后需要重新获取。图文通常没有播放数和时长。
- **计费与单次上限**以官网说明为准。技能侧硬上限 10000 条/次（按量）；**包月**视频搜索/用户搜索/作品最多 30、评论最多 50，超限为 `PLAN_LIMIT`，不是网络故障。取数成功或 empty 时，信封顶层可能带 `cost`（花费**估算**：包月为 `1`，按次为条数×单价）；热榜与错误响应无此字段。
- **账号安全**：只读能力，不登录/不发布/不点赞/不评论，无封号风险。
- **落盘**：默认不写文件。`--save` 或 `GUAIKEI_ENABLE_LOG=1` 时，搜索/用户搜索/作品/评论/详情写入 `%TEMP%/douyin-guaikei/logs/当天日期/`（文件名带 `${pid}_` 前缀）；热榜不落盘。旧技能目录下的 `logs/` 不再写入，可自行删除。清理示例：PowerShell `Remove-Item "$env:TEMP\douyin-guaikei\logs\*\*.json"`。

口语化指令完整参数表：[options.md](options.md)。GitHub 默认展示与技术人员查阅见仓库根目录 `readme.md`。
