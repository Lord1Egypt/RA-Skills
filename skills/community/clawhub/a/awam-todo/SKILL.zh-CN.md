---
name: awam-todo
version: 0.7.2
description: >-
  输入与管理 Awam 的 To-Do：在会话中解析用户自然语言里的待办内容、重要性、备注、工作空间目录、
  相关文档、链接与时间，调用脚本追加到按日期划分的存储文件，并自动维护索引（todo / in_progress /
  urgent / done / 归档文件）。新增时会检测相同/近似任务：相同默认更新已有状态（需用户确认），
  近似需用户确认后更新或强制新建。支持**待办依赖链**：可为任务标记前置依赖，推进到「进行中/结束」
  时若前置依赖未结束，脚本硬性拦截（exit 3）并交由 AI 向用户确认后决定是否强制推进。
  支持**子任务**：子任务归属于一个主任务（`--parent`），属性与其他任务一致；把存在未完成子任务
  的主任务标记为「结束」会被硬性拦截，交由 AI 确认。支持**预案**：每条待办可填「最容易拦住我的
  障碍」与「如果它出现，我就……」，卡片与列表直接展示。支持**逾期双出口**：逾期任务给出天数，
  并提供「立即推进」与「调整计划（`postpone` 改截止日）」两个出口；被置顶的任务（逾期/停滞/今天
  到期）一律带置顶理由。支持**存储格式版本**（文件头 `schema: N`、`migrate` 迁移）与**月度归档**
  （进入新月自动把上月已全部完成的日文件合并进 `storage/archive/YYYY-MM.md`）。所有按周统计一律以
  **周一**为起点；数据不足时一律显示「暂无推算」，不编造数字。AI 创建待办时若未给标签，脚本会**推测
  标签但只作为建议值展示**（`suggest-tags` 可只读预取），确认后才写入，不代用户决定分类。
  支持**两条可配置能力**：存储目录（`env --set storage_dir`，旧目录有数据时必须显式选 `--migrate`
  搬迁或 `--no-migrate` 留原处，搬迁先复制、校验一致才删旧）与「用编辑器打开」的编辑器
  （`env --set editor.path`，`init` 自动探测，未配置/失效时报错并停用入口，不猜路径）。
  支持**网页 UI 服务联动**：成功添加/维护待办后自动检查本地网页服务是否在运行，未启动时
  弹框询问是否启动 UI（`ui.port` / `ui.prompt` 可配置）。
  提供**分诊入口（`triage`）**：用纯规则（不依赖大模型）把一句话判定为 新增 / 更新 / 改状态 /
  删除，输出 JSON，拿不准时要求确认；提供**捕获服务（capture）**：全局快捷键读取剪贴板内容
  **不做规则筛选**（剪贴板原文即任务内容），喂给分诊入口，凡需确认/填写一律系统弹框；
  捕获服务融合在网页 UI 服务进程内，由 UI 的**设置页**管理（快捷键与分诊类型开关）。
  **语言策略**：AI 对话跟随用户语言；CLI/API 输出固定英文；网页 UI 中英国际化（默认英文、
  可切中文，内联实现、断网可用）。
  当用户说“记一下/加个待办/帮我记/安排XX/提醒我X日做XX”或显式
  调用 /awam-todo 时使用；也用于列出、完成、标记进行中、重新打开、归档待办、设置依赖、管理子任务。
---

# awam-todo（输入与管理 To-Do）

个人待办管理技能。所有数据落在本技能目录下的 `storage/`（**不纳入 Git 管理**），索引在
`index.json`（**不纳入 Git 管理**），本机环境信息在 `env.json`（**不纳入 Git 管理**，
由 `init` 自动生成）。核心命令见 `scripts/todo.py`（Python 3）。

**文档布局**（本技能包为双语）：
- `SKILL.md` —— 权威运行手册（英文）。
- `SKILL.zh-CN.md` —— 同一运行手册的中文镜像。
- `docs/OPTIMIZATION.md` —— 优化路线图（英文）。
- `docs/优化建议.md` —— 同一路线图的中文版。

## 何时用

| 用户意图 | 执行 |
|----------|------|
| 首次使用 / 换机器后初始化环境 | `init`（识别工作环境、探测编辑器并保存，统一工作空间） |
| 查看 / 修改环境配置（路径风格等） | `env`（可 `--set`、`--reformat-workspaces`） |
| 换存储位置 / 迁移已有的待办数据 | `env --set storage_dir=<目录>` + `--migrate`（见「可配置能力」） |
| 换「用编辑器打开」用的编辑器 | `env --set editor.path=<绝对路径或命令名>`（见「可配置能力」） |
| 新增一条待办 | 解析 → `add`（含重复检测，见下） |
| 检查是否重复 | `check --text "..."`（只读） |
| 只读推测标签（只建议、不写入） | `suggest-tags --text "..."`（JSON 输出） |
| 查看待办 | `list`（可按状态/日期筛选） |
| 完成一条待办 | `done <id>`（前置依赖未结束需确认） |
| 标记进行中 / 重新打开 | `start <id>`（前置依赖未结束需确认） / `reopen <id>` |
| 继续工作（标记进行中并用配置的编辑器打开工作区） | `work <id>`（别名 `continue`，前置依赖未结束需确认） |
| 逾期了：改期 / 取消截止 | `postpone <id> "下周一"`（别名 `reschedule` / `replan`；`--clear` 取消截止） |
| 设置 / 查看任务依赖 | `dep <id> [--add/--remove/--set/--clear] <dep_id...>` |
| 列出某主任务下的子任务 | `children <id>`（别名 `sub`） |
| 新增子任务（归属主任务） | `add --parent <主任务ID> ...` |
| 解除子任务归属 | `deparent <id>` |
| 强制归档某天文件 | `archive YYYY-MM-DD` |
| 月度归档（上月已完成的记录） | `archive-month [--month YYYY-MM] [--all] [--dry-run]`（别名 `monthly-archive`） |
| 旧版本存储迁移到当前 schema | `migrate`（默认预览） / `migrate --apply` |
| 查看索引（紧急/今日/逾期/进行中/开放/已完成） | `index` |
| 查看单条、某天文件或某月归档 | `show <id|YYYY-MM-DD|YYYY-MM>` |
| 对一句话分诊（新增/更新/改状态/删除） | `triage --text "..."`（只读，JSON；退出码 3 = 需要确认） |
| 删除一条待办（同时清理依赖/父任务引用） | `delete <id>` |
| 用全局快捷键捕获剪贴板（不做筛选） | 启动网页 UI（`server.py`）；按快捷键（默认 `Ctrl+Alt+T`）；剪贴板原文喂给分诊入口 |
| 管理捕获服务（快捷键 / 分诊类型 / 开关） | 网页 UI **设置**页，或 `env --set capture.*` |

## 命令速查表

| 命令 | 用途 |
|------|------|
| `add` | 新增待办（相同→默认更新；近似→需确认；`--force` 跳过全部检查） |
| `check` | 只读查重 |
| `suggest-tags` | 只读推测标签（JSON 输出） |
| `done` / `start` / `reopen` | 完成 / 标记进行中 / 重新打开（done、start 带依赖守卫） |
| `work`（`continue`） | 标记进行中 + 用配置的编辑器打开工作区 |
| `postpone`（`reschedule`、`replan`） | 重设 / 清除截止日（逾期第二出口） |
| `dep` | 查看 / 设置 / 追加 / 移除 / 清空依赖 |
| `children`（`sub`） / `deparent` | 列出 / 解除子任务 |
| `archive` / `archive-month`（`monthly-archive`） | 归档某天文件 / 执行月度归档 |
| `migrate` | 预览或执行 schema 迁移 |
| `list` / `show` / `index` | 列出待办 / 查看任务、某天或某月 / 查看索引 |
| `triage` | 对一句话做只读分诊 → 新增/更新/改状态/删除（含解析出的字段），JSON；需确认时退出码 3 |
| `delete` | 删除一条待办（同时清理其他任务对它的依赖/父任务引用） |
| `init` / `env` | 探测并保存环境 / 查看与修改配置 |

## 调用

```powershell
python "<技能目录>\scripts\todo.py" <命令> <参数>
```

`<技能目录>` 指本技能的安装目录（Windows 下通常形如
`C:\Users\<用户名>\.agents\skills\awam-todo`，按实际安装位置替换）。下文命令统一简写为
`python ...\todo.py`。

## 语言策略（三层）

| 层 | 语言 | 说明 |
|----|------|------|
| 会话中的 AI 对话 | **跟随用户语言** | 用户用什么语言就答什么语言（中↔英等）；用户写中文就回中文，写英文就回英文，不固定单一语言。 |
| CLI / API 输出（`todo.py` / `server.py`） | **固定英文** | 所有面向用户的 CLI 输出、argparse help、tkinter 弹框、网页 API 的 error/message 字段与启动日志均为英文。**数据值豁免**：状态（维护 / 进行中 / 结束 / 待开始 / 其他）、重要（重要 / 不重要）、紧急（紧急 / 不紧急）、标签、视图名与存储文件中文键（`状态:` / `重要:` / `内容:` 等）仍是字面中文运行时值——原样传给 CLI、原样展示，不要英化。 |
| 网页 UI（`web/index.html`） | **国际化：默认英文、可切中文** | 词表内联（zh/en），**不引任何外部库**、断网可用。语言偏好存 `localStorage["awam-todo:lang"]`，默认 `en`；顶栏有语言切换器（English / 中文）。表单 `<select>` 提交给后端的 **value 仍是中文数据值**，只有显示标签/选项翻译；`index.json` 里的数据值在 UI 中**原样展示、不做翻译**——如 `pin_reason` 由英文化的 CLI 置顶逻辑生成英文并在 UI 保持英文，状态/重要/紧急/标签等仍为中文。 |

切换 UI 语言只影响**展示**，绝不改数据。AI 在任何语言下都必须继续把中文数据值
（状态 / 重要 / 紧急 / 标签 / 视图名）原样传给 CLI。

## 工作环境识别与路径统一（必读）

`awam-todo` 会自动识别运行环境，并把**工作空间（workspace）路径**统一为一致的格式。

### `init` —— 识别并保存工作环境

首次使用或更换机器后，先运行 `init`：

```powershell
python ...\todo.py init
```

它探测当前工作环境并保存到 `env.json`：

| 字段 | 说明 |
|------|------|
| `path_style` | 路径风格：`windows` / `posix` / `mixed`（自动按 OS 判定，Windows→windows） |
| `platform.os` | 操作系统名（Windows / Linux / Darwin …） |
| `platform.is_windows` | 是否 Windows |
| `platform.python_version` | Python 版本 |
| `platform.hostname` / `platform.cwd` | 主机名 / 当前工作目录 |
| `dirs.skill_dir` / `dirs.storage_dir` | 技能目录 / **生效的存储目录**（可用 `env --set storage_dir` 改） |
| `editor` | **「用编辑器打开」用的编辑器**（`path` / `label` / `args`，由探测或 `env --set editor.*` 写入） |

`init` 会**保留**已保存的存储目录与编辑器配置（不会被重新探测冲掉）；`editor` 未配置时自动探测一次。

`init` 还会把**已有存储文件中的工作空间**统一为当前 `path_style` 的格式（如 Windows 下全部转成
`G:\Projects\...` 反斜杠）。

### Windows 路径统一规则（本机为 Windows 时自动生效）

- **保存（落盘）**：新增待办时，`--workspace` 无论传入正斜杠还是反斜杠，都会统一为
  `G:\Projects\...`（反斜杠）格式后写入存储文件。
- **读取 / 输出**：`list` / `show` / `index` / `add` 汇报时，工作空间一律以 Windows 反斜杠格式展示。
- **只影响工作空间**：`--docs`、`--links`（URL）等不做路径转换。
- 判断标准是 `env.json` 的 `path_style`；未初始化时按当前 OS 推断（Windows→windows）。

### `env` —— 查看 / 修改环境配置

```powershell
python ...\todo.py env                                  # 查看当前环境配置（含存储目录与编辑器）
python ...\todo.py env --set path_style=windows         # 修改路径风格（windows/posix/mixed）
python ...\todo.py env --reset                          # 重新探测环境并覆盖保存（含编辑器）
python ...\todo.py env --set path_style=posix --reformat-workspaces
                                                         # 改风格并同步重写全部工作空间
```

- `--reformat-workspaces`：把全部存储文件中的工作空间统一为当前 `path_style`（可配合改风格使用）。
- 修改即写回 `env.json`；改风格后可重跑 `init` 或直接 `--reformat-workspaces` 让存量数据同步。

## 四条可配置能力（技能必须知晓）

本技能有**四个可配置项**，都存在 `env.json`，都能通过 `env --set` 修改。用户提到「换个地方存待办」
「我用的不是 Cursor」「用 XX 编辑器打开」「网页端口」「别弹启动询问框」「改捕获快捷键」「关掉捕获」时，
走这四条，不要改代码。

### 1. 存储目录 `storage_dir`

| 项 | 值 |
|----|-----|
| 默认 | 技能目录下的 `storage/`（未配置时自动回退到这里） |
| 权威位置 | `env.json` 的 `dirs.storage_dir` |
| 影响范围 | 全部读写：日文件、`archive/` 月度归档、`index.json` 重建 |

```powershell
# 旧目录还有待办时，必须显式二选一，否则报错（退出码 2）且不动配置
python ...\todo.py env --set storage_dir="D:\awam-todo-data" --migrate     # 连数据一起搬
python ...\todo.py env --set storage_dir="D:\awam-todo-data" --no-migrate  # 只改配置，不动数据
```

搬迁语义（`_migrate_storage`，**这是数据安全的硬约束，不要绕过**）：

1. **先复制**到新目录（`YYYY-MM-DD.md` + `archive/`）；
2. **再校验**新旧的文件数与任务块数一致；
3. **校验通过才删除**旧目录文件；
4. 任何一步失败都中止、**保留旧目录原样**，并回滚配置指向原目录，同时回删本次写入的半份副本。

路径支持 `~`、`%VAR%` / `$VAR` 环境变量展开；相对路径按相对技能目录解析。写入前会校验可创建、可写。

### 2. 编辑器 `editor`

「用编辑器打开工作区」（CLI `work`、网页路径菜单）不再写死 Cursor，改用 `env.json` 的 `editor` 段：

| 键 | 说明 |
|----|------|
| `editor.path` | **必填**。编辑器可执行文件绝对路径，或 PATH 里的命令名（如 `code` / `cursor`） |
| `editor.label` | 选填。显示名，用于提示文案与网页菜单（如「用 VS Code 打开」） |
| `editor.args` | 选填。固定前置参数，多个用 `;` 分隔 |

```powershell
python ...\todo.py env --set editor.path="D:\Apps\Cursor\Cursor.exe"      # 绝对路径
python ...\todo.py env --set editor.path=code                             # 或 PATH 里的命令名
python ...\todo.py env --set editor.label="VS Code"
python ...\todo.py env --set "editor.args=--new-window"
python ...\todo.py env --set ui.port=9000          # 网页 UI 服务端口（默认 8796，见第 3 条）
python ...\todo.py env --set ui.prompt=off         # 维护后不弹框询问启动网页 UI（见第 3 条）
```

- `init` / `env --reset` 会**自动探测**常见编辑器（Cursor、VS Code、Trae、Windsurf、Sublime Text、Zed）。
  探测表 `EDITOR_CANDIDATES` 是 `todo.py` 里的常量，想加别的编辑器直接加一行。
- 探测不到就**不写** `editor` 配置，留给你显式指定。
- **未配置或路径失效时一律报错并停用入口**：CLI `work` 打印错误 + 可复制的配置命令（`work` 的主职责
  「标记进行中」已完成，返回码仍为 0）；网页**不渲染**「用编辑器打开」菜单项。
  **不要**退化成「按软件名猜路径」或「静默用系统默认程序打开」。
- 启动编辑器时会切断 stdio 并脱离进程组，避免编辑器占住调用方的管道。

### 3. 网页 UI 服务 `ui`

「添加 / 维护待办后自动检查本地网页服务并询问是否启动 UI」的开关与端口：

| 键 | 说明 |
|----|------|
| `ui.port` | 网页服务端口，默认 `8796`（与 `web/server.py` 默认一致） |
| `ui.prompt` | `ask`（默认）/ `off`。`ask`=维护成功后若服务未启动则**弹框询问**是否启动；`off`=不检查不询问 |

```powershell
python ...\todo.py env --set ui.port=9000          # 改端口（服务未启动时按此端口探测与拉起）
python ...\todo.py env --set ui.prompt=off         # 关闭「维护后询问启动网页 UI」
```

- 临时关闭（自测 / CI / 脚本化调用）：设置环境变量 `AWAM_TODO_UI_PROMPT=off`，优先级高于 `env.json`。
- 该配置只影响 `todo.py` 侧的检查与询问；网页服务本身的端口仍以启动参数为准（`server.py --port`）。

### 4. 捕获服务 `capture`

全局快捷键 + 剪贴板捕获，喂给分诊入口，运行在网页 UI 服务进程内（完整流程见下方「分诊入口与捕获服务」）：

```powershell
python ...\todo.py env --set capture.enabled=false           # 随 UI 启动时不再监听
python ...\todo.py env --set capture.hotkey="Ctrl+Shift+X"   # 改快捷键（UI 启动时按新键注册）
python ...\todo.py env --set capture.confirm_delete=false     # 删除前不确认（不推荐）
python ...\todo.py env --set capture.toast=false              # 捕获后不弹角标提示
python ...\todo.py env --set capture.triage_types.delete=false # 关闭删除分诊（改为「询问 + 回落为新增」）
```

`env` 输出末尾会打印当前捕获配置行
（`Capture service (hotkey reads clipboard -> triage): …`）。非法快捷键与未知子键会被拒绝（退出码 2）。

## 会话中解析（新增待办的核心步骤）

用户用自然语言说一条待办时，按下列字段抽取并传给 `add`；**未给的值用默认值**。

| 字段 | 参数 | 解析规则 | 默认 |
|------|------|----------|------|
| 任务内容 | `--text` | 必填；用户要做的核心事情 | 无 |
| 重要性 | `--importance` | 重要 / 不重要 | 不重要 |
| 紧急 | `--urgent` | 紧急 / 不紧急 | 不紧急 |
| 状态 | `--status` | 维护 / 进行中 / 结束 / 待开始 / 其他 | 进行中 |
| 截止时间 | `--due` | 时间自动解析（见下方映射），未说→ 不设截止 | 无截止 |
| 备注 | `--note` | 用户补充的说明 | 空 |
| 障碍（预案） | `--blocker` | 最容易拦住我的障碍，选填；**卡片与列表直接展示** | 空 |
| 对策（预案） | `--counter` | 「如果它出现，我就……」，选填；与障碍成对出现 | 空 |
| 标签 | `--tags` | 分类标签，多个用 `;` 分隔（如 `工作;学习`）；**未传时脚本会推测并给建议，但不写入**（见下） | 空 |
| 工作空间目录 | `--workspace` | 用户点名某项目/目录（如“放到 XX 项目”） | 空 |
| 相关文档 | `--docs` | 相关文件/文档，多个用 `;` 分隔 | 空 |
| 链接 | `--links` | 相关 URL，多个用 `;` 分隔 | 空 |
| 依赖任务 | `--deps` | 前置依赖任务 ID，多个用 `;` 分隔（如 `T-A;T-B`）；引用须存在且不成环 | 空 |
| 父任务 | `--parent` | 该任务归属的主任务 ID（作为其子任务）；须存在、不得成环 | 空 |
| 来源 | `--from-type` / `--from-url` | 来源类型（agent/link/web）+ 来源链接（如 AI 对话链接）；URL 留空则不记录 | 无来源 |
| 存储日期 | `--date` | 用户点名某天“放在 X 日”→ 存到该日期文件 | 今天 |

### 重复检测（新增必走）

每次 `add` 会先扫描全部存储，比对归一化后的任务内容：

| 结果 | 脚本行为 | Agent 必须做的事 |
|------|----------|------------------|
| **相同**（归一化全文一致） | **不新建**，exit code `3`，列出命中任务 | **向用户确认**；默认选项是 **更新已有任务状态**（推荐 `--update-id <id>`），不要新建重复项 |
| **近似**（相似度 ≥ 约 72%，或一方明显包含另一方） | **不新建**，exit code `3`，列出命中任务 | **向用户确认**：更新指定 ID / 仍要新建 / 取消 |
| 无命中 | 正常新建 | 汇报新建结果 |
| 用户已确认更新 | `add --update-id <id> ...` | 未给 `--status` 时脚本默认设为「进行中」；其它字段仅在显式传入时覆盖 |
| 用户坚持新建 | `add --force ...` | 跳过重复检测强制新建 |

确认话术示例（相同）：

> 已有相同待办 `T-…`（进行中）：……  
> 默认会**更新该任务状态**而不是再建一条。确认更新？还是强制新建 / 取消？

确认话术示例（近似）：

> 发现近似待办 `T-…`（相似度 xx%）：……  
> 请选择：更新该条 / 仍然新建 / 取消。

只读预检可用：`check --text "..."`（有命中同样返回 exit `3`）。

### 标签推测（AI 创建时：只建议，不写入）

AI 在会话中创建待办是**主要创建方式**，标签常常没被用户明说。为减少「建完才发现没分类」，脚本会**推测**
标签，但**绝不代写**——标签是用户的分类体系，推测只能作为**建议值**提交确认。

| 场景 | 脚本行为 | Agent 必须做的事 |
|------|----------|------------------|
| `add` 未传 `--tags`（或传空） | 推测后在输出末尾打印 `建议标签: …（尚未写入；确认后用：add --update-id <id> --tags "…"）` 与 `依据: …` | **向用户复述建议并确认**，确认后再用 `--update-id` 落库 |
| `add` 显式传了 `--tags` | **不推测**，按传入值写入 | 无需额外动作 |
| `add --update-id` 更新已有任务 | **不推测**（走早返回） | 无需额外动作 |
| 推测没把握 | **返回空、不显示任何建议** | 不要追问，也不要替用户编一个标签 |
| 想先问再建（推荐） | `suggest-tags --text "..."` 输出 JSON，字段 `suggestions` / `details` / `reason` / `written:false` | 先拿建议问用户，再一次性 `add --tags "…"` 建好 |

推测依据（三种证据可叠加，把握度达标才出场）：

1. **历史标签复用**：扫描 `storage/` 已有任务，与历史任务文本相关度达标时沿用其标签；
2. **内容/备注关键词**：词表规则（学习 / 英语 / 开发 / 工作 / 文档 / 健康 / 生活 等七类）；
3. **工作空间领域词**：路径中的领域词（如 `src/dev/repo`、`course/learn`、`doc/wiki`）**仅作辅助证据，单独命中不足以成建议**。

英文按**词边界**匹配（`debug` 不会因含 `bug` 而误判为「开发」）。词表与阈值是 `scripts/todo.py` 常量区
集中声明的中文常量（`TAG_RULES` / `TAG_WORKSPACE_RULES` / `TAG_MIN_SCORE` 等），可直接改词改阈值。

> 铁律延续本技能的「不推算原则」：**没把握就不给建议**，宁可让用户自己填，也不要塞一个看着像的标签。

### 依赖链（前置依赖硬检查）

可为任务标记**前置依赖**（其他待办 ID），形成依赖链；依赖检查本身是**死的硬规则**，有冲突时由
**AI 智能推荐处理方式**（向用户确认后执行）。

**设置依赖**（引用须存在的任务 ID；会做存在性与循环依赖检测，自依赖/成环/引用不存在直接报错）：

```powershell
python ...\todo.py dep T-20261002-005                 # 查看依赖
python ...\todo.py dep T-20261002-005 --add T-20261002-001 T-20261002-003   # 追加依赖
python ...\todo.py dep T-20261002-005 --set T-20261002-001                  # 设置（替换）依赖
python ...\todo.py dep T-20261002-005 --remove T-20261002-001               # 移除依赖
python ...\todo.py dep T-20261002-005 --clear                               # 清空依赖
```

也可在新增时用 `add --deps "T-A;T-B"` 直接带上前置依赖。

**硬检查规则（死的）**：目标状态推进到 `进行中`（`start` / `work`）或 `结束`（`done`）时，若
**直接前置依赖未全部 `结束`**，脚本**不落盘**、打印冲突清单并返回 exit `3`（与重复检测同一
“需确认”信号），提示用户确认。`reopen`（回退到待开始）不受依赖约束。

**冲突处理（由 AI 智能推荐）**：当脚本返回 exit `3` 且输出为“依赖检查未通过”，Agent 应结合上下文
向用户给出推荐与选项，例如：

> 该任务依赖 `T-…`（待开始）：……，尚未完成，不能直接推进到「进行中/结束」。
> 请选择：① 忽略依赖强制推进（`--force`）② 先处理/完成前置依赖 ③ 取消。

- 用户确认强制推进 → Agent 加 `--force` 重跑（`done <id> --force` / `start <id> --force` / `work <id> --force`）。
- 前置依赖一旦 `结束`，后续推进自动放行，无需再确认。
- 索引中任务带 `blocked` 字段（是否有未结束前置依赖），`list` 会标注“（被依赖阻塞）”。

**注意**：`add` 的 `--force` 同时是“跳过重复检测”和“跳过依赖硬检查”的统一覆盖开关；不带 `--force`
新建即以 `进行中/结束` 起步且前置未结束时同样会被拦截。

### 子任务（归属主任务）

子任务**归属于一个主任务**，其余属性（状态/重要/紧急/备注/工作空间/文档/链接/截止/依赖）与其他任务
完全一致；一个任务可有父任务，也可有自己的子任务（可嵌套，但父子链不得成环）。

```powershell
python ...\todo.py add --text "打包模块" --parent T-20261002-001        # 新增子任务（归属主任务）
python ...\todo.py children T-20261002-001                             # 列出某主任务下的子任务
python ...\todo.py sub T-20261002-001                                  # 同上（别名）
python ...\todo.py deparent T-20261002-005                             # 解除子任务归属
python ...\todo.py show T-20261002-005                                 # 查看（含 父任务 字段）
```

**父任务完成硬检查（死的）**：把**存在未完成子任务**的任务标记为 `结束`（`done`）时，脚本不落盘、
打印未完成子任务清单并返回 exit `3`（与依赖/重复检测同一“需确认”信号），交由 AI 向用户确认。

**冲突处理（由 AI 智能推荐）**：

> 该主任务还有未完成的子任务 `T-…`（进行中）：……，不能标记为「结束」。
> 请选择：① 忽略子任务强制结束（`--force`）② 先完成子任务 ③ 取消。

- 子任务全部完成后，主任务可正常结束；用户确认强制结束时加 `done <id> --force`。
- 新增 `--parent` 时校验父任务存在、不自引用、不成环；通过 `add --update-id` 或网页更新父任务时同样校验。
- 索引条目含 `parent`（父任务 ID）字段。

### 时间自动解析（`--due` 交给脚本，脚本按以下规则解析）

- 今天 / 今日 → 今天；明天 / 明日 → 明天；后天 → 后天
- 星期X / 周X → 未来最近一次；下周X → 下一周那天
- `X月X日`、`2026-10-05` → 指定日期
- `HH:MM`、`X点`、`X点半` → 今天该时刻
- 相对日期 + 时间组合：`明天 10:00`、`周五 09:00`、`3天后 15:00`
- `X小时后` / `X分钟后` → 以当前时刻推算
- 解析失败则 `--due` 不传（无截止），并在回复中提示用户“未识别到时间，未设截止”。

### 例子

```
用户：记一下，明天上午十点前写好季度报告，重要，备注里带上Q3数据，放到 19AI 项目，
      参考 data.xlsx，附上 https://example.com/report，标签 工作;汇报
→ python ...\todo.py add --text "写好季度报告" --importance 重要 --due "明天 10:00" \
    --note "带上Q3数据" --workspace "G:\Projects\19AI" --docs "data.xlsx" \
    --links "https://example.com/report" --tags "工作;汇报"

# 若 exit 3 且为相同任务 T-20261002-001，用户确认「更新」：
→ python ...\todo.py add --update-id T-20261002-001 --text "写好季度报告" --importance 重要 \
    --due "明天 10:00" --note "带上Q3数据" --workspace "G:\Projects\19AI"

# 若用户坚持新建：
→ python ...\todo.py add --force --text "写好季度报告" ...
```

## 分诊入口（`triage`）—— 一句话 → 新增 / 更新 / 改状态 / 删除

一个**只读、纯规则**的入口，用来判断一句话对待办列表意味着什么。不依赖大模型 —— AI 会话可以直接
用它（比如用户随手贴来一句话），捕获服务也从剪贴板喂给它。它本身从不写任何数据。

```powershell
python ...\todo.py triage --text "把继续detect-agent软件的开发标记为完成"   # stdout 输出 JSON
echo %ERRORLEVEL%   # 0 = 判定明确，3 = 需要确认
```

判定顺序：**删除 > 改状态 > 更新 > 新增**。疑问句（…？）与不含动作动词的句子回落到
`unknown` + `need_confirm`；以「需要/要/必须/应该/记得…」开头且没有命中已有任务时**强制回落为
`add`**（这是承诺新任务）。规则抽取字段：`due`（明天/下周一/3天后/HH:MM…）、重要/紧急、
`备注:`、`标签:`、工作空间路径，以及更新/删除的主体。目标解析：按 T-ID 直接命中，否则按文本相似度
匹配真实任务（优先未结束任务）；锁定不了目标时给 `need_confirm` + `candidates`
（或 `fallback_action=add`）。

JSON 契约（`cmd_triage` 输出）：

| 字段 | 含义 |
|------|------|
| `action` | `add` / `update` / `status` / `delete` / `unknown` |
| `confidence` | `high` / `medium` / `low` |
| `need_confirm` | 执行前是否必须确认（删除永远为 `true`） |
| `reasons` | 需要确认的原因（`destructive` / `question` / `duplicate` / `target_not_found` / `action_disabled` …） |
| `text` | **原句原文，不做任何规则筛选**（这就是被捕获的任务内容） |
| `target` / `candidates` | 命中的任务 `{id, text, score, kind}`（kind：`exact` / `similar`） |
| `status` | `status` 动作的目标状态（结束/进行中/待开始/维护/其他） |
| `fields` | 解析出的附加字段：`due` / `importance` / `urgent` / `note` / `tags` / `workspace` / `text`（更新时） |
| `suggested_tags` | `add` 的只读标签建议（绝不写入） |
| `fallback_action` | 目标缺失时建议的动作（通常是 `add`） |

**AI 会话中的用法**：对用户这句话跑 `triage --text "<原话>"`；若 `need_confirm=true`（或
`action=delete`），先与用户确认，再执行底层命令（`add` / `done`、`start` 表达状态 / `add --update-id`
表达更新 / `delete`）。若 `need_confirm=false` 且 `action=add`，直接用解析出的 `fields` 走 `add`。

## 捕获服务（全局快捷键 → 剪贴板 → 分诊 → 系统弹框）

**不做规则筛选的捕获**：按快捷键时剪贴板里的**原文**原样当作任务内容交给分诊入口。没有关键词过滤、
没有长度限制 —— 剪贴板原文**就是**任务内容。服务运行在**网页 UI 服务进程**（`web/server.py`）内，
随 UI 一起启停，配置走 UI 的**设置页**。

- 启动：运行网页 UI（`python ...\web\server.py`）。启动时注册全局快捷键（默认 `Ctrl+Alt+T`）并打印
  `Capture service: listening: …`。
- 按快捷键：读取剪贴板 → `triage_text` → 应用启用的分诊类型 → 执行：
  - `need_confirm=false`（高置信的新增/改状态/更新）→ 直接执行，弹角标提示（可关）；
  - 否则 → **系统弹框（tkinter）**：展示判定结果，要求确认，并允许补填字段
    （截止时间、标签、备注、重要/紧急、目标选择、新状态）；
  - **删除永远先确认**（可用 `capture.confirm_delete` 关闭）；
  - 被守卫拦截（依赖/子任务/重复）时再弹一个「是否强制」的确认框。
- 弹框语言：标签固定英文；中文数据值（状态 / 重要 / 紧急 / 标签 / 原文）原样展示。
- 停止：停掉网页 UI 进程（Ctrl+C），热键监听随之结束。

配置（都在 `env.json` 的 `capture` 段，可在网页 UI 设置页管理，或 `env --set capture.*`）：

| 键 | 说明 |
|----|------|
| `capture.enabled` | `true`（默认）/ `false` —— 是否随 UI 启动热键监听 |
| `capture.hotkey` | `Ctrl+Alt+T`（默认）。修饰键 `Ctrl`/`Alt`/`Shift`/`Win` + `F1`–`F24`、字母/数字、`Space`、`Enter`、`Tab`、`Esc`；至少一个修饰键 |
| `capture.confirm_delete` | `true`（默认）—— 捕获弹框里删除前必须确认 |
| `capture.toast` | `true`（默认）—— 每次捕获后弹角标提示 |
| `capture.triage_types` | `{add, update, delete, status}` 默认全开；被禁用的动作一律先询问并**回落为 `add`** |

设置页还提供**试用分诊**输入框：粘贴一句话看 JSON 判定结果（只读，POST `/api/capture/triage`），
不会写入也不会执行。

## 预案：障碍 + 对策（选填，但强烈建议填）

每条待办可带一组**实施意图（if-then）**，落盘为 `障碍:` / `对策:` 两行，索引里是 `blocker` / `counter`：

```powershell
python ...\todo.py add --text "背完 2000 个单词" \
  --blocker "晚上刷手机" --counter "拿起手机前先背 20 个"
```

- 两个字段都选填，可只填其一；**网页卡片会直接把预案摆在决策现场**，而不是藏在编辑表单里。
- 汇报/展示任务时，若用户没填，不要替他编障碍与对策——显示「（未填）」即可。
- 会话里用户说"我老是拖延 / 一到晚上就刷手机"这类信息，应主动建议写入这两个字段。

## 逾期、置顶与两个出口

- **逾期天数**：仅当「未完成 + 截止已过（按自然日）」时给出 `逾期 N 天`；无截止、已完成、
  尚未逾期一律没有这个数字（**不显示「逾期 0 天」**）。
- **停滞天数**：进行中且距「更新（无则创建）」≥ `STALL_DAYS`（默认 3 天）→ `已 N 天未推进，滚入今日`。
- **置顶顺序**：逾期（红）> 停滞（琥珀）> 今天到期（蓝）。**凡置顶必带理由**
  （索引里是 `pin` / `pin_reason`），不得静默重排。
- **逾期必须给两个出口**（这是硬要求）：
  1. 立即推进 → `start <id>` / `done <id>`
  2. 调整计划 → `postpone <id> "下周一"`（重设截止）或 `postpone <id> --clear`（取消截止）

```powershell
python ...\todo.py postpone T-20261002-001 "下周一 10:00"   # 改期
python ...\todo.py postpone T-20261002-001 --clear         # 取消截止
python ...\todo.py list --state overdue                    # 只看逾期（带天数与出口提示）
python ...\todo.py list --state today                      # 只看今天要处理（逾期/停滞/今天到期）
```

时间解析不了时 `postpone` 直接报错并保持原值——**不猜日期**。

## 不推算原则（重要）

缺失输入时派生指标一律返回 `None`，渲染成 `—` 或 `暂无推算`：

| 指标 | 有数据 | 无数据 |
|------|--------|--------|
| 逾期天数 | `逾期 N 天` | 不出现该字段 |
| 距截止 | `N 天` | `—` |
| 停滞天数 | `N 天` | `—` |
| 预计完成日 | 需要「进展记录」样本 ≥ 3 条才推算 | `暂无推算（缺少进展记录）` |

当前版本**没有进展记录层**，所以预计完成日恒为「暂无推算」。这是有意为之——记录层的设计见
`docs/优化建议.md` 第 7/8 条。**绝不允许为了"看起来完整"而输出假数字。**

## 周口径（写死，不要临时改）

任何按周统计一律 **周一 00:00 至周日 23:59**（`WEEK_START_ISO = 1`）。索引的 `week` 段给出
`start` / `end` / `created` / `done`。以后做周报环比必须**同口径**对比。

## 存储格式版本与迁移

- 每个存储文件头部写 `schema: N`（当前 `SCHEMA_VERSION = 2`），`index.json` 顶层写 `schema_version`。
- 没有 `schema` 行的旧文件视为 v1；`migrate` 默认只预览，`--apply` 才重写（读出来按当前格式写回，
  补齐 schema 头与新字段默认值，**无损**）。
- 新增字段时：**同步改 `_parse_block` / `_write_block` / `_task_view` / `build_index`，并提升
  `SCHEMA_VERSION`**，否则网页端看不到新字段。

## 月度归档

进入新月份后，把**上月及更早、且全部任务已结束**的日文件合并进 `storage/archive/YYYY-MM.md`，
原日文件删除；仍有未完成任务的日文件**保持不动**。归档文件带 `月份:` / `来源文件:` 头，
每条任务带 `原日期:` 行，可用 `show YYYY-MM` 查看。归档文件不参与日常索引，只在
`index.json` 的 `monthly_archives` / `summary.archived_tasks` 里计数。

自动触发点在 `build_index()` 里（每个进程只跑一次，读命令也可能触发，属预期行为）；
手动触发用 `archive-month`，`--dry-run` 先看计划。

## 可覆盖的默认值（只是预填，不锁死）

`env.json` 的 `defaults` 段控制新增待办的默认 状态 / 重要性 / 紧急：

```powershell
python ...\todo.py env --set defaults.status=待开始
python ...\todo.py env --set defaults.importance=重要
```

网页新建表单用同一份值预填，用户随时可改。默认值是**建议值**，不是约束。

## 数据与状态

- **存储**：`storage/YYYY-MM-DD.md`，每个文件含头部 `归档: true/false`、`schema: N` 与若干任务块
  （`## T-YYYYMMDD-NNN` + `状态/重要/紧急/内容/父任务/备注/障碍/对策/工作空间/文档/链接/标签/依赖/来源/截止/创建/更新` 行）。
  `依赖: T-A; T-B` 记录该任务的前置依赖（任务 ID）；`父任务: T-X` 记录该子任务归属的主任务；
  `标签: 工作; 学习` 记录该任务的分类标签（用 `;` 分隔）。
- **来源 `from`**：可选对象 `{type, url}`，记录待办来源（如某次 AI Agent 对话链接）。由
  `--from-type` / `--from-url` 写入；获取不到对话链接时留空（不落盘、不入索引）。
- **ID**：`T-YYYYMMDD-NNN`，按当天递增，脚本自动生成。
- **状态**：`维护 [ ]` · `进行中 [~]` · `结束 [x]` · `待开始 [ ]` · `其他 [ ]`；新增待办默认「进行中」，不再出现 `open`。
- **重要**：`重要` / `不重要`（默认「不重要」）。
- **紧急**：`紧急` / `不紧急`（默认「不紧急」）；截止在 24 小时内/已过期仍自动视为紧急。
- **归档不变量**：某文件全部任务 `done` → 自动把该文件标 `归档: true` 并记入索引
  `archived_files`；重新打开某任务 → 若不再全部完成，自动取消归档。

## 索引 `index.json`（脚本每次变更后自动重建）

```json
{ "schema_version": 2,
  "generated": "...",
  "summary": {"todo":n, "in_progress":n, "urgent":n, "done":n, "total":n,
              "archived_files":n, "files":n, "today":n, "overdue":n,
              "week_created":n, "week_done":n, "monthly_archives":n, "archived_tasks":n},
  "week": {"start":"YYYY-MM-DD", "end":"YYYY-MM-DD", "created":n, "done":n},
  "urgent": [...], "today": [...], "overdue": [...],
  "in_progress": [...], "todo": [...], "done": [...],
  "archived_files": ["YYYY-MM-DD", ...],
  "monthly_archives": [{"month":"YYYY-MM","files":[...],"file_count":n,"tasks":n}] }
```

索引条目含 `depends_on`（前置依赖 ID 列表）、`blocked`（是否存在未结束前置依赖）、`parent`（父任务 ID）、
`tags`（标签列表）、`blocker` / `counter`（预案），以及派生指标
`overdue_days` / `due_in_days` / `stall_days` / `projected_finish` / `pin` / `pin_reason`
（**无数据一律为 `null`**，展示时渲染「—」/「暂无推算」）。

**排序规则**：向用户展示进度（`list` / `index`）时，若用户未特别说明，默认按
“置顶（逾期 > 停滞 > 今天到期）→ 紧急 → 重要性（重要>不重要）→ 有截止 → 创建时间”排列（脚本内实现）。

向用户汇报时优先用 `index` 的 summary 与这几个桶给一句话概览：**先看 `today`（今天要处理）与
`overdue`（逾期），再看 `in_progress`**；提到逾期时必须同时给出两个出口（推进 / 改期）。

## 前端实现约束（长期有效）

改 `web/index.html` 时必须遵守：

1. **零外部库、零 CDN、零外链字体/图片**——所有 CSS/JS/图标内联，断网可用。
2. **图标用内联 SVG**（文件内 `P` 图标表 + `ic(name, cls)` 助手），**禁止 emoji**。
3. 数据不足时显示「—」/「暂无推算」，**不补 0、不编日期**。
4. 破坏性操作（删除）二次确认；置顶/排序变化必须能解释原因。
5. **悬浮/浮层定位：纵向锚定到触发元素，横向才跟随鼠标**。浮层不能整体跟随鼠标，否则鼠标永远追不上、
   选不中；且多卡片场景下必须取「当前 hover 的那个」浮层，不能用 `document.querySelector()` 取文档第一个。
   浮层与触发元素之间必须用透明桥接带补上间隙，避免鼠标穿过时 `:hover` 断开、浮层消失。
6. 改动后跑自测：`python scripts/selftest.py`（CLI 场景，临时目录，不碰真实数据）
   与 `node scripts/smoke-web.js`（前端渲染冒烟，最小 DOM 桩）。
7. **i18n 内联自包含**：zh/en 词表在脚本内（常量 `I18N`、助手 `tr()`），语言偏好用
   `localStorage["awam-todo:lang"]`、默认 `en`；**禁止**引外部 i18n 库或 CDN（离线约束）。
   只做展示层翻译：`<select>` 的 value 与存储数据保持中文。

## 非目标

- 不做笔记、日历或项目排期；只管理待办本身。
- 不做多人协作 / 同步 / 远程服务。
- `from` 的来源链接只能由 Agent 在会话上下文中取得（如当前 AI 对话链接）；取不到就留空，
  脚本不会自行编造。

## 网页前端展示（web）

当用户要求「用网页展示待办 / 打开看板 / web 查看 / 网页操作待办」时，启动本地网页前端：

```powershell
start-awam-todo.cmd                      # 统一入口：先停残留旧服务，再同时启动 UI 后端 + 捕获服务
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\start-awam-todo.ps1" [-NoBrowser]
python "...\awam-todo\web\server.py"     # 直接启动；捕获服务就在同一进程内一起起
python "...\awam-todo\web\server.py" --port 9000  # 指定端口
```

- **推荐统一入口是 `start-awam-todo.cmd`**（或其调用的 `.ps1`）：先停掉**残留的旧 awam-todo 服务**
  （占用端口的遗留进程，含以相对路径 `web\server.py` 启动的），等端口释放，再在**同一个进程里同时启动**
  网页 UI 后端与捕获服务，最后自检 `/api/settings` 并打印捕获服务状态（`Capture service state: running`）。
  如果设置页之前显示「服务未运行 / 加载失败」，通常就是升级前的旧服务进程还占着端口 —— 重新跑这个入口即可修复。
- 服务常驻后台，浏览器访问 `http://127.0.0.1:8796/`。
- **维护后自动检查与询问启动（LLM / CLI 通用）**：成功**添加 / 维护**一条待办后
  （`add` / `add --update-id` / `done` / `start` / `work` / `reopen` / `postpone` /
  `dep` 改动 / `deparent`），脚本会检查本地网页服务是否在运行——**未运行**时弹出对话框询问
  「是否现在启动网页 UI」：用户选择启动则后台拉起 `web/server.py` 并自动打开浏览器；
  选择不启动则跳过。服务已在运行时不做任何打扰。
  - 关闭询问：`env --set ui.prompt=off`（临时关闭用环境变量 `AWAM_TODO_UI_PROMPT=off`）。
  - Agent 注意：弹框由脚本直接弹出、用户点击后脚本自行拉起服务，Agent 只需按脚本输出
    汇报结果；若脚本提示「无法弹框」（无图形环境），Agent 应在会话中向用户确认是否启动，
    确认后运行 `server.py` 的启动命令。
- 网页支持：列表展示与统计、按状态/标签筛选、关键词搜索、**增删改查**、状态流转（开始/完成/重开/待开始）、
  重复检测确认（相同/近似）、依赖链与子任务冲突确认（可强制推进）。
- **视图**：`全部 / 今日 / 进行中 / 待开始 / 已结束 / 紧急 / 逾期`。
  「今日」= 逾期 + 停滞 + 今天到期，每条都带置顶理由，顶部有一句口径说明。
  **「今日」是视图而不是入口**——默认落在「全部」。
- **预案**：新增/编辑可填「障碍」「对策」（`;` 无需分隔，单行文本）；卡片直接展示；搜索也会匹配预案内容。
- **逾期双出口**：逾期卡片上直接给「立即推进」与「调整计划」两个按钮；「调整计划」弹出输入框，
  支持自然语言时间（明天 / 下周一 / 3天后），也可一键清除截止。
- **三档响应式**：手机（<640）单列 + 底部 Tab；平板（640–1023）顶部横向导航；
  桌面（≥1024）左侧固定边栏（视图/标签/口径信息）+ 多栏卡片网格。
- **图标全部内联 SVG，不使用 emoji**；语义色三态：绿=已完成，红=逾期，琥珀=停滞/容错（区别于错误）。
- **首尾双新建入口**：顶部「＋新增待办」按钮 + 列表底部的大号虚线「新增待办」卡。
- **标签**：新增/编辑可填标签（`;` 分隔）；卡片显示 `#标签` 徽章；工具栏有标签下拉过滤（含各标签计数）。
- **工作空间浮动菜单跟随鼠标**：悬浮在项目路径上时，操作菜单（复制路径 / 打开目录 / 用编辑器打开）
  以鼠标位置为弹出中点（水平居中、略低于光标），跟随鼠标移动；移入菜单后锁定，方便点击。
- **「用编辑器打开」按配置渲染**：菜单项文案取自 `env.json` 的 `editor.label`（如「用 VS Code 打开」）；
  `editor` 未配置或路径失效时**整个菜单项不渲染**，避免点了没反应。对应接口
  `POST /api/workspace/editor`（`/api/workspace/cursor` 为历史别名）。**网页只改文案，不提供配置界面**——
  配置一律走 CLI `env --set`。
- **延迟保存（patch 机制）**：网页操作不再实时写文件，所有修改先在浏览器内存 + 浏览器存储
  （`localStorage`：`awam-todo:baseline` / `awam-todo:pending`）中暂存为 patch 队列；保存时一次性
  `POST /api/todos/apply-patches` 对比**当时最新的文件**应用 patch 后落盘，避免与命令行并发写冲突。
  **保存前做变更比较**：将写入的内容与磁盘当前内容逐字对比，完全一致（如提交了与现值相同的字段、
  相同状态、删除已不存在的任务）则不写文件、不重建索引（响应 `changed=0`），避免无谓重写。
  保存时机：① 页面上点「保存更改」② 自动保存（间隔可在页面上配置，默认 10 分钟，存
  `awam-todo:autosave-min`）③ 关闭/刷新页面时自动 `sendBeacon` 保存。未保存更改有徽章计数；
  若上次关闭时有未保存更改，重开页面会提示恢复。
- 后端复用 `todo.py` 的解析 / 校验 / 索引逻辑；命令行改动后网页端保存时会自动合并到最新文件
  （`external_changed=true` 时提示「检测到外部修改，已合并保存」）。
- 停止：在运行窗口按 Ctrl+C（或结束对应 python 进程）；再用统一入口（`start-awam-todo.cmd`）重启时
  会自动停掉端口上的残留旧服务。

REST API（仅本机）：
- `GET    /api/todos`               列表 + 摘要（可 `?state=`、`?q=`、`?tag=` 过滤；含 `revision` 文件指纹）
- `GET    /api/todos/<id>`          单条任务
- `POST   /api/todos`               新增（重复检测命中返回 409 + duplicates，可 `force` / `update_id`）
- `PUT    /api/todos/<id>`          更新字段（含状态，带依赖/子任务守卫）
- `PATCH  /api/todos/<id>/status`   仅改状态（冲突返回 409 + conflicts，可 `force`）
- `DELETE /api/todos/<id>`          删除（同时清理其他任务对它的依赖 / 父任务引用）
- `POST   /api/todos/apply-patches` 批量应用 patch 一次性落盘（网页延迟保存入口）
  body: `{"revision": <GET /api/todos 返回的指纹>, "patches": [{"op":"create|update|status|delete", ...}]}`；
  保存前对比 revision 与当前文件指纹，不一致时把 patch 应用到最新文件（合并语义），响应含
  `external_changed`、`failed`（duplicate/conflict/not_found）、`id_map`（temp_id → 正式 ID）、
  `changed`（实际写盘文件数；0 表示内容与磁盘一致，未写入）。
- `POST   /api/workspace/open`      用系统文件管理器打开目录
- `POST   /api/workspace/editor`    用 env.json 配置的编辑器打开目录（`/api/workspace/cursor` 为历史别名）
- `GET    /api/settings`            捕获服务配置 + 当前服务状态
- `PUT    /api/settings`            更新捕获设置
  （`{capture:{enabled,hotkey,confirm_delete,toast,triage_types}}`）；立即重新注册快捷键，
  响应里带新的服务状态
- `POST   /api/capture/triage`      对 `{text}` 跑分诊入口 —— 与 CLI `triage` 同一 JSON 契约（只读）

启动时若发现旧服务已占端口，先结束原 python 进程再重启。网页改动与命令行 `todo.py` 完全同源，
任一端操作后另一端看到的都是最新状态。
