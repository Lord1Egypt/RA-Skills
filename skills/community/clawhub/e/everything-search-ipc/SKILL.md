---
name: everything-search
description: 使用 Python 通过 Everything SDK IPC 或本机 HTTP JSON 快速搜索 Windows 本机文件与文件夹，并直接返回完整路径，不依赖 es.exe，也不打开 Everything 图形搜索窗口。支持 SSH、Windows 服务和普通桌面会话，以及定位 Codex 会话产生的 rollout JSONL 日志。适用于用户要求查找本机文件、目录、Codex 对话日志、按 Everything 搜索语法过滤结果、仅返回路径，或明确要求调用 Everything.exe 后台索引能力时。
---

# Everything 本地搜索

通过 `scripts/search_everything.py` 查询正在运行的 Everything 后台索引。默认先使用 SDK IPC；当 SSH、Windows 服务或计划任务与 Everything 搜索客户端不在同一 Windows Session，且 SDK 返回 IPC 错误码 2 时，自动回退到本机 HTTP JSON。优先返回真实搜索结果，不使用递归遍历磁盘代替 Everything 查询。

## 执行流程

1. 确认运行环境为 Windows，并确认 Everything 后台进程正在运行。
2. 按 Python 运行架构选择 Skill 内置的官方 Everything SDK 载荷，支持 x86、x64、ARM 和 ARM64。
3. 首次调用时把匹配的 Base64 文本载荷释放到系统临时缓存，验证 SHA-256 后加载；后续调用复用校验通过的缓存文件。
4. `--dll` 或环境变量 `EVERYTHING_SDK_DLL` 可覆盖内置载荷；只使用与 Python 架构一致的可信文件。
5. 默认使用 `--transport auto`。SDK IPC 错误码 2 时，从 `EVERYTHING_HTTP_URL`、`--http-url` 或 Everything.ini 的 `http_server_port` 发现本机 HTTP 服务并重试。
6. HTTP 通道只接受 `127.0.0.1`、`localhost` 或 `::1`，避免把本机索引查询意外发送到外部主机。
7. 调用脚本执行搜索，并按用户要求返回文件、文件夹或全部结果。
8. 报告实际查询词、结果数量和完整路径。结果为空时明确说明未找到，不猜测路径。

## 常用调用

搜索文件和文件夹：

`python scripts/search_everything.py "everything" --limit 100`

仅搜索文件夹：

`python scripts/search_everything.py "everything" --type folder --limit 100`

仅搜索文件：

`python scripts/search_everything.py "everything" --type file --limit 100`

输出带类型信息的 JSON：

`python scripts/search_everything.py "everything" --type folder --json`

显式指定 SDK DLL：

`python scripts/search_everything.py "everything" --dll "C:\path\Everything64.dll"`

SSH 或 Windows 服务中直接使用 HTTP：

`python scripts/search_everything.py "everything" --transport http --limit 100`

显式指定本机 HTTP 地址：

`python scripts/search_everything.py "everything" --transport http --http-url "http://127.0.0.1:22080/"`

## 查找 Codex 对话日志

Codex 通常把活动会话日志写入当前用户目录下的 `.codex\sessions\年\月\日\rollout-*.jsonl`，归档会话可能位于 `.codex\archived_sessions`。先使用 Everything 按路径、日期、文件名或会话 ID 定位 JSONL，再读取候选文件查找具体对话内容。

按会话 ID 精确定位日志：

`python scripts/search_everything.py "019f8805-4c12-7941-a107-aec371a7eebb ext:jsonl" --type file`

列出指定日期下的会话日志：

`python scripts/search_everything.py "path:\"<用户目录>\.codex\sessions\2026\07\22\" ext:jsonl" --type file`

列出全部活动会话日志：

`python scripts/search_everything.py "path:\"<用户目录>\.codex\sessions\" ext:jsonl" --type file --limit 1000`

定位日志后，使用 `rg -n -i "对话关键词" "完整的 rollout JSONL 路径"` 搜索正文；需要结构化处理时，逐行解析 JSON，不要把整个 `.jsonl` 文件当作一个 JSON 数组。

优先关注 `session_meta`、`turn_context`、`event_msg` 和 `response_item` 记录。活动会话文件可能持续增长，因此报告文件大小和修改时间时注明这是当前快照。只提取用户要求的会话和字段，不整份输出日志；发现令牌、Cookie、密钥或其他敏感值时不得回显。

## 查询规则

- 将用户给出的普通关键词原样传给 Everything。
- 允许使用 Everything 搜索语法，例如 `ext:xlsx 供应商`、`path:"D:\资料"`。
- Everything 的快速路径用于定位 JSONL 文件；按对话正文关键词搜索时，定位后再读取文件内容，不假定文件名索引等同于正文索引。
- 使用 `--type folder` 自动添加 `folder:`；使用 `--type file` 自动添加 `file:`。
- 默认纯文本输出每行一个完整路径，便于 PowerShell、Python 或 RPA 直接读取。
- 不把 `Everything.exe` 当作标准输出客户端；它负责维护索引并提供 IPC 或 HTTP 查询服务。
- SSH、计划任务和 Windows 服务通常与桌面 Everything 客户端处于不同 Session。遇到 SDK IPC 错误码 2 时优先使用本机 HTTP，不优先启动第二个 Everything 客户端。
- HTTP 服务应绑定到 `127.0.0.1`，并关闭不需要的文件下载能力。不要把无认证的 Everything HTTP 服务暴露到局域网或公网。
- Skill 已内置从 voidtools 官方签名 DLL 转换的文本载荷，并在释放前后校验 SHA-256。不要用来源不明的 DLL 或载荷替换；需要覆盖时，只使用与 Python 架构一致的可信文件。

## 故障处理

- 提示找不到 SDK DLL 时，检查 Python 架构和 DLL 文件名是否匹配。
- 提示 IPC 查询失败时，检查 Everything 后台进程是否运行、当前实例是否为默认实例，以及调用进程是否与 Everything 客户端处于同一 Windows Session。错误码 2 在默认 `auto` 模式下会自动尝试本机 HTTP。
- HTTP 回退失败时，确认 Everything 的 HTTP 服务器已启用，端口与 Everything.ini 一致，并可通过 `http://127.0.0.1:<端口>/` 访问。
- 若目标是命名实例，不要假定默认实例可查询；先确认实例配置，再扩展调用参数或使用对应实例的官方接口。
