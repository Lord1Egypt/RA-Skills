# 360disk CLI 命令参考

## 运行方式（推荐）

默认推荐 npx（热更新）：

```bash
npx -y -p @aicloud360/360-ai-cloud-disk-cli@latest 360disk <command>
```

回归测试 / CI 建议固定版本（可复现）：

```bash
npx -y -p @aicloud360/360-ai-cloud-disk-cli@<exact-version> 360disk <command>
```

说明：本文档中的 `360disk ...` 命令均可等价替换为上述 npx 形式。

建议先定义命令前缀，避免每行重复输入完整 npx：

```bash
DISK_360_CLI='npx -y -p @aicloud360/360-ai-cloud-disk-cli@latest 360disk'
$DISK_360_CLI dir ls /
```

---

## 全局选项

| 选项 | 说明 | 默认值 |
|---|---|---|
| `--api-key <key>` | API 密钥（覆盖环境变量和本地配置） | — |
| `--env <env>` | 环境：`prod` / `test` | `prod` |
| `--sub-channel <channel>` | 子渠道标识 | `open` |
| `--format <type>` | 输出格式：`json` / `text` | `json` |
| `--quiet` | 仅输出 result 数据 | `false` |
| `--timeout <ms>` | 请求超时（毫秒） | `30000` |
| `--retries <n>` | 失败重试次数 | `0` |

鉴权优先级：`--api-key` > `API_KEY` 环境变量 > `~/.360disk/config.json`

## 执行前快速自检

- 先执行 `$DISK_360_CLI auth whoami`（或 `360disk auth whoami`），确认当前登录状态
- 云盘路径以 `/` 开头；目录路径建议以 `/` 结尾
- 含 `|` 的多路径参数必须整体加引号
- 全局选项放在子命令前（如 `$DISK_360_CLI --quiet dir ls /`）

---

## auth — 鉴权管理

### auth login

```bash
360disk auth login --api-key <api_key> [--env <env>] [--sub-channel <channel>]
```

保存 API Key 到 `~/.360disk/config.json`。

### auth whoami

```bash
360disk auth whoami
```

查看当前鉴权状态（API Key 部分脱敏）。

### auth login-wechat

```bash
360disk auth login-wechat [--qr-mode <mode>] [--qr-file <path>] [--timeout <sec>] [--interval <ms>]
```

使用微信扫码登录（适用于无 API Key 场景）。

| 参数 | 必填 | 说明 | 默认值 |
|---|---|---|---|
| `--qr-mode <mode>` | 否 | 二维码呈现方式：`terminal`（终端字符码）或 `file`（PNG 文件） | `terminal` |
| `--qr-file <path>` | 否 | 与 `--qr-mode=file` 联用，指定 PNG 输出路径（未指定则写入系统临时目录） | — |
| `--timeout <sec>` | 否 | 轮询总超时秒数 | `120` |
| `--interval <ms>` | 否 | 轮询间隔毫秒 | `1500` |

> ```bash
> # 在终端显示字符二维码
> 360disk auth login-wechat
>
> # 生成 PNG 二维码文件
> 360disk auth login-wechat --qr-mode file --qr-file /tmp/qr.png
> ```

### auth logout

```bash
360disk auth logout
```

停止自动备份监听并清除本地配置文件。

---

## user — 用户信息

### user info

```bash
360disk user info
```

返回昵称、QID、存储空间使用、VIP 等级等。

---

## dir — 目录操作

### dir ls

```bash
360disk dir ls [path] [--page <n>] [--size <n>]
```

| 参数 | 必填 | 说明 | 默认值 |
|---|---|---|---|
| `path` | 否 | 目录路径 | `/` |
| `--page <n>` | 否 | 页码（从 0 开始） | `0` |
| `--size <n>` | 否 | 每页数量 | `50` |

> **提示**：`path` 是目录路径（文件夹），示例里建议用类似 `/工作目录/` 这样的目录名，避免和“文档类型”混淆。

### dir mkdir

```bash
360disk dir mkdir <path>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 文件夹路径（如 `/项目/子目录/`） |

---

## file — 文件操作

### file mv

```bash
360disk file mv <src> <dest>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `src` | 是 | 源路径，多个用 `\|` 分隔 |
| `dest` | 是 | 目标文件夹路径 |

> **注意**：`|` 是 shell 管道符，多文件时必须用引号包裹整个 `src`，路径含空格也需加引号。
> ```bash
> # 单文件（路径含空格时加引号）
> 360disk file mv "/我的文档/报告 2026.docx" "/归档/"
> # 单目录（src 末尾 / 可省略，CLI 会自动按目录重试）
> 360disk file mv "/项目资料" "/归档/"
> # 多文件（用引号包裹含 | 的整个参数）
> 360disk file mv "/文档/a.txt|/文档/b.txt" "/归档/"
> ```

### file trans-copy

```bash
360disk file trans-copy <src> <dest> [--delete <0|1>] [--replace <0|1>] [--src-ks-id <id>] [--new-ks-id <id>]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `src` | 是 | 源文件完整路径，多个路径用 `\|` 分隔 |
| `dest` | 是 | 目标目录路径（必须以 `/` 开头） |
| `--delete <0\|1>` | 否 | 是否删除源文件：`1`=转移，`0`=复制（默认 `1`） |
| `--replace <0\|1>` | 否 | 同名处理：`0`=重命名，`1`=覆盖（默认 `0`） |
| `--src-ks-id <id>` | 否 | 源文件所在群组 `ks_id` |
| `--new-ks-id <id>` | 否 | 目标目录所在群组 `ks_id` |

> **注意**：多文件场景下 `src` 含 `|` 时必须加引号。
> ```bash
> # 转移（默认：删除源文件）
> 360disk file trans-copy "/文档/a.txt|/文档/b.txt" /归档/
>
> # 复制（保留源文件）并启用覆盖
> 360disk file trans-copy /文档/a.txt /备份/ --delete 0 --replace 1
> ```

### file rename

```bash
360disk file rename <path> <new_name>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 原文件/文件夹完整路径（文件夹需以 `/` 结尾） |
| `new_name` | 是 | 新名称（仅名称，不含父路径）。文件夹末尾 `/` 可省略，CLI 会自动补齐 |

> **文件与文件夹规则不同：**
> ```bash
> # 文件重命名（new_name 仅文件名）
> 360disk file rename "/文档/草稿.docx" "最终报告.docx"
>
> # 文件夹重命名（new_name 仅目录名，末尾 / 可省略，也可带 /）
> 360disk file rename "/我的知识库/" "新知识库"          # 自动补齐为 新知识库/
> 360disk file rename "/我的知识库/" "新知识库/"         # 显式带 / 也可以
> 360disk file rename "/我的知识库/" "/新知识库/"        # 前导 / 会自动去掉
> ```
> **注意**：文件 `new_name` 不能含 `/`，否则报错并提示改用 `file mv`。

### file rm

```bash
360disk file rm <path> [--batch]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 文件路径，多个用 `\|` 分隔（含 `|` 时整体须加引号） |
| `--batch` | 否 | 批量模式：从 stdin 读取路径列表（每行一个），同时保留 argument 路径 |

> **目录路径**：删除目录时，路径末尾的 `/` 可省略，CLI 会自动补全重试。
> 例如 `/bbb/mydir` 与 `/bbb/mydir/` 均可正确删除目录。

> **注意**：多文件时 `|` 必须在引号内。含大量文件时推荐用 `--batch` + stdin 管道，可彻底绕开 `|` 转义问题。
> ```bash
> # 删除文件
> 360disk file rm /临时/a.txt
> # 删除目录（两种写法均可）
> 360disk file rm /bbb/mydir/
> 360disk file rm /bbb/mydir
> # 多文件（加引号）
> 360disk file rm "/临时/a.txt|/临时/b.txt"
> # 批量删除（macOS/Linux：stdin 管道，推荐；支持文件与目录混合）
> cat paths.txt | 360disk file rm /临时/e.txt --batch
> ```
>
> **Windows 提示**：
> - Windows 不支持 `echo -e "...\\n..." | 360disk file rm ... --batch` 这种删除命令。
> - Windows `cmd` 中带括号的 `(echo ... & echo ...) | ...` 写法也不推荐/不兼容，请不要使用。
> - `cmd` 请改用文件管道：`type paths.txt | 360disk file rm /临时/e.txt --batch`
> - `PowerShell` 可用：`"/临时/c.txt`n/bbb/mydir" | 360disk file rm /临时/e.txt --batch`
>
> **批量模式输出格式**：每项单独记录成功/失败，失败不中断整批。
> ```json
> {
>   "success": true,
>   "result": {
>     "total": 3,
>     "succeeded": 1,
>     "failed": 2,
>     "items": [
>       { "index": 0, "input": "/临时/not-exist.txt", "success": false,
>         "error": "源文件不存在 (errno: 3008)" },
>       { "index": 1, "input": "/临时/a.txt", "success": true },
>       { "index": 2, "input": "/临时/b.txt", "success": false,
>         "error": "源文件不存在 (errno: 3008)" }
>     ]
>   }
> }
> ```

### file search

```bash
360disk file search <keyword> [--type <type>] [--page <n>] [--size <n>]
```

| 参数 | 必填 | 说明 | 默认值 |
|---|---|---|---|
| `keyword` | 是 | 搜索关键词 | — |
| `--type <type>` | 否 | 文件类型：`-1`全部 `0`其他 `1`图片 `2`文档 `3`音乐 `4`视频 | `-1` |
| `--page <n>` | 否 | 页码（从 1 开始） | `1` |
| `--size <n>` | 否 | 每页数量 | `20` |

> **提示**：`--page` 超过最大页数时会返回空结果（Text 格式会显示“无搜索结果”）。可先用较小的 `--page`（如 `1`）验证是否有数据，再逐页翻看。

### file share

```bash
360disk file share <paths>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `paths` | 是 | 文件路径，多个用 `\|` 分隔 |

> **注意**：多文件分享时，含 `|` 的参数必须加引号。
> ```bash
> 360disk file share "/文档/报告.pdf|/文档/数据.xlsx"
> ```

### file url

```bash
360disk file url <path> [--nid <nid>]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 文件路径（与 `--nid` 二选一） |
| `--nid <nid>` | 否 | 文件 NID，指定时忽略 path |

### file node-info

```bash
360disk file node-info <nid> [--ks-ext <0|1>]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `nid` | 是 | 节点 nid（仅支持文件夹/知识库） |
| `--ks-ext <0\|1>` | 否 | 是否返回 `ks_info`：`0`=不返回，`1`=返回（默认 `0`） |

> ```bash
> # 查询基础节点信息
> 360disk file node-info 17454790191978055
>
> # 查询节点信息并返回 ks_info
> 360disk file node-info 17454790191978055 --ks-ext 1
> ```

### file origin-size

```bash
360disk file origin-size <path>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 目录完整路径（必须以 `/` 开头） |

> ```bash
> # 统计目录下所有文件和文件夹（递归）原始大小
> 360disk file origin-size /mcp/ai-test/666/
> ```

### file clear-dir

```bash
360disk file clear-dir <path>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | **单个**目录路径（必须以 `/` 开头；勿用 `\|` 拼多个目录） |

> **注意**：该操作会直接清空目录下文件（不进入回收站），请谨慎执行。多个目录须**多次执行**，勿使用 `path1|path2`。
> ```bash
> # 清空单个目录内容（保留目录）
> 360disk file clear-dir /临时目录/
>
> # 多个目录须分别执行
> 360disk file clear-dir /临时目录A/
> 360disk file clear-dir /临时目录B/
> ```

### file config

```bash
360disk file config --path <path> --command <config:*> --type <ini|json|yaml|yml> [--key <key>] [--value <value>] [--content <text>|--stdin]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--path <path>` | 是 | 配置文件路径（必须以 `/` 开头） |
| `--command <cmd>` | 是 | `config:get` / `config:set` / `config:delete` / `config:list` / `config:read` / `config:write` |
| `--type <type>` | 是 | 配置类型：`ini` / `json` / `yaml` / `yml` |
| `--key <key>` | 否 | 键路径（如 `app.debug`） |
| `--value <value>` | 否 | 写入值（`config:set` 场景） |
| `--content <text>` | 互斥 | 整文件内容（仅 `config:write` 场景，与 `--stdin` 互斥） |
| `--stdin` | 互斥 | 从标准输入读取整文件内容（仅 `config:write` 场景） |

> ```bash
> # 读取 JSON 中某个键
> 360disk file config --path /mcp/app.json --command config:get --type json --key app.name
>
> # 设置 JSON 键值
> 360disk file config --path /mcp/app.json --command config:set --type json --key app.debug --value true
>
> # 读取整个 YAML
> 360disk file config --path /mcp/app.yml --command config:read --type yml
>
> # 写入完整内容（stdin，macOS/Linux）
> cat local-config.json | 360disk file config --path /mcp/app.json --command config:write --type json --stdin
> ```
>
> **Windows 用法**（`config:write` + `--stdin` 需管道输入；cmd 无 `cat`，请用下面写法）：
> - cmd：`type local-config.json | 360disk file config --path /mcp/app.json --command config:write --type json --stdin`
> - PowerShell：`Get-Content .\local-config.json -Raw | 360disk file config --path /mcp/app.json --command config:write --type json --stdin`
>
> **输出**：默认 JSON 时整文件在 `result.data.config`（`config:read`）；`--format text` 时成功提示下会打印配置内容（勿只看第一行成功文案）。

### file save

三种数据源（互斥）：

```bash
360disk file save --url <url> [--dest <path>] [--filename <name>]
360disk file save --content <text> [--dest <path>] [--filename <name>]
360disk file save --stdin [--dest <path>] [--filename <name>]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--url <url>` | 互斥 | **单个**下载地址（勿用 `\|` 拼多个 URL；须分多次 `file save`） |
| `--content <text>` | 互斥 | 直接传入文件内容（支持 `\n` 转换为换行） |
| `--stdin` | 互斥 | 从标准输入读取内容 |
| `--dest <path>` | 否 | 云盘存储路径（以 `/` 开头和结尾） |
| `--filename <name>` | 否 | 保存的文件名 |
| `--rename <0\|1>` | 否 | 同名文件处理策略：`0`=直接替换，`1`=自动重命名（默认） |

> **提示**：`--content` 中的 `\n` 会被 CLI 自动转换为真实换行。若内容较长，推荐使用 `--stdin` 管道输入。
>
> **`--url`**：仅支持**一个**地址；用 `|` 连接多个 URL 会导致 OpenAPI 把整串当作无效 URL（常见 HTTP 404 任务失败）。
>
> **Windows 用法**：
> - cmd：`type report.md | 360disk file save --stdin --dest /文件夹/ --filename report.md`
> - PowerShell：`Get-Content report.md -Raw | 360disk file save --stdin --dest /文件夹/ --filename report.md`
> - cmd 获取目录列表：`dir /a /q | 360disk file save --stdin --dest /备份/ --filename filelist.docx`

### file append

```bash
360disk file append <path> [--content <text>] [--stdin]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `path` | 是 | 云盘文件完整路径（必须以 `/` 开头） |
| `--content <text>` | 互斥 | 追加的文本内容 |
| `--stdin` | 互斥 | 从标准输入读取追加内容 |

> **注意**：`--content` 与 `--stdin` 互斥，必须且只能使用一个。
> ```bash
> # 直接追加文本
> 360disk file append /工作/日志.txt --content "2026-03-31: 完成需求分析"
>
> # 通过管道追加多行内容（macOS / Linux）
> echo -e "line 1\nline 2" | 360disk file append /工作/日志.txt --stdin
>
> # 将本地文件内容追加到云盘（macOS / Linux）
> cat local_log.md | 360disk file append /项目/开发日志.md --stdin
> ```
>
> **Windows 用法**：cmd **没有** `cat`，请用 **`type`** 读本地文件再管道到 `--stdin`：
> - cmd：`type local_log.md | 360disk file append /项目/开发日志.md --stdin`（路径含空格时用 `type "C:\Users\xxx\log.md" | ...`）
> - PowerShell：`Get-Content .\local_log.md -Raw | 360disk file append /项目/开发日志.md --stdin`
>
> **勿在 cmd 使用 `echo -e ... | ...`**：cmd 的 `echo` 不认识 `-e`，会把 **`-e` 连同错误编码的字节** 写进管道，云盘里会出现乱码或（U+FFFD）。多行中文推荐：**`--content "第一行\n第二行"`**（CLI 会展开 `\n`）、或 **`chcp 65001`** 后短文本 `echo`、或 **UTF-8 文件 + `type`/`Get-Content -Encoding utf8`** 管道。新版本 CLI 会尝试 **GBK 解码** 并剥掉误传的 `-e` 前缀，仍建议优先上述写法。

### file exists

```bash
360disk file exists --path <path> --files <json>
360disk file exists --path <path> --stdin
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--path <path>` | 是 | 目标目录，必须以 `/` 开头 |
| `--files <json>` | 互斥 | 待检测文件数组 JSON，如 `[{"fname":"a.txt","fsize":123}]` |
| `--stdin` | 互斥 | 从标准输入读取 `files` JSON |

> **注意**：`--files` 与 `--stdin` 互斥，必须且只能使用一个。
> ```bash
> # 直接传 JSON（macOS / Linux，单引号由 shell 剥掉）
> 360disk file exists --path /AI为我下载/20260331/ --files '[{"fname":"a.txt","fsize":123}]'
>
> # Windows cmd：不支持单引号，须用双引号并对内部双引号转义
> 360disk file exists --path /AI为我下载/20260331/ --files "[{\"fname\":\"a.txt\",\"fsize\":123}]"
>
> # 从 stdin 读取 JSON（macOS / Linux：echo + 单引号由 shell 剥除，管道内为标准 JSON）
> echo '[{"fname":"a.txt","fsize":123},{"fname":"b.txt","fsize":456}]' | 360disk file exists --path /AI为我下载/20260331/ --stdin
> ```
>
> **Windows 说明**：`cmd.exe` 不把 `'` 当作字符串定界符；**也不要在 cmd 里使用 `echo '[...]' | ... --stdin`**——`echo` 会把单引号一并输出，管道里是非法 JSON。长 JSON 或 stdin 模式请把 **UTF-8** JSON 写入文件后：`type files.json | 360disk file exists --path /目录/ --stdin`；PowerShell：`Get-Content .\files.json -Raw -Encoding utf8 | ...`。`--files` 在 cmd 下请用双引号转义写法（见上）。CLI 会尽量剥掉外层 `'` 并修正 `\"`，仍推荐 cmd 优先双引号 `--files` 或 **`type` 管道 `--stdin`**。PowerShell 的 `--files` 可用单引号整段 JSON（无需 `\"`）。

### file upload

```bash
360disk file upload <files> [--dest <path>]
```

| 参数 | 必填 | 说明 | 默认值 |
|---|---|---|---|
| `files` | 是 | 本地文件路径，多个用逗号分隔 | — |
| `--dest <path>` | 否 | 云盘目标路径 | `/` |

### file download

```bash
360disk file download <nid> [--dir <path>] [--no-auto]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `nid` | 是 | 文件 NID（通过 `dir ls` 或 `file search` 获取） |
| `--dir <path>` | 否 | 本地下载目录（默认 `~/.mcp-downloads`） |
| `--no-auto` | 否 | 仅获取下载链接，不自动下载 |

---

## completion — Shell 补全

### completion install

```bash
360disk completion install [--bash] [--zsh]
```

自动检测 shell 类型并安装补全脚本到 `~/.360disk/completion.{bash,zsh}`。

### completion uninstall

```bash
360disk completion uninstall [--bash] [--zsh]
```

### completion script

```bash
360disk completion script [--bash] [--zsh]
```

输出补全脚本到 stdout，可通过 `eval "$(360disk completion script)"` 临时加载。

---

## 错误码参考

| 退出码 | 名称 | 含义 |
|---|---|---|
| `0` | SUCCESS | 成功 |
| `1` | GENERAL | 一般错误 |
| `2` | INVALID_ARGS | 参数错误 |
| `3` | AUTH_ERROR | 鉴权错误（未登录、Key 无效） |
| `4` | NOT_FOUND | 资源不存在 |
| `5` | PERMISSION_DENIED | 权限不足 |
| `6` | NETWORK_ERROR | 网络错误/超时 |
| `7` | CONFLICT | 资源冲突（文件已存在） |
| `8` | SERVER_ERROR | 服务端错误 |
| `10` | QUOTA_EXCEEDED | 配额超限（空间不足） |

常见错误的推荐处理：

- `3`（AUTH_ERROR）：执行 `auth whoami` / `auth login` 后重试
- `4`（NOT_FOUND）：先用 `dir ls` 或 `file search` 校验路径
- `6`（NETWORK_ERROR）：增加 `--retries 2 --timeout 60000` 重试

---

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `API_KEY` | 云盘 API 密钥 | — |
| `ECS_ENV` | 环境（`prod` / `test`） | `prod` |
| `SUB_CHANNEL` | 子渠道标识 | `open` |

---

## claw-backup — 本地备份到云盘

```bash
360disk claw-backup --source <path> --dest <path> [--force]
360disk claw-backup --source-dir <path> --claw-name <name> [--force]
```

两种使用模式（互斥）：

| 模式 | 参数组合 | 说明 |
|---|---|---|
| 标准备份 | `--source` + `--dest` | 将单个本地文件或目录上传到指定云盘目录 |
| OpenClaw 模式 | `--source-dir` + `--claw-name` | 按 OpenClaw 白名单配置，只备份特定目录和文件 |

| 参数 | 必填 | 说明 |
|---|---|---|
| `--source <path>` | 互斥 | 本地源文件或目录（标准备份模式） |
| `--dest <path>` | 互斥 | 云盘目标目录（标准备份模式，以 `/` 结尾） |
| `--source-dir <path>` | 互斥 | OpenClaw 本地根目录（OpenClaw 模式） |
| `--claw-name <name>` | 互斥 | 云盘中的 OpenClaw 备份目录名（OpenClaw 模式） |
| `--force` | 否 | 强制上传文件，跳过本地增量数据库比对；上传成功后仍更新数据库 |

> **说明**：`claw-backup` 内置增量比对（基于本地 SQLite 数据库），默认只上传变更文件。`--force` 可跳过比对强制全量上传。
>
> ```bash
> # 标准备份：将本地 ~/.cc-switch 目录备份到云盘 /cc-switch-backup/
> 360disk claw-backup --source ~/.cc-switch --dest /cc-switch-backup/
>
> # OpenClaw 模式备份
> 360disk claw-backup --source-dir ~/.cc-switch --claw-name cc-switch-backup
>
> # 强制全量备份（跳过增量比对）
> 360disk claw-backup --source ~/.cc-switch --dest /cc-switch-backup/ --force
> ```

---

## claw-restore — 云盘恢复到本地

```bash
360disk claw-restore --remote <path> --target <path>
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--remote <path>` | 是 | 云盘源目录（以 `/` 开头） |
| `--target <path>` | 是 | 本地目标目录（不存在时自动创建） |

> ```bash
> # 将云盘 /cc-switch-backup/ 递归恢复到本地 ~/.cc-switch-restored
> 360disk claw-restore --remote /cc-switch-backup/ --target ~/.cc-switch-restored
> ```

---

## claw-auto-backup — 自动备份监听

自动监听本地目录变化并实时同步到云盘（后台守护进程）。

### claw-auto-backup enable

```bash
360disk claw-auto-backup enable --source-dir <path> --claw-name <name> [--event-log <path>]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--source-dir <path>` | 是 | 监听的本地根目录（只能是一个目录） |
| `--claw-name <name>` | 是 | 云盘中的 OpenClaw 备份目录名 |
| `--event-log <path>` | 否 | 自动备份事件日志文件路径；仅传入时才写日志 |

> **说明**：`enable` 会在后台启动守护进程并写入状态文件，进程与当前 shell 会话解耦，关闭终端后仍持续运行。
> ```bash
> # 启用自动备份
> 360disk claw-auto-backup enable --source-dir ~/.cc-switch --claw-name cc-switch-backup
>
> # 启用并记录事件日志
> 360disk claw-auto-backup enable --source-dir ~/.cc-switch --claw-name cc-switch-backup --event-log ~/auto-backup.log
> ```

### claw-auto-backup disable

```bash
360disk claw-auto-backup disable
```

停用自动备份监听，终止后台守护进程并更新状态文件。

### claw-auto-backup status

```bash
360disk claw-auto-backup status
```

查看当前自动备份状态，返回 `enabled`、`pid`、上次备份时间、`watch_pairs` 等信息。

---

## Windows 速查

在 Windows 中，建议优先使用以下等价命令：

- 读取文件内容并保存到云盘
  - `cmd`：`type report.md | 360disk file save --stdin --dest /文件夹/ --filename report.md`
  - `PowerShell`：`Get-Content report.md -Raw | 360disk file save --stdin --dest /文件夹/ --filename report.md`
- 将本地配置文件内容写入云盘（`file config` 的 `config:write` + `--stdin`）
  - `cmd`：`type local-config.json | 360disk file config --path /mcp/app.json --command config:write --type json --stdin`
  - `PowerShell`：`Get-Content .\local-config.json -Raw | 360disk file config --path /mcp/app.json --command config:write --type json --stdin`
- 将本地文件内容追加到云盘已有文本（`file append --stdin`，勿用 `cat`）
  - `cmd`：`type local_log.md | 360disk file append /项目/开发日志.md --stdin`
  - `PowerShell`：`Get-Content .\local_log.md -Raw | 360disk file append /项目/开发日志.md --stdin`
- `file exists --files` / `--stdin`（cmd 勿用单引号包 `--files`；**勿用 `echo '...' |`** 走 stdin）
  - `cmd`：`360disk file exists --path /目录/ --files "[{\"fname\":\"a.txt\",\"fsize\":123}]"`
  - `PowerShell`：`360disk file exists --path /目录/ --files '[{"fname":"a.txt","fsize":123}]'`
  - 长 JSON / stdin：UTF-8 存 `files.json` 后 `type files.json | 360disk file exists --path /目录/ --stdin`；PowerShell：`Get-Content .\files.json -Raw -Encoding utf8 | ...`
- 批量删除（stdin 路径列表）
  - `cmd`：`type paths.txt | 360disk file rm /临时/e.txt --batch`
  - `PowerShell`：`"/临时/c.txt`n/bbb/mydir" | 360disk file rm /临时/e.txt --batch`
