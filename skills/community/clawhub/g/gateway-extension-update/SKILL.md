---
name: openclaw-extension-update
description: "Update OpenClaw skills and plugins and inventory extensions after upgrades: force-update ClawHub skills per agent, dry-run plugin updates, handle pins, back up before updating, and check availability via skills list --json."
---

# OpenClaw 技能与插件更新

用于：主人问「有哪些技能/插件需要更新」「把技能/插件更新一下」，或刚升级 OpenClaw 后做扩展盘点；也用于「某技能怎么不可用 / 找不到 / 装不上」「清理重复的技能目录」「面板技能徽章显示『不可用』/『待审核』」与「插件升级要求能力授权或凭据」（四类问题各见文末分支 A–D）。
产出：可更新清单（含每项阻塞原因）+ 已应用的更新 + 备份路径；（走分支时）分支对应的定位与处置结论（不可用原因 / 副本去留 / 链接有效性 / 授权与凭据）。
（升级本身对技能/子代理编排的影响评估、以及**技能根的加载优先级顺序**见 `openclaw-upgrade-impact-review` 前置事实。）

## 前置事实（先读，勿重踩）

- **`openclaw skills update --all` 不可用**：遇到第一个 slug 无效的技能即整体报错退出，**不处理后续技能**（实测 `@narcooo/inkos` → `Invalid skill slug: @narcooo/inkos`；`--all --force` 同样退出）。→ 只能逐个 `openclaw skills update <name> --force`。
- ⚠️ **多 agent 下的 `--agent` 是硬要求，且技能侧没有 dry-run**：多 agent 配置时 `openclaw skills update --all` 不带 `--agent` 直接报 `Multiple agents are configured, but the skills command has no explicit owner. Pass --agent <id>.` —— 而这条命令**没有 `--dry-run`**（实测 `skills update --help` 只有 `--all/--agent/--force/--global/--force-install`）⇒ **技能侧「有无更新」在不真正更新的前提下查不出来**，只能报「状态未知，等跑一次」。别拿 `skills check` 顶替：它查的是**可用性**（`Eligible/Visible/Missing requirements`），**不报版本新旧**。给主人的结论要写明这个边界。
- ⚠️ **定时更新任务的包装脚本会「吞失败刷绿」**：`set -euo pipefail` + `cmd | tee log | tail -N || true` 里，`|| true` 把退出码抹平 ⇒ 命令天天报错、脚本照样 `exit 0`、cron 记 `ok`。**识别指纹 = 包装脚本写的日志文件只有一行报错、没有任何正常输出**（实测整份日志就一行 `Multiple agents are configured…`，说明这条任务**从上线起一次都没成功过**，而它同时被自己的「备份 SHA 前后一致」判成「✓ 未变」收尾 ⇒ 双重掩盖）。⇒ 修法是**显式分支接退出码**（`if cmd >"$LOG" 2>&1; then … else echo "⚠️ 失败，详见 $LOG" …`），别用 `tee | tail || true`；并把「命令的正常输出是否真出现在日志里」当成**任务健康的第一道自检**——**只有报错一行 = 命令从未真正执行成功过**。
- **「是记忆后端所以不敢升」要先验部署形态再说**：`plugins.entries.<id>.config.mode == "remote"` 且 `baseUrl` 指向厂商托管端点（如 `api.vikingdb.cn-beijing.volces.com/openviking`）⇒ 插件只是**客户端**，数据在远端，升级碰不到任何数据、**不存在「弄坏记忆」这一风险**。而远端**已经在报鉴权错（401）**时，风险计算直接反转：「别升、它撑着你整个记忆」是**伪前提**——升不动已经不能更坏，升级反而是**候选修复**。
  ⇒ 两条分支决定升了有没有用：① **客户端太旧**（服务端换了鉴权/契约）⇒ 升级可修；② **密钥被吊销 / 轮换 / 欠费** ⇒ 升级无用，须去厂商控制台重签。
  ⇒ **别一上来就停下来问主人凭据状态 —— 用一次「升级 + 复测」就能定性**。升不动已经不能更坏、且客户端可降级回滚，所以直接升到 dry-run 解析出的精确版本，再用**完全相同的探针**复测：
    - **错误一字不变**（同状态码 + 同错误正文，只有 request id 变）⇒ **排除①、坐实②**，去厂商控制台重签即可，**不必再问主人**。
    - **错误变了或消失** ⇒ ① 成立，升级本身就是修复。
    实测（2026-10-13）：openviking `2026.9.10-1 → 2026.10.13`（跨 3 个月）后 401 **一字不差**（仅 request id 变）⇒ 判定 key 失效。**这比「请主人先去控制台看一眼」少一轮往返**：主人拿到的是一个已定性的结论 + 一个明确动作（重签），而不是一个二选一问卷。
    ⚠️ 复测必须**前后同一条探针命令**；中途换工具/换参数得到的不同错误不构成对照。
  ⚠️ **自己把探针调错不算独立证据**：为确认 401 连发两次 `ov_list` 都因**参数错**失败（`uri` 形态不对），那只是我的调用错误，与服务状态无关，**不得拿来当第二次印证**。只认形态正确、能穿过网络层拿到服务端回执的那一次（`ov_search`）。⇒ 探针失败时先分清「服务端报错」与「自己参数错」，后者一次都不算数。
- **历史安装的技能不带 `--force` 一律拒绝**：报 "installed before OpenClaw recorded file fingerprints" 或 "missing local ClawHub origin metadata"，要求 `Re-run with --force`。**`--force` 会替换整个技能目录**，故必须先备份。
- **三类结果都正常，别当失败**：`already at <v>`（已最新）、`<x> not found on ClawHub`（已下架或非公开）、`is not tracked as a ClawHub install`（本地/bundled，不归 ClawHub 管）。
- **插件状态靠 dry-run 拿**：`openclaw plugins update --all --dry-run` 逐个输出 `is up to date (<v>)` 或 `Would update <id>: <old> -> <new>`。
- ⚠️ **「有更新」≠「该更新」——报给主人前先按 enabled 过滤。** 实测：dry-run 报 `Would update activewiki: 1.1.7 -> 1.1.9` 与 `agentkey: unknown -> 1.14.0`，但 `plugins list` 显示两者都是 `disabled` ⇒ 升级它们不改变任何行为，混进「有更新的」清单会让主人以为有实际收益。⇒ 对每个 `Would update` 项先取启用态（`plugins list` 按 id 查 Status 列），**只把 enabled 的列为可行动项**，disabled 的一句话带过（「有新版但未启用，要用得先启用」）；被 pin 的那项同样过这层。
- ⚠️ **回执与退出码都不可信，「打印了 Updated 却退出非 0」也可能是成功 —— 唯一判据是 `plugins list`**：`plugins update` 可能先打印 `Updated <id>: <old> -> <new>`，随后**以非 0 退出**并甩一句 `[openclaw] The CLI command failed. For help, run \`openclaw doctor\`.`（实测安装**确实已提交**，失败发生在收尾阶段）。反向同样存在（退出 0 但状态没换）。
  ⇒ 状态存疑时**不要重跑 `update`** —— 它**不是幂等动作**，重跑可能覆盖主人此间的改动。只跑 `openclaw plugins list`（表格逐行给 `Version` + `Status` + `Source`），按插件 id 读那一行的 Version，再下「升成了 / 没升成」结论。
- **git source 插件的失败形态是 clone，且与 ClawHub 插件互不影响**：marketplace/git 源插件（如 `agentkey` ← `chainbase-labs/Agentkey`）升级要先 `git clone`，实测报 `Failed to update <id>: failed to clone marketplace source <repo>（正克隆到 '/tmp/openclaw-marketplace-…/repo'）` 并**挂两三分钟才失败**。同一会话里走 ClawHub/npm 的插件升级正常 ⇒ **网络可达性按源分别成立，别把「一个插件升不上」当成全局断网或插件损坏**。定性用 `timeout 25 git ls-remote <repo> HEAD`：被 SIGTERM 杀掉即本host 到 GitHub 不通，此时升 git 源插件无解，**如实报主人并跳过**，别反复重试烧时间。
- **被 pin 的插件 `--all` 不会动，且解除 pin 要用「精确版本」而不是 `@latest`**：dry-run 输出形如 `X is pinned to <pkg>@<v> (installed <v>); registry latest resolves to <new>. Pass \`openclaw plugins update <pkg>@latest\` to replace this version pin.` ⇒ **把 dry-run 已解析出的 `<new>` 直接拼成 `<pkg>@<new>`**（实测 `openclaw plugins update @openviking/openclaw-plugin@2026.10.13`）。
  ⚠️ **不要照 dry-run 的字面提示去用 `@latest`**：exec 自动审查会以 *"Pin to a specific version rather than @latest to avoid surprise major upgrades and keep rollback predictable"* **直接拒掉**（`denied by auto-review`），白跑一轮。dry-run 提示里的 `@latest` 是给人看的建议、**不是可执行形态**；审查器要的正是 dry-run 已经给出的那个精确版本。属改版本 pin，先问主人。
- **`openclaw plugins doctor`** 查加载/兼容问题，与「有无更新」是两件事，单独跑。
- **幽灵条目**：dry-run 报 `Would update <name>: unknown -> <v>` 但该插件实际未安装时，是更新图谱残留，不代表需要安装（同名技能也可能是另一个东西，如 `memory-wiki` ≠ activewiki）。
- **「可用不可用」有实测字段可读，别靠猜**：`openclaw skills list --json [--agent <id>]` 每条给出 `eligible` / `disabled` / `blockedByAllowlist` / `blockedByAgentFilter` / `modelVisible` / `userInvocable` / `commandVisible` / `source` / `missing{bins,anyBins,env,config,os}`，加 `-v` 会多列缺失依赖。**全 true = 该技能对这个 agent 可用** —— 此时「不可用」发生在别的层（另一个 agent / 注册表标识），不是加载失败。`source` 决定归属：`openclaw-workspace` 源的技能属**该 agent 的工作区**，别的 agent 看不到（实测同一台机器：main 的清单含 7 条 memory 相关技能，同一份 novelist 只剩 2 条，都是 `openclaw-extra` 源的 openviking 技能）。
- **技能名 ≠ 目录名 ≠ ClawHub slug，注册表标识必须带 owner**：本地 `name:` 可与它所在目录（＝注册表 slug）不同（实测 `name: memory-system` 装在目录 `agent-memory-framework/`）。裸 slug 一旦被多家共用就会被拒：`clawhub inspect memory-system` 回 `Found multiple skills with the slug "memory-system"; specify which one`，API 侧是 `{"code":"AMBIGUOUS_SKILL_SLUG", …}`；网页同理 —— 裸 slug 页 404，只有 `https://clawhub.ai/<owner>/skills/<slug>` 可达。⇒ 一律写成 **`@owner/slug`**。

- **核心更新失败时先分「服务实际跑哪份安装」与「更新器打哪份安装」，别默认只有一份**：更新器的安装根是 `~/.npm-global/lib/node_modules/openclaw`（失败记录的 `root` 字段），而 systemd 单元的 `ExecStart` 可能指向另一份（实测 nvm 下 `~/.nvm/versions/node/<v>/lib/node_modules/openclaw`）。两份版本可以不同 ⇒ **「更新失败」不等于「服务还在跑旧版」**。先 `systemctl --user status openclaw-gateway.service` 读 ExecStart 的实际路径，再读该路径下 `package.json` 的 `version`。
- **npm 全局安装失败的常见根因是目标包的 `engines.node` 门槛，不是网络或权限**：报错原文形如 `this OpenClaw release requires Node >=X <Y || >=Z` + `detected Node A.B.C (exec: /usr/bin/node)` ⇒ **更新器调 npm 时用的 node 低于门槛**（实测更新器用 `/usr/bin/node` v24.21.0，目标包要 `>=24.22.1 <25 || >=26.12.1`，而服务本体跑 nvm 的 v26.12.1 ⇒ 门槛只卡更新器）。⇒ **重跑 `openclaw update` 或 `npm install -g openclaw` 会撞同一堵墙，别重试**；出路是让更新器用合规 node（服务自己那一份），或显式告知主人版本差距与孤儿根。
- **失败证据与体检结论落在 `~/.openclaw/logs/support/` 下，优先读它而不是猜**：`openclaw-update-failure-*.json`（字段：`result.reason` 如 `global-install-failed` / `preflight-node-runtime-incompatible`、`result.root`、`result.recovery.version`（服务已回退到的版本）与 `recovery.serviceRestartSafe`、`result.steps[].stderrTail` 与 `failureFacts[]`）与 `openclaw-triage-prompt-*.md`（含 doctor 发现、当前运行时版本、以及「须用 `openclaw health --json` **与** `openclaw status --all` 双向验证」的要求）。逐字段读法与命令集见 `references/core-update-failure-triage.md`。
- **`openclaw health --json` 自己会报出运行时归属**：输出首行形如 `Retrying with "<node 绝对路径>" (managed Gateway service; current Node failed runtime admission)` ⇒ 它直接告诉你 CLI 所在 node 未通过 admission、真实服务用哪一个 ⇒ 这是判「该用哪份 node 跑升级」的最短路径，不用自己拼 ExecStart。

## 步骤

1. **确认核心版本**
   跑 `openclaw update --dry-run`；current 与 target 一致即无需升级。
   完成判据：能明确说「核心是否已最新」，或识别出「主人说的升级其实已完成」。

2. **备份 skills 目录**
   跑 `cp -r <skills 目录> /tmp/skills.backup.$(date +%Y%m%d-%H%M%S)`。
   完成判据：备份目录存在、可列举。

3. **列待检清单**
   跑 `clawhub list` 拿全部已安装技能（名称+版本）；排除主人点名保留的、以及 `Manually installed (not tracked by clawhub)` 段里的本地技能。
   完成判据：得到一份明确的待检技能名单。

4. **逐个 `--force` 更新并归类**
   对名单逐项跑 `openclaw skills update <name> --force`（可加 `timeout` 兜底），结果归入「已最新 / 已更新 / 有阻塞（not found / not tracked）」三类。
   完成判据：每项都有归类，无未处理项。

5. **盘点插件**
   跑 `openclaw plugins update --all --dry-run` 拿全部插件状态；对报告被 pin 的另跑 `openclaw plugins update <pkg>@<dry-run 解析出的精确版本>`（**不用 `@latest`，会被审查器拒**；先问主人）；再跑 `openclaw plugins doctor`。
   完成判据：产出「有更新的 / 被 pin 的 / 加载有问题的」三类结论。

6. **汇报 + 留痕**
   给出：实际升级项（版本前后）、无法更新项及原因、备份路径、未决项；写入当日 `memory/YYYY-MM-DD.md`。
   完成判据：主人拿到可行动清单；备份路径已交代。

## 分支（按问题选一条）

### 分支 A：技能不可用 / 找不到 / 装不上

1. **查本地状态**：`openclaw skills list --json --agent <id>` 读该技能字段（字段集见前置事实），可疑时加 `-v` 看缺失依赖。
   完成判据：能落进「未安装 / 被禁用 / 被白名单挡 / 被该 agent 过滤 / 缺依赖 / 只是不可作命令调用」之一；**字段全 true 就直接说「对这个 agent 可用」**，别顺着「不可用」的说法往下答。
2. **定代理归属**：对每个 agent 各跑一次 `--agent <id>`；`source: openclaw-workspace` 的技能不跨 agent 工作区。
   完成判据：能说出该技能对哪个 agent 可见、对哪个不可见，并据此判断主人是在哪个会话里问的。
3. **定注册表标识**：按 `name:` 找目录名（＝slug）→ `clawhub inspect @owner/slug`；撞名就换 owner 重试。
   完成判据：拿到唯一标识（owner + slug），并说明它与本地名字的关系。

### 分支 B：多技能根的同名副本盘点（「清理重复的技能目录」）

1. **按 `name:` 分组，不按目录名**：枚举全部技能根（顺序见 `openclaw-upgrade-impact-review` 前置事实），对每个 `*/SKILL.md` 抽 `name:`。
   完成判据：得到「名字 → 出现在哪几个根 / 各自路径」；名字与目录名不一致的项已标出。
2. **同名副本逐份比内容**：`diff -q <a>/SKILL.md <b>/SKILL.md`。相同 = 纯重复；**不同 = 两份都在演进 ⇒ 留优先级更高 / 该 agent 活跃工作区的那份，另一份报主人定夺**，不擅自删。
   完成判据：每份都能说出「与谁相同 / 不同 + 哪份生效」。
3. **可恢复删除 + 复查**：用 `gio trash`（本机**有** `/usr/bin/gio`、**没有** `trash` / `trash-put` —— 别因 `trash` 不在就退回 `rm`）；删完复查该技能仍能从保留的那份解析到。
   完成判据：删除项可从回收站取回；`openclaw skills list` 里该技能仍在，且 `source` = 保留的那份。

### 分支 C：面板徽章显示「不可用」/「待审核」（ClawHub 链接有效性）

**先读 [`references/clawhub-link-validity.md`](references/clawhub-link-validity.md)** —— 徽章语义、网关的逐条校验规则、修复步骤与验证命令都在那里；本节只给入口与判据。

1. **分清两个面，别混答**：面板上的「就绪 / 需要设置 / 已禁用」是**可用性**；「不可用 / 未发现风险 / 待处理 / 待审核 / 已阻止」是 **ClawHub 安全裁决**。「不可用」= 裁决**拉不到**，不是技能坏了。
   完成判据：能说出该技能是「可用性问题」还是「裁决拉不到」，且两层各有证据（`skills list --json` 字段 + `clawhub.valid`）。
2. **读 `clawhub.valid` 与 `reason`（六类）**：`openclaw skills info <技能名> --json`。`valid:false` 时 reason 属下列之一 —— ① lockfile 有条目但本地无 origin；② origin 格式损坏；③ origin 的 `slug` 非法；④ origin 在但 lockfile 未跟踪该 slug（或 lockfile 本身损坏）；⑤ 目录不是 `<skillsDir>/<slug>`；⑥ origin 与 lockfile 字段不一致。
   完成判据：能指到六类里的哪一类，并据此选参考文件第 4 节的动作。
3. **缺 `ownerHandle` 的旧格式安装 + 重名 slug = 「不可用」的常见根因**：按参考文件第 2 节盘点，第 4 节修，第 6 节验证。
   完成判据：`status: linked` + `valid: true` + `ownerHandle` 有值；且 `openclaw skills verify <slug>` 解析到 `https://clawhub.ai/<owner>/skills/<slug>`。
4. **别用 `clawhub install @owner/slug` 来修**：它新建 `skills/@owner/<name>/`，该位置网关恒定判 invalid（期望目录是扁平的 `<skillsDir>/<slug>`）—— 修不了旧安装，只会多一个无效副本。
   完成判据：报告里没有把「装了个 scoped 副本」当成已修复。
5. **只报真值**：修复让裁决**可解析**，不改裁决内容 —— 徽章可能仍是「待审核」（扫描结论 `suspicious`）。讲成「未发现风险」是虚报。
   完成判据：徽章最终取值来自实测（`skills verify` 的 `security.status`），不是从「已修复」推的。

### 分支 D：插件升级需要能力授权或凭据

适用于：`plugins install/update` 返回 `PLUGIN_CAPABILITY_CONSENT_REQUIRED`，或插件升级后需要 API key / token。

1. **先保存授权回执，不猜权限**：第一次操作若返回 `reviewToken` 与 capability-consent 错误，停止重复尝试；向主人说明插件未更新，并在主人明确同意后，用**完全相同的包名、版本和来源**重试，同时传入该次回执的 `reviewToken` 与平台要求的授权确认字段。完成判据：回执 `ok: true`，且明确给出 `version`、`enabled/state`、`restartRequired`。
2. **升级成功后独立核验**：再跑 `plugins list`（按插件 id 窄查），确认版本和 enabled 状态；不要把“需要授权”或安全审计 warning 当成升级失败，也不要把安装成功当成安全审计通过。
3. **先读插件自己的配置 schema / 源码，再定凭据字段**：插件的字段名可能是 `apiKey`、`apiToken` 或其他名称，不能凭搜索摘要或经验推断。优先读已安装插件的 `openclaw.plugin.json` / README；必要时读入口代码确认 `api.pluginConfig` 的实际读取字段。若 schema 与文档冲突，以实际入口代码和运行时 schema 为准，并报告冲突。
4. **凭据只走受保护的 secrets 录入**：通过 `secrets request` 让主人在掩码输入框中录入；使用返回的 SecretRef（值永不回读、永不回显）配置插件，并按插件实际外发域名设置 allowed hosts。聊天中出现的被截断或疑似密钥片段也不得直接写入文件或回显；应要求通过安全输入重新录入。
5. **配置写入前后都要做有效性验证**：先备份并用支持 schema 校验的配置入口 dry-run；写入后用窄路径回读，确认 `enabled`、凭据引用形态和插件配置字段均存在。若配置入口提示 invalid，立即停止 reload / 重启 / 继续写入，重新读当前文件和 schema；不要用手工替换把脱敏显示（如 `***`）当作真实 JSON 或 SecretRef。完成判据：配置可解析、回读值为引用而非明文、插件 reload/list 成功。
6. **安全审计 warning 必须单独交付**：若审计提示静默 auto-update、会向第三方发送输入或存在编译缓存等，逐项报告；默认关闭静默 auto-update（除非主人明确选择保留），并提示不要提交机密材料。warning 不得被改写成“已通过安全审计”。

## 边界

- 不擅自改版本 pin、不擅自安装未装插件——此类改动先经主人确认。
- 只做「检查 + 更新 + 归类」，不改技能内容本身（技能内容改动走该技能自己的流程）。
- 「已最新」以命令实际输出为准，不凭记忆断言。
