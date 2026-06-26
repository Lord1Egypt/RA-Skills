# file-change-tracker

一个给 OpenClaw 文件修改流程加保护的 skill。

它的目标很直接。在任务准备修改文件时，先为**明确知道会改动的目标路径**建立一个可靠的本地 Git 恢复点。任务结束后，如果这些目标路径里产生了新的文件改动，就把修改结果也记录下来，并把最近几次提交记录和可用的回退方式展示给用户。

这个 skill 不是为了替代正常的版本管理流程，而是为了在模型执行写文件、批量替换、代码生成、配置调整这类操作时，尽量把“先留后手，再继续修改”变成默认动作。

当前实现采用**显式路径范围**。它不会默认按整个仓库去做快照，而是按本次任务明确声明的文件或目录路径工作。

## 核心能力

这个 skill 主要做三件事。

### 1. 在修改前为目标路径创建保护快照

当任务会写文件时，先执行 `pre`，并把预计会改动的文件或目录路径明确传给脚本。

它会确认当前目录是否已经是 Git 仓库，并在需要时补齐最基本的本地配置。随后只针对这些目标路径判断是否已经存在未提交改动。

- 如果当前仓库已经有一个干净的 `HEAD`，并且目标路径没有待保存变化，它会直接把这个 `HEAD` 当作修改前恢复点
- 如果目标路径已经存在未提交改动，它会先把这些目标路径的现场保存成一个本地提交，避免后续写操作把目标范围内已有改动混在一起
- 如果仓库还没有首个提交，它会补一个初始化锚点，确保后续快照和回退都有落点

### 2. 在修改后记录目标路径的结果快照

任务完成后执行 `post`。

它会读取 `pre` 阶段保存的目标路径集合，并只检查这些路径里是否真的带来了新的变化。

- 如果存在有效的 PRE 快照并且这些目标路径里有新改动，就创建一个 `guard(post)` 本地提交作为结果快照
- 如果这些目标路径里没有新改动，就不创建无意义提交，而是明确报告这次没有新增快照
- 如果当前会话没有先执行 `pre`，它不会静默继续，而是直接报错提醒先建立修改前恢复点
- 如果目标路径集合发生变化，也不会静默放宽范围，而是要求重新执行一次 `pre`

### 3. 把当前文件记录和回退方式告诉用户

任务结束后，可以执行 `report`、`recent`、`sessions` 和 `rollback-help`。

这样用户能立刻知道。

- 当前保护会话对应的是哪组目标路径
- 当前或最近一次保护会话的状态和备注是什么
- 当前目标路径最近几次提交记录是什么
- 最近几次保护会话是什么
- 本次保护作用在哪个仓库
- 当前是否启用了额外排除文件
- 本次保护覆盖了哪些目标路径
- PRE 和 POST 快照分别是什么
- 想撤回本次改动时有哪些常见方式

这正是这个 skill 的使用重点。它不只是“顺手 commit 一次”，而是把**修改前保护、修改后留痕、结果对用户可见**串成一个完整动作。

## 适用场景

适合这些场景。

- 修改代码文件
- 修改配置文件
- 批量替换文本
- 重构
- 自动生成文件到已知目录
- 运行会落盘的命令或脚本，且输出路径已知

不适合这些场景。

- 纯只读分析
- 纯搜索
- 纯解释
- 只查看差异但不落盘
- 最终会改哪些文件还完全不清楚的任务

## 工作方式

脚本入口在。

```bash
{baseDir}/scripts/helper.sh
```

它支持六个子命令。

```bash
{baseDir}/scripts/helper.sh pre "reason" -- <path> [<path> ...]
{baseDir}/scripts/helper.sh post "reason" [--session <session-id>]
{baseDir}/scripts/helper.sh recent [count]
{baseDir}/scripts/helper.sh sessions [count]
{baseDir}/scripts/helper.sh report [count]
{baseDir}/scripts/helper.sh rollback-help [--session <session-id>]
```

### `pre`

用于记录修改前恢复点。

它会完成下面这些动作。

- 检查当前目录是否是 Git 仓库，不是则初始化
- 检查当前仓库是否配置了 repo-local 的 `user.name` 和 `user.email`
- 接收这次任务准备改动的目标路径列表
- 只在这些目标路径范围内检查工作区、暂存区和未跟踪文件状态
- 在必要时把这些目标路径保存为 `guard(pre)` 提交
- 为本次会话创建独立状态目录 `.git/.guarded-edit/sessions/<session-id>/`
- 把会话状态写到 `.git/.guarded-edit/sessions/<session-id>/state.bin`
- 把目标路径集合写到 `.git/.guarded-edit/sessions/<session-id>/paths.nul`
- 用 `.git/.guarded-edit/current-session` 标记当前活跃会话

### `post`

用于记录修改后的结果状态。

它会完成下面这些动作。

- 读取前一步写入的 session 信息和目标路径集合
- 如果没有有效的 PRE 快照，直接报错并停止
- 只检查这些目标路径里是否还有新的未提交变化
- 在必要时创建 `guard(post)` 提交
- 如果没有新变化，则只报告 `POST_NONE`

### `recent`

用于展示最近几次本地提交记录。

默认显示最近 5 条提交。

如果当前存在活跃或最近一次保护会话，并且能读到这次会话保存的目标路径集合，那么它会优先只展示这些目标路径对应的最近提交记录，而不是直接展示整个仓库的提交历史。

如果当前没有可用会话，或者没有保存到目标路径集合，才会退回到整个仓库的最近提交记录。

### `sessions`

用于展示最近几次保护会话记录。

默认显示最近 5 条会话。

输出里会包含会话 ID、当前状态、备注，以及对应的 PRE 和 POST 提交摘要。当前会话会带 `*` 标记，方便在有多个会话时快速定位要查看或回退的是哪一次。

### `report`

用于输出当前最常用的简要结果。

默认显示最近 5 条记录。

它会优先输出当前或最近一次保护会话的核心状态，包括会话 ID、会话状态、备注、仓库、排除文件、保护路径、PRE 快照、POST 快照、最近几次记录，以及最近几次会话。这样更适合在任务结束后直接贴给用户看。

### `rollback-help`

用于输出这次会话常见的回退建议。

它会给出几类典型命令。

- 用 `git diff <pre_sha>..<post_sha> --pathspec-from-file=<paths_file> --pathspec-file-nul` 查看本次保护路径范围内的改动
- 用 `git revert <post_sha>` 做保留历史的撤销
- 用 `git restore --source=<pre_sha> --staged --worktree --pathspec-from-file=<paths_file> --pathspec-file-nul` 按路径恢复到修改前
- 用 `git reflog -n 10` 查看更多可恢复位置

它本身不会直接执行回退，只负责把信息明确告诉用户。

## 行为边界

这个 skill 的边界也很清楚。

它依赖的是**当前目录所属的本地 Git 仓库**。如果目录原本不在 Git 仓库里，它会在当前目录初始化一个本地仓库。它不会把这个 skill 扩展成远端同步、协作流转或历史整理工具。

默认情况下，它不会主动进行远端同步，也不会改写历史。它做的是本地安全快照和回退提示，而不是替代团队的完整 Git 工作流。

## 需要提前知道的行为

这版虽然已经从“整仓库快照”收缩成了“目标路径快照”，但仍有两个边界需要知道。

第一，如果任务开始前目标路径里本来就已经有未提交改动，那么 `pre` 会把这些现有改动一起保存到 PRE 快照里。

这意味着 PRE 快照未必只包含“本次任务”新增的内容，也可能包含任务开始前就已经存在、但尚未提交的目标路径内本地修改。

第二，未被 `.gitignore` 和 `guarded-edit.ignore` 忽略的新增文件、生成物、二进制文件，甚至误放进目标路径内的敏感文件，也可能一起进入快照。因此在生成目录或产物目录被显式列为目标路径时，最好先确认 `.gitignore` 和 `guarded-edit.ignore` 是否合理。

## 建议的用户回报格式

任务完成后，建议按下面这种方式告诉用户结果。

```text
已完成本次修改，并已创建本地 git 保护记录。

会话: <session_id> (<session_status>)
会话备注: <session_comment>
仓库: <repo_root>
排除文件: <active_guard_ignore_or_empty>
保护路径:
- <path1>
- <path2>
PRE 快照: <pre_sha_or_summary>
POST 快照: <post_sha_or_summary>

当前目标路径最近 5 次记录:
<recent output>

最近 5 次会话:
<sessions output>

支持回退。
如需查看本次保护路径范围内的差异，可用:
  git diff <pre_sha>..<post_sha> --pathspec-from-file=<paths_file> --pathspec-file-nul
如需保留历史并撤销 post 提交，可用:
  git revert <post_sha>
如需按路径恢复到本次修改前，可用:
  git restore --source=<pre_sha> --staged --worktree --pathspec-from-file=<paths_file> --pathspec-file-nul
如需查看更多恢复点，可用:
  git reflog -n 10
```

## 文件结构

```text
file-change-tracker/
├── SKILL.md
├── README.md
└── scripts/
    └── helper.sh
```
