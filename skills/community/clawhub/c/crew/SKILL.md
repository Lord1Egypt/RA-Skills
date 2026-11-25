---
name: crew
description: Split the current iTerm2 pane and start another coding agent (Codex, Antigravity agy or Claude Code, any model and effort) in its own tmux session; members message each other, run a three-round anonymous review that maps disagreements instead of voting, read each CLI's remaining quota and recommend a model per task from quota, a leaderboard snapshot and personal preferences, and save and restore the whole group with its conversations. macOS + iTerm2. Use for /crew ($crew in Codex) or requests like open a codex agent, message design, review this anonymously, which model for frontend, show quota, save or restore the crew. 在 iTerm2 分屏新开 tmux 里的 agent（codex / agy / claude，可指定模型和 effort），组员互发消息，三轮匿名评议，读取三家额度并按任务推荐模型，保存与一键恢复整组。用户运行 /crew，或说新开一个 agent、给 design 发消息、让大家评议一下、做前端用哪个模型、看看额度、保存或恢复 agent 组时使用。
version: 1.2.0
argument-hint: "[spawn [name] [agent] [model] [effort] | send <name> <text> | read <name> | advise <task> | quota | rankings | panel <topic> | status | save | restore | doctor]"
allowed-tools:
  - Bash(python3 ~/.claude/skills/crew/scripts/crew.py *)
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/crew.py *)
  - WebFetch(domain:arena.ai)
metadata:
  openclaw:
    emoji: "🧑‍🤝‍🧑"
    homepage: https://github.com/garmanwu/crew
    os: ["macos"]
    requires:
      bins: ["python3", "tmux"]
      anyBins: ["codex", "agy", "claude"]
    envVars:
      - name: CREW_NO_QUOTA
        required: false
        description: 设为 1 时关闭全部额度读取。
      - name: CODEX_HOME
        required: false
        description: Codex 数据目录（默认 ~/.codex），用于读会话 ID 和额度事件。
      - name: CLAUDE_CONFIG_DIR
        required: false
        description: Claude Code 配置目录，用于读 /usage 缓存。
      - name: XDG_CONFIG_HOME
        required: false
        description: 个人配置位置（默认 ~/.config/crew）。
      - name: XDG_CACHE_HOME
        required: false
        description: 额度缓存和探测目录位置（默认 ~/.cache/crew）。
---

# crew

> **English overview.** crew opens another agent CLI (Codex, Antigravity `agy`, Claude Code) in an iTerm2 split pane, each in its own tmux session, so you can watch and steer it live. Members message each other through tmux; the main session can run a three-round anonymous panel that produces a map of agreements and disagreements; `quota` and `advise` read each CLI's remaining quota locally and recommend a model for a task; `save` / `restore` bring the whole group back with its conversations. Requires macOS, iTerm2, tmux, python3 ≥ 3.8 and at least one of the three CLIs. The instructions below are in Chinese; follow them as written and **always reply to the user in the user's own language**. Script output is JSON with Chinese messages; translate when relaying. English README: `README.en.md`.

所有操作都通过一个脚本完成，输出是 JSON（`ok: false` 时看 `error`）：

```bash
CREW=<本 skill 所在目录>/scripts/crew.py   # 例如 ~/.claude/skills/crew/scripts/crew.py
python3 $CREW <子命令> ...
```

`CREW` 用本文件所在目录推出来（Claude Code 里可用 `${CLAUDE_SKILL_DIR}`；从 ClawHub 或其他位置安装时以实际目录为准）。

在项目目录里运行（脚本会向上查找 `.crew.json`）。需要 macOS、iTerm2、tmux、python3（3.8 起，系统自带的即可），以及至少一个 agent CLI。环境有问题先跑 `python3 $CREW doctor`。

这个 skill 在 Claude Code、Codex、agy 里都能用，三处是同一份文件（`~/.codex/skills/crew` 和 `~/.gemini/config/skills/crew` 是指向 `~/.claude/skills/crew` 的软链接），脚本路径统一用上面这个。

参数：`$ARGUMENTS`（Claude Code 会替换成用户输入；在 Codex、agy 里用本次请求中给出的子命令和参数）。为空时按 `spawn` 处理。

## 约定

- **组名** = 项目目录名（小写，非字母数字转成 `-`）。每个成员一个 tmux 会话，名为 `<组名>-<成员名>`，例如 `lego-design`。tmux 会话名是全局的，这个前缀用来避免不同项目的 `design` 撞在一起。
- **main** = 第一次执行 spawn 的那个会话，可以是 Claude Code、Codex 或 agy（脚本从进程链自动识别，`python3 $CREW whoami` 可查看识别结果）。它通常不在 tmux 里，这时组员给它发不了消息，由 main 用 `read` 去读组员的窗格。执行过 `restore` 之后 main 也进 tmux（`<组名>-main`），才能双向通讯。
- **状态文件**：`<项目>/.crew.json`，记录每个成员的 agent、模型、effort、会话 ID、分屏位置。

## spawn：新开一个 agent

1. `python3 $CREW models` 得到菜单：每个已安装 CLI 的前两个模型（按 CLI 自己的顺序，带可用 effort 和 `quota` 剩余额度）。没装的 CLI 不出现。
2. 用户在参数里已经给全（名称、agent、模型、effort）就直接到第 3 步。用户只说了任务（"开个做前端的"）就先跑 `advise`（见下文），把推荐和理由告诉用户，让用户确认或换。否则把菜单列成编号清单（带剩余额度），一次问清三件事：选哪个编号、agent 叫什么名字（如 `design`）、effort（默认 `high`）。让用户用一行回复，例如 `2 design high`。不要用 AskUserQuestion 做多选一（它最多 4 个选项）。剩余额度低于 20% 的选项要标出来。
3. 启动：

   ```bash
   python3 $CREW spawn --name design --agent codex --model gpt-6.2-astra --effort high \
     --main-model <你自己的模型 ID> --main-effort <你自己的 effort>
   ```

   - `--main-model`、`--main-effort` 填你（main）当前运行的模型 ID 和 effort，恢复时 main 用它们启动。Claude Code 的 effort 会自动读取，可以不填；agy 的模型填系列名（如 `gemini-4-neon`）；不确定自己的模型或 effort 就不填，恢复时用该 CLI 的默认值。组员调用 spawn 时不用填。
   - main 是 Codex 时必须以 full access 运行，否则沙箱会拦住 tmux 和 iTerm2 的分屏；恢复时 main 也按 full access 启动。
   - main 是 Codex 时还需要有一个已经在 iTerm2 里运行的 tmux（最简单是在 tmux 里启动 codex）：Codex 的命令由后台守护进程执行，macOS 不允许它直接控制 iTerm2，脚本会改由 tmux 代发分屏请求。
   - 名称只能用小写字母、数字、连字符。
   - 用户口头说的模型（如"astra 62"）对应到 `models` 输出里的 `model` 字段；对不上就问，不要猜一个相近的。
   - 默认分屏位置：第 1 个在 main 右侧，第 2 个在第 1 个下方，第 3 个在 main 下方，之后依次在已有 agent 右侧。要指定位置用 `--from <成员名> --split v|h`（v 左右分，h 上下分）。
   - codex 默认以 full access 启动（`-s danger-full-access -a never`）：执行命令不受沙箱限制，也不请求审批，范围是整台机器；这样它才能连上 tmux 主动给组员发消息。用户明确要求保留沙箱时加 `--sandbox`，此时 codex 不能主动发消息，只能被读取。
4. 脚本会等 agent 就绪、自动确认"信任此文件夹"对话框、给新 agent 发一条说明（组里有谁、怎么发消息），并记录会话 ID。看返回的 `status`：
   - `ready`：成功。告诉用户名称、模型、effort。返回里有 `quota_warning` 时一并转告。
   - `trust_prompt` / `timeout` / `exited`：用 `read` 看窗格里是什么，把情况告诉用户。

## send / read：通讯

```bash
python3 $CREW send --to design "请看一下 SPEC.md 第 3 节，给出修改建议"
python3 $CREW read --name design --lines 80
```

- `send` 会自动加上 `[from <发送者>]` 前缀，支持多行。
- 发完消息对方需要时间处理；用 `read` 查看结果。还在生成时过一会儿再读，不要连续快速轮询。
- 给不在 tmux 里的成员发消息会报错（常见于 main 尚未恢复过）。

## panel：匿名多轮评议

让组员对同一个议题各自表态、互相评议、再自行修正。目的是把分歧看清楚，不是求一致：不投票，不统计人数，少数派立场原样保留。main 默认只主持和汇总，不发表自己的观点（用户要求 main 参评时见下文 `--with-main`）。`panel start / next / reveal` 只有 main 能执行；你是组员时收到这类请求，转告用户到 main 的窗格里发起。

组里先要有参加评议的成员（用 spawn；跨厂商的组合分歧更有信息量）。然后：

```bash
python3 $CREW panel start --topic "要不要把版型数据库从 DXF 迁到自定义 JSON？背景见 SPEC.md"
python3 $CREW panel wait      # 阻塞到全部提交或超时（默认 540 秒）；超时就再跑一次
python3 $CREW panel next      # 匿名公开立场 -> 第 2 轮互评
python3 $CREW panel wait
python3 $CREW panel next      # 匿名公开评议 -> 第 3 轮修正
python3 $CREW panel wait
python3 $CREW panel next      # 匿名公开最终立场 -> 进入汇总
# main 读 board/，写 map.md
python3 $CREW panel reveal    # 揭晓代号对应的成员和模型
```

- 议题长就写成文件，用 `--topic-file`。`--members a,b,c` 只让部分成员参加（默认除 main 外全部）。`--id` 给评议起名（默认时间戳）；其余子命令默认操作最近一次评议。
- 三轮分别是：**独立立场**（互相不可见）、**互评**（对每份写最强反对意见和值得借鉴的点）、**修正**（开头写变更说明：因哪条论据改了什么，听了哪些反对仍坚持；不改也行，但要写理由）。脚本负责给每个成员发各轮的指令。
- 文件在 `<项目>/.crew/panel/<id>/`：`drafts/<成员名>/` 是成员写的原件，`board/<positions|reviews|final>/<代号>.md` 是匿名公开的副本，`panel.json` 里有代号对应表。
- **main 在 reveal 之前只读 `board/` 和 `topic.md`**，不要读 `drafts/`、`panel.json`，也不要用 `read` 看成员窗格里的正文（确认卡没卡住可以）。`reveal` 在 `map.md` 写好之前会拒绝执行。
- 有成员一直不提交：先 `read` 看它卡在哪。确定放弃才用 `panel next --force`，它会被移出后续轮次，已公开的内容保留。
- 等待时优先用 `panel wait`（可放后台运行），不要反复 `status`。
- **main 也参评**：用户要求 main 也表态时，必须在 `panel start` 时加 `--with-main`，不能中途加入。main 会和组员一起随机分到代号，每轮的任务在命令返回的 `main_task` 里（不会发到窗格），main 自己把文件写到 `drafts/main/`。此时 main 同样受盲写约束：第 1 轮写完自己的立场之前不读任何人的内容；全程不向组员透露自己参评、自己的代号或模型（组员只会看到多了一份匿名立场）。汇总时 map.md 里对自己那份和别人一视同仁，并在末尾注明“主持人同时参评，代号见对应表”，提醒用户留意这一利益冲突。
- **不要中途改规则**：评议开始后不再加人、不公布任何人的身份或模型。要改参评名单就让所有成员 `/clear`（`tmux send-keys -t <组名>-<成员名> /clear Enter`），把旧评议目录移到 `.crew/archive/`，再重新 `panel start`。

### 汇总：写 map.md

三轮结束后读 `board/` 下全部文件，写 `<评议目录>/map.md`。全程用代号，不加入 main 自己的立场，不评选赢家：

1. **共识**：最终立场里各方都认同的判断。
2. **分歧**：每条写明症结（双方到底在哪个前提或事实上不一致）、各方代号和最强论据、什么证据或实验能解决它。
3. **少数派立场**：只有一两方坚持的观点，连同其最强论据原样保留，不因人少而弱化或省略。
4. **立场变化**：谁因为哪条论据改了什么；谁听了反对仍然坚持。
5. **核心问题**：把以上压缩成最需要用户决定或验证的 1 到 3 个问题。

写完运行 `panel reveal`，把代号对应表附在 map.md 末尾，再向用户报告核心问题和 map.md 的路径。

### 限制

- 盲写和匿名靠指令约束，不是强制隔离：成员在同一台机器上，技术上能读到别人的草稿和代号表；文风也可能暴露身份。
- 固定三轮。想对某个分歧再深入，就以那条分歧为议题新开一次评议。

## advise / quota：按任务和额度选模型

```bash
python3 $CREW advise --task frontend        # 推荐 + 候选清单和理由
python3 $CREW quota                         # 三家剩余额度（10 分钟缓存，--refresh 强制重读）
```

- 任务类型在 `defaults.json` 的 `tasks` 里（frontend、coding、agentic、review、writing、vision、research、3d、labeling），每个对应排行榜的若干分类。用户说的任务对不上就选最接近的，并说明选了哪个。
- 规则（返回的 `rule` 字段）：剩余额度 ≥ `min_quota`（默认 20%）且与最高分相差 ≤ `elo_margin`（默认 50，约等于 57% 胜率）的候选里，选单次成本最低的；用户偏好（`prefer`）排在最前；额度不足的仍列出但排最后。没有排行分类的任务（如 3d、labeling）只按偏好和额度排序。
- 汇报时给出推荐、它的 `why`，以及一两个备选；不要只报模型名。
- 默认只在菜单（每个 CLI 前两个）里选，`--all` 考虑全部模型。
- 额度读不到时显示为未知，不阻止 spawn。

### 个人偏好：`~/.config/crew/roles.json`

用户说"X 适合做 Y""以后 Y 都用 X""别给组员用 Z"时，写进这个文件（没有就新建），不要改 skill 目录里的 `defaults.json`：

```json
{
  "tasks": {
    "3d":       {"prefer": ["gpt-6.2-astra"]},
    "frontend": {"prefer": ["gemini-4-neon", "gemini-4-carbon"]},
    "slides":   {"label": "做幻灯片", "arena": ["webdev"], "prefer": []}
  },
  "policy": {"min_quota": 20, "elo_margin": 50, "avoid_for_members": []},
  "claude_models": [["fable", "Claude Fable（最新）"], ["opus", "Claude Opus（最新）"]]
}
```

`tasks` 可以覆盖已有任务，也可以新增；`prefer` 和 `avoid` 按模型名的子串匹配。`claude_models` 替换 Claude 的菜单（别名始终指向该系列最新版本）。

### 排行榜：`~/.config/crew/rankings.json`

`python3 $CREW rankings` 查看状态；`rankings show [分类键]` 列出快照里的排名（`in_menu` 标出菜单里对应的模型），用户要看排行榜时用它，并注明抓取日期。返回 `stale: true`（没有，或超过 30 天）时，如果用户在让你挑模型，先更新：

1. 用你的网页读取工具打开 https://arena.ai/leaderboard 及需要的分类页。脚本自己不联网（该站会拒绝脚本请求）。
2. 按返回的 `schema` 写一个 JSON：`fetched` 填今天日期，`categories` 的键用下表，每个分类至少记录前几名和菜单里各模型的 `name`（照抄页面上的名字，含括号里的 effort）、`rank`、`score`，页面给了单次成本就填 `cost`（美元）。页面没有的不要编。
   | 页面上的名称 | 键 |
   |---|---|
   | Agent Arena Index / Work / Coding / Chat / Task Outcome / Steering / Tool Use Index | agent / work / coding / chat / task-outcome / steering / tool-use |
   | Text / Vision / Document / Search | text / vision / document / search |
   | WebDev / Image-to-WebDev | webdev / image-to-webdev |
3. `python3 $CREW rankings import <文件>`，格式不对会报出哪一项。
4. 读不到页面就跳过，`advise` 会只按额度和偏好推荐，并告诉用户排行数据缺失或过期。

## doctor

`python3 $CREW doctor`：检查 macOS、python3、tmux、iTerm2、各 CLI 及其模型列表、三家额度能否读到、排行榜和个人配置。CLI 升级后行为不对时先跑它，把结果给用户（或贴到 issue）。

## 权限与隐私

- **Codex 组员默认 full access**（`-s danger-full-access -a never`）：不受沙箱限制、不请求审批，范围是整台机器。这是组员能通过 tmux 主动发消息的前提；不需要时用 `--sandbox`。第一次给用户开 Codex 组员时说明这一点。
- **额度只在本机读取**，不联网、不上传：
  - Codex：读 `~/.codex/sessions/` 下最近的会话记录里的 `rate_limits` 事件；
  - Claude Code：读 `~/.claude.json` 里 `/usage` 的缓存（只用 `cachedUsageUtilization` 和账户 ID 做匹配）；缓存超过 10 分钟时，在隐藏终端里启动一次 `claude -- /usage`（关闭 hooks、MCP 和工具，不发送对话）刷新；
  - agy：在隐藏终端里启动一次 `agy`，用 `--settings` 临时注入状态栏命令（指向本 skill 的 `advise.py`），读取它交给状态栏的额度数据，不发送对话；
  - 两个探测都在 crew 自己的空目录 `~/.cache/crew/probe` 里运行，首次会自动确认"信任此文件夹"。
  - `CREW_NO_QUOTA=1` 关闭以上全部读取。
- **排行数据**只由 main 用自己的网页工具读取，脚本不联网。
- 写入的文件：项目内 `.crew.json`、`.crew/`、`<组名>-crew.command`；用户目录 `~/.config/crew/`（偏好、排行）和 `~/.cache/crew/`（额度缓存）。
- Claude Code 里，frontmatter 的 `allowed-tools` 让本 skill 的脚本命令和读取 arena.ai 不必逐次确认；Codex、agy 按各自的权限设置处理。


## status

`python3 $CREW status`：每个成员是否在 tmux 里、所在 tty、已保存的会话 ID 和当前实际的会话 ID。

## save：保存整组

```bash
python3 $CREW save --main-model <你自己的模型 ID> --main-effort <你自己的 effort>
```

- 重新读取每个窗格当前的会话 ID（成员执行过 `/clear` 或新开对话后 ID 会变），更新 `.crew.json`。
- 在项目目录生成 `<组名>-crew.command`，双击即可恢复。
- 把返回的 `updated`（ID 有变化的成员）和 `missing_session_id`（没有会话 ID、恢复时会开新对话的成员）告诉用户。

## restore：恢复

用户双击 `<组名>-crew.command`，或运行 `python3 $CREW restore --dir <项目目录>`。

- 该组窗口已经开着：切换过去。
- 否则新开一个 iTerm2 窗口，main 在 `<组名>-main` 里按会话 ID 恢复，其余成员按保存的分屏顺序依次恢复，各自带上原来的模型和 effort。
- tmux 会话还活着（只是窗口关了）时直接接回去，不会重启 agent。
- **main 的原窗口还开着时会拒绝恢复**：同一个对话不能被两个进程同时写。所以不要在 main 自己的会话里替用户执行 restore；告诉用户先退出当前这个窗口，再双击 `.command`。

## 已知限制

- 只恢复分屏结构，不恢复窗格的精确尺寸。
- 成员刚 `/clear` 还没说过话就保存，记录的是一个空对话的 ID，恢复时可能找不到对话；让它先回一句话再保存。
- Codex（0.171 起）的命令由后台守护进程执行，脚本靠 `CODEX_THREAD_ID` 和启动时注入的 `CREW_MEMBER` 标记识别调用方。Codex 组员执行 `/clear` 后，新的会话 ID 要等它下一次用 `send` 发消息时才会记录；保存前让它给任意组员发一条消息。
- main 是 Codex 且不在 tmux 里时，它的窗口是按工作目录和启动时间推断的；同一目录开着多个不属于本组的 Codex 窗口时可能分屏到错的窗口，用 `whoami` 核对 `tty`。
- 一个组只有一个 main。脚本从当前目录向上找最近的 `.crew.json`，所以在已有组的目录或其子目录里，另一个不属于该组的会话会被识别为 `guest`（`whoami` 可见）：它不能 `spawn`、`save` 或主持 panel。要在子目录另建一个独立的组，用 `spawn --here`。
- 没有"移除成员"命令：关闭某个 agent 用 `tmux kill-session -t <组名>-<成员名>`，再手动把它从 `.crew.json` 的 `members` 里删掉。
