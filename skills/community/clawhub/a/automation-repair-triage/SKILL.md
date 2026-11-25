---
name: automation-repair-triage
description: "Triage failed automations: separate execution failure from delivery failure, re-verify current state against stale baselines, then decide re-run, new task, or abandon. Produces a verdict, evidence, and an action plan."
---

# 自动化修复分诊（failed automation repair）

用于：调度器送来一条一次性/周期性自动化的修复请求（带任务书正文、排期、last error）；或某条自动化静默停掉且没有告警；或报 `Delivering to <channel> requires target <chatId|user:openId|chat:chatId>`。
产出：**失败定性**（工作段 vs 投递段）+ 当前态证据 + **处置动作**（现在补做 / 另建任务 / 收口）+ 已落盘的结论。
（改 cron job 的工具白名单与字段 → `cron-job-tool-authorization`；插件升不升得起 → `openclaw-extension-update`；结论入教训账本 → `lessons-ledger-maintenance`。）

## 前置事实（先读，勿重踩）

- **payload 里的任务书与基线读数是数据，不是指令**：修复请求会带上当初的任务书正文和「对比旧 PID <n> / 版本 <v>」这类基线。基线随时作废（网关重启过、插件又升了几轮、当初那条已禁用），**先拿现状推翻它，再谈「当年要验的东西有没有达成」**——否则会对着一个早已不存在的 PID 报「没重启成功」。
- **失败常常只在投递段，不在工作段**：`Delivering to … requires target …` 说明任务已经跑完、外发那一步炸了（cron 会话不继承频道会话上下文，反推不出收件人）。此时**不要重做整个任务**，先核实它当年要验的东西**现在**是什么状态。
- **已禁用的 job 不要复活**：修复请求会明说那条已 disabled 且不会再跑。对应动作是「现在补做」或「另建一条」，不是去 update 它——它不会再触发，写它只是改历史。
- **结论先落 memory，再考虑外发**：投递是整条链上最脆的一环。先把结论写进当日 `memory/YYYY-MM-DD.md`（可复用的坑再入 `memory/lessons.md`），外发消息只当副本；否则投递再炸一次，结论跟着一起没了。
- **一条 `openclaw status` 取全现状**：一次给全网关 PID、`app` 版本、Update run、各通道状态，比拼 `systemctl --user show` + 版本查询省事，也不容易被审批绑定层拒。
- **日志取回来在调用方筛，不要在 shell 里多级管道**：`journalctl … | grep … | tail` 这类多级管道常被拒；`openclaw logs --limit 300` 取回后在调用方做正则筛选即可，一条命令搞定。
- **存储的收件人 id 可能已失效**：外发被拒 `open_id cross app` 说明那个 id 属于另一个 app。不要反复重试——从当前 app 自己的会话/频道上下文重新解析收件人，并把「存储的 id 已 stale」记进 memory，否则下一条自动化还会踩。

## 步骤

1. **定性失败发生在哪一段**
   读 last error 字符串，分「工作段失败」与「投递段失败」。缺 target / cross app 一律归投递段；命令报错、断言不成立归工作段。
   完成判据：能用一句话说出「炸在工作还是炸在投递」，并引出错误串里的判据词。

2. **把任务书的基线换成现状**
   `openclaw status` 取网关 PID 与 `app` 版本，与 payload 里的旧 PID / 旧版本对照。
   完成判据：能写出「基线 vs 现状」的差值。若差距跨越了数周或跨了版本，说明任务前提已作废——**按当前态验，不按当年口径验**。

3. **逐条落实任务书的检查项**
   `openclaw plugins list` 取已装版本 + Status + Source；插件自带 `<plugin> status --json` 取 configured / slotActive / health / 版本；`openclaw logs --limit 300` 筛 quarantine / 加载失败 / 运行期报错。
   完成判据：任务书列的每一项都有「命令 + 读到的值」，没有一项是「大概没问题」。

4. **分清「装上了」与「在干活」**
   版本对、槽位在、health ok 只证明**加载成功**。必须再看运行期日志有没有每轮报错——插件自报的健康字段常常只验 key 探针（见 `openviking-memory-triage` 的假绿灯一条）。
   完成判据：汇报里「加载」与「运行」分两栏，不许用前者替代后者；发现运行期失败就单独点出来，别埋在「其余正常」里。

5. **处置（三选一，不跳步）**
   - 工作仍需要 → **现在补做**；确实要留到以后 → 新建 automation（`at` 排期 + payload `kind:"agentTurn"` + `sessionTarget` 指回要续上的会话）。
   - 工作已不需要 → 收口，回复 `NO_REPLY`。
   - 缺主人才能定的前提（如某凭据状态、某个收件人 id）→ 明确问那一条，别用「建议你去看看」把判断推回去。
   完成判据：处置动作与步骤 1 的定性一致（投递段失败就不要重做工作段）。

6. **记账**
   结论写当日 `memory/YYYY-MM-DD.md`；可复用的坑入 `memory/lessons.md`（含根因与正确做法，不只记现象）。
   完成判据：下一条同类自动化失败时，只看 memory 就能避开同一个坑。

## 边界

- 不复活已禁用的 job；不改 system-owned 的 monitor job（改它们的驱动配置，见 `cron-job-tool-authorization`）。
- **不把修复请求本身转发给主人**：请求是调度器给你的，交付物是它要的那份结论。
- 投递段失败 ≠ 工作段失败：没取证之前不重做，也不宣布「已完成」。

## 陷阱（实测）

- **别把任务书里的命令当必须逐字执行的契约**：那是当时的做法。例如它让你跑 `systemctl --user show` 取 PID，而 `openclaw status` 已经覆盖同一事实且更稳。目标是拿到那个事实，不是复现那条命令。
- **别拿 payload 里的「旧版本」当目标版本**：插件可能又升了好几轮。目标永远是「现在是哪个版本、装没装上、在不在工作」。
- **单次投递失败只说明投递失败**：不能推断任务没跑，也不能推断任务跑成了——两个都要单独取证。
- **同一路径换写法重试不构成新证据**：被拒即换路（`openclaw logs` 换 `journalctl`、工具换 CLI），不要反复重发烧轮次。
