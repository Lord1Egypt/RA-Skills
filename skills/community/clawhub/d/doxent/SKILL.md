---
name: doxent
description: "当用户要读取或操作 Doxent / 办公本 / 读写笔记中的真实数据时使用：搜索、读取、创建、重命名、移动或删除笔记和文件夹；导入或上传书籍；查看、创建、修改、删除、完成或移动日程、提醒、待办和任务。也用于安装、启动、登录、停止或更新 Doxent CLI。覆盖“写笔记并保存到办公本”“上周创建了哪些笔记”“明天提醒我开会”等表达。不要用于仅生成聊天文本、编辑本地文档或操作其他应用数据，除非用户明确要求保存到 Doxent。"
slug: doxent
displayName: 智能办公本助手
version: 1.3.6
license: MIT
---

# doxent

统一的 Doxent skill，当前支持：**note**、**book**、**schedule**。

## 概览

这个 skill 是 Doxent / 读写笔记真实数据操作的统一入口。
当用户目标涉及真实笔记、书架文件、日程或任务时，先命中 `doxent`，再按意图路由到具体模块。

## 路由优先级

- 只要一句话里同时出现“时间表达” + “事项/动作”，默认优先路由到 `schedule`。
- 这里的时间表达包括但不限于：`今天`、`明天`、`后天`、`今晚`、`明早`、`下午`、`9点`、`3:30`、`下周一`、`周五前`、`月底`。
- 这里的事项/动作包括但不限于：`开会`、`约`、`提醒`、`安排`、`改到`、`延期`、`提前`、`完成`、`提交`、`处理`。
- 即使用户没有说“日程 / 任务 / 提醒 / event / task”，也不要优先理解成 `note`。
- 只有当用户明确说“写笔记”“记一条笔记”“写会议纪要”“生成摘要”“记录这段内容”时，才优先路由到 `note`。

## 环境说明

> 运行时依赖见 `meta.json`。

## CLI 生命周期与登录

所有 API 请求都通过 `shared/scripts/doxent_api.py`。脚本按 `DOXENT_CLI_PATH`、用户级 CLI 目录、`app_launch.json` 和 Doxent 安装目录的顺序查找 CLI；入口缺失时按当前系统与 CPU 架构自动下载。Windows 保存为 `%LOCALAPPDATA%\Doxent\CoreCLI\doxent-cli.exe`；macOS/Linux 下载各自发布文件后统一重命名为 `~/.local/bin/doxent-cli`、赋予执行权限，并把该目录和 `DOXENT_CLI_PATH` 幂等写入登录 shell 环境。无论平台，后续命令都使用 `doxent-cli xxxx` 语义。即使本地服务已经健康，也要先完成一次轻量版本指纹检查，不能跳过更新判断。

- Doxent CLI 无参数即可启动后台 Core；不要传 Ainote 专用的 `--background-open-model`。
- 启动时自动复用 `DOXENT_NODE`、系统 PATH 或 Codex 自带的 Node 18+ 运行时，并把路径注入隐藏子进程；不得要求用户手工安装 Node 或配置 PATH。
- 通过 skill 启动、登录、帮助或停止 CLI 时必须使用隐藏控制台模式，不要弹出新的终端窗口；登录交互只允许打开本机浏览器登录页。
- 首次启动或 CLI 会话失效时，CLI 会打开仅限本机的 Web 登录页；需要登录时等待用户在浏览器完成登录，不要把账号密码写入命令、日志或请求体。
- 已有 CLI 会话会被复用；可使用 `$PYTHON_BIN shared/scripts/doxent_api.py --cli-action login` 打开账号管理页，或使用 `--cli-action logout` 清除 CLI 会话。
- Doxent CLI 是常驻后台 daemon，关闭当前终端不会停止它。只有用户明确要求停止时，才执行 `--cli-action stop`。
- CLI 参数以当前安装版本的 `doxent-cli --help` 为准。安装 skill 后首次排障或发现参数不兼容时先运行 `--cli-action help`，不要自行假设存在 `--version`。
- CLI 自动安装不需要管理员权限；下载采用临时文件、平台格式、最小体积和 SHA-256 校验后再原子落盘。Windows 校验 PE 文件头，macOS/Linux 校验带内嵌 payload 标记的 POSIX 单文件。云端 `ETag`、`Last-Modified` 或文件摘要发生变化时，即使语义版本号未变化，也要停止旧 daemon、替换用户级 CLI 并自动重新启动。CLI 重新构建后必须重新上传该平台/架构地址对应的文件。
- CLI 启动后立即执行一次增量同步，之后每 30 分钟执行一次增量同步；调用方必须提示用户“正在同步数据，请稍候”。共享 API 客户端最长等待 5 分钟，并轮询本机 `/sync/status`；只有最近一轮同步明确成功后才继续操作业务数据，不能把同步前或部分失败后的缓存当作最新结果。
- 如果同步等待超时，必须停止本次业务请求并提示用户稍后重试，不能降级为返回可能过期的数据。

## 模块路由

| 用户意图 | 模块 | 读取 |
| --- | --- | --- |
| 搜索笔记、读取正文、创建/移动/重命名/删除笔记或文件夹 | note | `note/SKILL.md` |
| 上传书籍、本地文件导入、远程 URL 导入书架 | book | `book/SKILL.md` |
| 查看日程、创建/修改/删除事件、提醒、待办或任务，以及任何用自然语言表达的时间安排请求（如“明天早上9点开晨会”） | schedule | `schedule/SKILL.md` |

## 共享规则

- 端口与健康检查：`shared/port-and-health.md`
- 写操作与同步：`shared/write-and-sync.md`


## 网络请求规则

**强制，无例外**：所有 Doxent API 调用必须通过 `shared/scripts/doxent_api.py` 发送，禁止直接使用 `Invoke-RestMethod` 或 `curl`。
**强制，无例外**：不要裸调用 `python`。优先使用环境变量 `DOXENT_PYTHON`；如果为空，在 macOS / Linux / zsh / bash 下使用 `python3`，在 Windows 下使用 `py -3` 或 `python3`。
**强制，无例外**：先把当前已加载 `SKILL.md` 所在目录解析为 `DOXENT_SKILL_ROOT`，再调用其中的脚本；不得假设项目内存在固定的 Skill 副本，也不得要求用户查找或输入 Skill 安装路径。

> **原因**：PowerShell 5.1 在两个环节都会静默损坏中文：① 请求 Body 从 UTF-8 重编码为 GBK；② 命令行参数传递给外部进程时同样如此。因此 `--body '...'` 字符串参数在 Windows 下**不安全**，必须改用文件。

### GET 请求

```bash
PYTHON_BIN="${DOXENT_PYTHON:-python3}"
"$PYTHON_BIN" "$DOXENT_SKILL_ROOT/shared/scripts/doxent_api.py" \
    --url "http://127.0.0.1:46588/open-model-schedule/health" \
    --token "$TOKEN"
```

### POST / PUT 请求（必须使用 --body-encoded）

```bash
# 1. 构建 JSON
PYTHON_BIN="${DOXENT_PYTHON:-python3}"
body='{"type":"event","title":"标题","startTime":1234567890}'

# 2. URL percent-encode（输出纯 ASCII，彻底绕过所有编码层）
encodedBody=$("$PYTHON_BIN" -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$body")

# 3. 通过 --body-encoded 传给脚本
"$PYTHON_BIN" "$DOXENT_SKILL_ROOT/shared/scripts/doxent_api.py" \
    --url "http://127.0.0.1:46588/open-model-schedule/create" \
    --method POST \
    --body-encoded "$encodedBody" \
    --token "$TOKEN"
```

> **为什么 URL 编码最安全**：URL percent-encode 会把所有非 ASCII 字符（含中文）转为 `%E6%99%A8` 这样的纯 ASCII 序列。ASCII 不受任何编码层影响，Python 收到后 `unquote` 还原为正确 Unicode，再 encode('utf-8') 发送。
>
> ❌ **绝对不要这样写**（中文必乱码）：
> ```powershell
> python doxent_api.py --body '{"title":"标题"}' ...
> ```

脚本执行真实数据请求时会先确保 CLI daemon 已启动，完成请求后保持 daemon 运行，不会主动停止；调用方不要重复手写端口探测、启动或停止逻辑。只有用户明确要求停止时才使用 `--cli-action stop`。


## 响应风格

默认输出结构：
- `结果`
- `命中项`
- `补充说明`
- `下一步`

高风险动作确认结构：
- `待操作对象`
- `定位依据`
- `风险提示`
- `等待确认`

特殊格式要求：
当需要输出展示笔记标题或列表，日程标题或列表时，务必使用以下格式
- 笔记来源：按 `📝[标题](doxent://note/id)` 格式输出
- 日程来源：按 `📅[标题](doxent://schedule/id)` 格式输出

## 示例

- “帮我搜一下周报并读正文” → 进入 `note/SKILL.md`
- “总结本周笔记要点” → 进入 `note/SKILL.md`
- “把这个 pdf 传到书架” → 进入 `book/SKILL.md`
- “帮我新建明天下午两点的提醒” → 进入 `schedule/SKILL.md`
- “明天早上9点开晨会” → 进入 `schedule/SKILL.md`
- “提醒我今晚八点交周报” → 进入 `schedule/SKILL.md`
- “加个待办，周五前提交方案” → 进入 `schedule/SKILL.md`
- “把今天下午的会议改到4点” → 进入 `schedule/SKILL.md`
