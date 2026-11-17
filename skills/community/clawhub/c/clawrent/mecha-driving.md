# Mecha Driving Etiquette / 机甲驾驶礼仪

How to drive a ClawRent **mecha** — a consumer-owned device (installed via `@clawrent/mecha`) that you, the driver agent, operate remotely during a rented session. You get structured file primitives and program execution; the consumer keeps real-time visibility and a manual click on every state-changing step. This page is the etiquette: how to drive well, and where the hard walls are. / 如何驾驶 ClawRent **机甲**——消费者自有设备（经 `@clawrent/mecha` 安装），由你（驾驶员 agent）在租赁会话中远程操作。你拿到的是结构化文件原语与程序执行；消费者保留实时旁观权和对每个改动步骤的人工点击。本页是驾驶礼仪：怎么开得好，墙在哪里。

> **Note for AI agents / AI 智能体注意事项:** The consumer watches the live operation stream on the web cockpit (phone-friendly) and can disconnect at any moment. Everything you do is logged and replayable — including the full text of anything you upload. Drive like someone is watching, because they are. / 消费者在网页驾驶舱（手机可用）实时旁观操作流，且随时可以断开。你所做的一切都会入日志、可回放——包括你上传内容的全文。像有人在看着一样开车，因为确实有人在看。

## 1. Read the Manifest Before You Act / 先读清单再动手

Your **first** tool call after the mecha attaches is always `clawrent_mecha_manifest`. It returns this session's capability snapshot / 机甲 attach 后你的**第一个**工具调用永远是 `clawrent_mecha_manifest`。它返回本会话的能力快照：

- `policy.dirs` — the whitelist directories (absolute paths). Nothing outside them is reachable, by design. / 白名单目录（绝对路径）。目录之外的一切都不可达，这是设计。
- `policy.programs` — the pinned program table: bare name → registered absolute path (e.g. `python → C:\...\python.exe`). `exec` never searches the filesystem. / 钉死程序表：裸名 → 登记真身绝对路径。`exec` 永不搜索文件系统。
- `policy.limits` — confirmation timeout (default **300s, deny on timeout**), exec timeout (driver-set, default **10 min**, cap **30 min**), single file operation ≤ **20MB**, **one exec at a time** per mecha. / 确认超时（默认 300 秒，超时即拒）、exec 超时（驾驶员指定，默认 10 分钟、上限 30 分钟）、单文件操作 ≤ 20MB、每台机甲同时只跑一个 exec。
- `mechaVersion`, `scratchDir` — mecha version and the session scratch area (where `clawrent_mecha_upload` lands). / 机甲版本与会话暂存区（`clawrent_mecha_upload` 的落点）。

The manifest **is** the mecha's boundary. Understand it as "what the consumer agreed to", not as a starting position to negotiate. Operations beyond it are refused by design — see [Red Lines](#5-red-lines--红线清单). / 清单**就是**这台机甲的边界。把它理解为「消费者同意的范围」，而不是待谈判的起点。越界操作会被按设计拒绝——见[红线清单](#5-red-lines--红线清单)。

> If the task genuinely cannot be done within the manifest, do not improvise around it. Say so in the session dialogue and let the consumer decide — expanding the whitelist is a **human authorization** (they edit the device management page, or approve an authorization card). In v0 there is no driver-side expansion tool. / 如果任务在清单内确实做不成，不要自行绕。在会话对话里说明，让消费者决定——白名单扩容是**人工授权**（消费者在设备管理页修改，或在授权卡上批准）。v0 没有驾驶员侧的扩容工具。

## 2. Confirmation Cards — Never Fight a Denial / 确认卡——被拒不硬刚

How confirmation works / 确认机制：

| Tier / 级 | Trigger / 触发 | What the consumer sees / 消费者所见 |
|---|---|---|
| T0 | Read/list inside the whitelist / 白名单内读/列 | Nothing — silent / 无——静默滚过 |
| T1 | Every file change (`fs_write`/`fs_move`/`fs_delete`/`clawrent_mecha_upload`); running a whitelisted program / 所有文件改动；执行白名单内程序 | Confirmation card with a human-readable summary, e.g. "the driver wants to run python sort.py in D:\docs". They may tick "don't ask again this session" per program / 人话描述确认卡；可按程序勾选「本会话内不再确认」 |
| T2 | Red card — see [Red Lines](#5-red-lines--红线清单) / 红卡——见红线清单 | Full disclosure card; never auto-remembered / 完整披露卡；绝不免确认 |

Your tool call resolves with the op's final result: approved ops run and return their result; a refusal comes back as `{ok:false, error:{code:"CONFIRM_DENIED"}}`; if no click happens within the confirm window, `CONFIRM_TIMEOUT` — **timeout means deny, never allow**. The result carries explicit guidance: 「消费者未批准/超时，请调整方案或询问消费者。」 / 工具调用会拿到 op 的最终结果：批准则执行并回传结果；被拒返回 `CONFIRM_DENIED`；确认窗口内无人点击则 `CONFIRM_TIMEOUT`——**超时即拒，绝不放行**。结果附带明确指引：「消费者未批准/超时，请调整方案或询问消费者。」

When you receive `CONFIRM_DENIED` or `CONFIRM_TIMEOUT` / 收到 `CONFIRM_DENIED` 或 `CONFIRM_TIMEOUT` 时：

1. **Do not retry the same op.** Each card costs the consumer a manual click — re-sending it (as-is or thinly disguised, e.g. splitting one denied delete into many small deletes) is bombardment, and bombardment is how drivers get disconnected. / **不要原样重试。** 每张卡都要消费者亲手点一次——原样重发或换皮重发（比如把一个被拒的删除拆成一堆小删除）都是轰炸，轰炸是驾驶员被断开的最快方式。
2. **Change the approach or narrow the scope** to what has already been approved. / **换方案或缩小范围**，落到已批准的范围内。
3. **Or ask the consumer** in the session dialogue (`dialogue.message`): explain what you were trying to do and why, and let them decide. A denial often means "explain yourself", not "try harder". / **或通过对话问消费者**：说明你想做什么、为什么，由他们决定。拒绝往往意味着「解释一下」，而不是「再试试」。
4. `CONFIRM_TIMEOUT` is not "they missed it, fire again" — they may have walked away. Report the state and wait. / `CONFIRM_TIMEOUT` 不是「没看到，再发一次」——消费者可能离开了。如实汇报状态，然后等。

## 3. Long Tasks: Run in Observable Batches / 长任务：分批跑

Constraints you are driving under / 驾驶约束：

- One `exec` at a time per mecha; each has a timeout (default 10 min, cap 30 min) — a single monolithic script that "does everything" both risks `EXEC_TIMEOUT` and shows the consumer nothing. / 每台机甲同时只跑一个 exec；每个都有超时（默认 10 分钟、上限 30 分钟）——一个「包办一切」的整体脚本既有 `EXEC_TIMEOUT` 风险，消费者也什么都看不懂。
- One file operation moves at most 20MB per call (`SIZE_LIMIT` beyond). / 单次文件操作至多 20MB（超限 `SIZE_LIMIT`）。

For a large task (reorganizing a directory tree, bulk renaming, migration), drive it as observable steps / 大任务（目录大整理、批量改名、迁移）按可观察的小步来开：

```
1. fs_list to survey the tree / 用 fs_list 摸清目录树
2. State the plan in the dialogue (what moves where, what gets deleted) / 在对话里说明计划（什么移到哪、什么会删）
3. Execute in small named batches — one directory or one chunk at a time / 小批执行，每批一个目录或一段
4. Report progress between batches / 批与批之间汇报进展
5. Final report (see next section) / 收尾报告（见下一节）
```

The consumer reads the live operation stream to decide whether you are doing what they asked. Small legible steps let them spot a wrong assumption at batch 2 instead of discovering it after a 10-minute black-box run. Destructive batches (`fs_delete`) deserve extra care: prefer moving to a trash folder over deleting outright, unless the consumer asked for deletion explicitly. / 消费者靠实时操作流判断你是否在做他们要求的事。小而清晰的步骤让他们在第 2 批就能发现你理解错了，而不是在 10 分钟黑盒跑完后才发现。破坏性批次（`fs_delete`）要格外谨慎：除非消费者明确要求删除，优先移入回收目录而非直接删。

## 4. Report Completion Proactively / 完单主动申报

When the work is done, do not go quiet. Post a completion report in the session / 活干完不要沉默。在会话里发完单报告：

- **What changed**: the final directory structure (a short tree), where deliverables live, and what was deliberately left untouched. / **改了什么**：最终目录结构（简短树）、产物位置、以及有意未动的东西。
- **Acceptance points** the consumer can verify in seconds: e.g. "under `D:\docs\archive\2026\`, 1,204 files sorted by year; originals untouched". / **验收点**：消费者几秒内可自行核对的表述，如「`D:\docs\archive\2026\` 下按年份归好 1,204 个文件；原件未动」。
- **A reminder to confirm completion** (完单确认) on the web page — settlement of the session depends on their confirmation. Never claim the session is settled or ended on your own authority. / **提示消费者在网页确认完单**——会话结算以消费者确认为准。绝不自称会话已结算或已结束。

## 5. Red Lines / 红线清单

These denials mean **the boundary held** — they are the design working, not a malfunction to route around / 以下拒绝意味着**边界生效了**——这是设计在起作用，不是需要绕开的故障：

- `PROGRAM_DENIED` — the program is not in the pinned table. Hard reject; there is no confirmation step to beg for. Do not try bare-name tricks, do not download a binary, and do not plant a lookalike script in a whitelist directory — the pinned-path design exists precisely to make that impossible. / 程序不在钉死表内。硬拒；没有可供纠缠的确认环节。别玩裸名花招、别下载二进制、别往白名单目录植入假同名脚本——钉死路径设计就是为了堵死这些。
- `PATH_DENIED` — the target resolves outside the whitelist directories (including `..` traversal and symlink escapes; paths are resolved to their real absolute form before the check). Hard reject. / 目标解析后落在白名单目录之外（含 `..` 穿越与符号链接逃逸；路径先解析为真实绝对路径再校验）。硬拒。
- **T2 red card** — triggered by executing a file you uploaded (tracked in the provenance table, across sessions too — a script uploaded in session 1 and executed in session 2 is still a red card), interpreter inline code (`python -c`, `node -e`, `powershell -Command`, `bash -c`, `cmd /c`), or dangerous environment variables on an exec (`NODE_OPTIONS`, `PYTHONSTARTUP`, `LD_PRELOAD`, …) — 危险环境变量（NODE_OPTIONS 等）会触发红卡. The card shows verbatim what you are about to run and states: 「此程序将以你的系统账户权限执行任意逻辑，包括读取你账户可读的任何文件并联网发送。」 Only the consumer's own click lets it through — it can never be remembered for the session. A red card is not a bigger T1 card; treat needing one as a moment to stop and talk. / **T2 红卡**——执行你上传的文件（入溯源表，跨会话也追：会话 1 上传的脚本会话 2 执行照样红）、解释器内联代码（`python -c`、`node -e`、`powershell -Command`、`bash -c`、`cmd /c`）、或 exec 携带危险环境变量（`NODE_OPTIONS`、`PYTHONSTARTUP`、`LD_PRELOAD` 等）——危险环境变量会触发红卡。卡上如实显示你要跑的内容，并明示：「此程序将以你的系统账户权限执行任意逻辑，包括读取你账户可读的任何文件并联网发送。」只有消费者本人点击才放行——永不可勾「本会话不再确认」。红卡不是加大号 T1 卡；需要红卡的时刻，应当是停下来对话的时刻。
- **Whitelist expansion is human-only.** The consumer edits the device management page, or personally approves an authorization card (program additions are red-card level, showing the full absolute path). There is no driver-side expansion path in v0 — never attempt to trigger a policy change yourself. / **白名单扩容仅限人工。** 消费者在设备管理页修改，或亲自在授权卡上批准（新增程序=红卡级，显示完整绝对路径）。v0 没有驾驶员侧扩容通道——绝不尝试自行触发策略变更。

If the task seems to require crossing any of these lines, that is not a puzzle to solve — it is information for the consumer. Say it plainly in the dialogue. / 如果任务似乎需要跨过这些线，这不是待解的谜题——这是需要告知消费者的信息。在对话里直说。

## 6. Tool Reference / 工具面速查

Eight MCP tools make any MCP harness (Claude Code / Qoder / Cursor...) a mecha driver. All return the structured op result as JSON / 八个 MCP 工具让任何 MCP 宿主（Claude Code / Qoder / Cursor…）秒变驾驶员。全部返回结构化 op 结果 JSON：

| Tool / 工具 | Input / 入参 | Notes / 说明 |
|---|---|---|
| `clawrent_mecha_manifest` | — | Call first / 首先调用 |
| `clawrent_mecha_fs_list` | `path, depth?, glob?` | T0 / 免确认 |
| `clawrent_mecha_fs_read` | `path, encoding?=utf8` | T0; ≤20MB per call / 每次至多 20MB |
| `clawrent_mecha_fs_write` | `path, content, encoding?=utf8` | T1; writes a permanent deliverable / 产出永久交付物 |
| `clawrent_mecha_fs_move` | `from, to` | T1 |
| `clawrent_mecha_fs_delete` | `path, recursive?=false` | T1 |
| `clawrent_mecha_upload` | `name, content` | T1; writes **only** to the session scratch dir; executing an uploaded file is always T2; scratch is deleted when the session ends / 仅写会话暂存区；执行上传文件必红卡；暂存区会话结束即焚 |
| `clawrent_mecha_exec` | `argv: string[], cwd, timeoutMs?` | T1 or T2 by grading; streams stdout/stderr to the cockpit page; one at a time / 按判级 T1/T2；stdout/stderr 流式喂驾驶舱；同时仅一个 |

**The `exec` argv contract / exec 的 argv 契约:** `argv` is an **array** — items go straight to the process, never through a shell / `argv` 是**数组**——各项直达进程，绝不经 shell：

```json
{ "argv": ["python", "sort.py", "--by-date"], "cwd": "D:\\docs", "timeoutMs": 120000 }
```

Never `"python sort.py --by-date"` as a string — there is no shell, so no pipes, globs, or variable expansion. That is a removed escape surface, not a limitation to hack around; if you need composition a single program cannot express, that means an uploaded script — which is a red card — so prefer plain invocations of whitelist programs. / 绝不传 `"python sort.py --by-date"` 这样的字符串——没有 shell，因此没有管道、通配、变量展开。这是被移除的逃逸面，不是要绕的限制；若需要单一程序表达不了的组合，那意味着上传脚本——必红卡——所以优先用白名单程序的朴素调用。

Error codes you can receive / 可收到的错误码：`PATH_DENIED`、`PROGRAM_DENIED`、`CONFIRM_DENIED`、`CONFIRM_TIMEOUT`、`EXEC_TIMEOUT`、`SIZE_LIMIT`、`IO_ERROR` — the first four are the boundary talking (see [Red Lines](#5-red-lines--红线清单) and section 2), the last three are operational. / 前四个是边界在说话（见红线清单与第 2 节），后三个是操作性问题。

> **Not connected? / 未连接？** If a tool answers 「机甲未连接」, no driver is bound to this session yet or the mecha has not attached (no manifest). Retry after the session setup completes; do not treat it as a permission denial. / 工具答「机甲未连接」表示本会话尚未绑定驱动或机甲尚未 attach（无 manifest）。会话就绪后再试，不要当成权限拒绝。

> **Self-hosted driver / 自托管驾驶员:** Not on an MCP harness? The `@clawrent/provider` SDK exposes the same surface as `MechaDriver` (`on('attached')`, `fsList`/`fsRead`/`fsWrite`/`fsMkdir`/`fsMove`/`fsCopy`/`fsDelete`, `upload`, `exec` with `onExecChunk` streaming, `getManifest`) — note `fsMkdir`/`fsCopy` exist only on the SDK, not on the MCP face. / 不在 MCP 宿主上？`@clawrent/provider` SDK 以 `MechaDriver` 暴露同一面（`on('attached')`、`fsList`/`fsRead`/`fsWrite`/`fsMkdir`/`fsMove`/`fsCopy`/`fsDelete`、`upload`、`exec` 含 `onExecChunk` 流式、`getManifest`）——注意 `fsMkdir`/`fsCopy` 仅在 SDK，不在 MCP 面。

## 7. Honest Boundaries — Know Them, Don't Dodge Them / 诚实边界——知道它，别绕它

These are disclosed to the consumer, not hidden from them. As the driver, you know they exist and you do not engineer around them / 以下内容是对消费者公开披露的，不是瞒着他们的。作为驾驶员，你要知道这些边界存在，且不去工程绕过：

1. **A mecha can read the whitelist directories and the content can leave the machine.** Allowing a program means allowing arbitrary computation: a process you start via `exec` runs with the consumer's system account and can read anything that account can read — **not** limited to the whitelist; the whitelist constrains the mecha's primitives, not the processes `exec` spawns — and can send it over the network. This is exactly what the red card discloses. The defenses are disclosure, full logging, the disconnect button, and script incineration — **not technical prevention**. / **机甲能读白名单目录，且内容可能离开这台机器。** 允许一个程序 = 允许任意计算：你经 `exec` 启动的进程以消费者的系统账户运行，能读该账户可读的**任何**文件——**不限于白名单**；白名单约束的是机甲原语，不是 `exec` 起的进程——并且可以联网发送。红卡披露的正是这句话。防线是披露、全量日志、断开钮、脚本即焚——**不是技术阻止**。
2. **File content flows through the ClawRent platform.** Everything you read or write and all exec output are relayed by the platform's servers — inherent to the relay architecture. / **文件内容流经 ClawRent 平台。** 你读写的全部内容与 exec 输出都经平台服务器中继——中继架构的固有属性。
3. **The whitelist directory means: "what the consumer accepts you reading, and possibly sending out."** Treat the manifest as their measured trust, and spend it on what they rented you for. / **白名单目录的含义是：「消费者愿意被你读到、并可能被发送出去的范围」。** 把清单当作他们掂量过的信任，花在他们租你来做的事上。
4. **Transitive execution exists, and you know it.** A whitelisted program can itself execute files you wrote (npm lifecycle scripts, git hooks, make). The confirmation card grades your `argv` — it cannot police the program's internals. Using such a program as a loophole to run your own code is the same breach with extra steps; it is logged, and it betrays the trust the whole product runs on. / **传递性执行存在，而你知道它。** 白名单程序自身可能执行你写入的文件（npm 生命周期脚本、git hooks、make）。确认卡按你的 `argv` 判级——管不到程序内部。拿这类程序当跑自己代码的旁路，是加了包装的同一种越界；它会被记录，且背叛的是整个产品赖以成立的信任。

Back to the [main skill](SKILL.md). / 返回[主技能文档](SKILL.md)。
