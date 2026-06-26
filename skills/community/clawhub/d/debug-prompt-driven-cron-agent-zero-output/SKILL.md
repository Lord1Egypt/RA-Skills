---
name: "debug-prompt-driven-cron-agent-zero-output"
description: "用于排查“定时任务成功执行但结果全为 0 / 未检索到样本 / 明明有数据却日报为空”这类问题，尤其适合 Discord、Obsidian、cron、agentTurn、prompt 驱动任务、日整理、复盘脚本、采样漏扫、thread starter 漏计、主频道消息未纳入、Snowflake 字符串比较、时区时间窗边界等场景。只要用户提到“任务跑通了但产物为空”“怀疑不是分类错而是采样漏了”“想确认 prompt job 是否没有固定源码”“想定位检索链路断点”，就应触发此技能。"
metadata: { "openclaw": { "emoji": "🧭" } }
---

# 排查纯 Prompt 驱动定时任务为何产出全 0

这个技能帮助你把“任务执行成功但结果为空”的问题快速定位到实现入口、采样链路和高风险断点，从而区分是检索漏扫还是后续分类清零。

## When to use this skill

- 当你需要判断一个 cron / agent 任务为什么“跑成功了，但日报、复盘、统计结果全为 0”，并且怀疑问题出在上游检索而不是下游分类。
- 当你面对的是自然语言 prompt 驱动的任务，想确认它是否其实没有固定脚本实现、导致采样方式由模型临场决定。
- 当用户提到 Discord 线程、主频道消息、thread starter、mention、reply、Snowflake、Asia/Shanghai 昨日时间窗等关键词，并想排查样本是否被漏掉。
- 当你需要给出“有证据的根因判断 + 明确边界 + 最小修复建议”，而不是只做泛泛猜测。

## Steps

1. **先定位任务的真实实现入口**
   - 打开 cron 配置文件，确认 job 的定义位置与执行类型：
     - `/Users/can4hou6joeng4/.openclaw/cron/jobs.json`
   - 在目标案例中确认到的关键字段是：
     - `id: "c6e92d09-5ff6-4079-b839-a9c4fe6d2e10"`
     - `name: "obsidian-discord-guild-daily-review-final"`
     - `schedule.expr: "0 5 * * *"`
     - `schedule.tz: "Asia/Shanghai"`
     - `payload.kind: "agentTurn"`
     - `payload.message: "你是“小笔（Writer）”执行每日复盘整理..."`
   - **为什么这一步重要：** 先搞清楚它到底是显式脚本任务还是 prompt 任务，才能决定后续排查应该审源码还是审 prompt 与运行痕迹。

2. **确认是否存在独立源码、技能或模板实现**
   - 在工作区与相关目录做关键词检索，目标不是“多找点文件”，而是确认有没有真正负责读取 Discord 数据的固定代码：
     - `/Users/can4hou6joeng4/.openclaw/workspace`
     - `/Users/can4hou6joeng4/.openclaw`
     - `/Users/can4hou6joeng4/Documents/code/Ours`
   - 已实际使用的检索关键词包括：
     - `obsidian-discord-guild-daily-review-final`
     - `c6e92d09-5ff6-4079-b839-a9c4fe6d2e10`
     - `1478785297784373490`
     - `Conversation info`
     - `thread starter`
     - `message_reference`
     - `mentions`
     - `dispatch`
   - 目标案例的结论是：
     - 找到了 `jobs.json`
     - 找到了 run 记录
     - 找到了 Obsidian 产物
     - **没找到对应 JS/TS 脚本、skill 实现、模板源码**
   - **为什么这一步重要：** 如果没有独立实现代码，就不能假设“读取 API、分页、样本源覆盖”这些逻辑被明确写死；它们可能完全依赖模型临场决定。

3. **把 prompt 中“声明的筛选口径”与“缺失的机械实现”分开看**
   - 在同一个 job 配置里提取已声明的业务口径：
     - `仅处理 guild: 1478785964896817267`
     - `仅采集：用户 1478785297784373490 本人发言 + @该用户/回复该用户消息。`
     - `时间窗：昨日 00:00:00~23:59:59（Asia/Shanghai）。`
   - 同时明确记录：配置里**没有**这些可执行级约束：
     - 必须调用哪种 Discord read API
     - 必须先扫主频道，再扫 thread
     - 是否包含 thread starter
     - 是否读取 thread replies
     - mentions 如何判定
     - reply 如何判定 `message_reference.message_id` / `referenced_message.author.id`
     - `author.id` 是否强制按字符串比较
     - 是否做分页 / limit
   - **为什么这一步重要：** 很多“口径写得很清楚”的任务，真正的问题在于采样实现并没有被固定；只审口径会误判成“逻辑没问题”。

4. **读取最终产物，判断“是样本为空，还是分类后归零”**
   - 检查实际输出文件：
     - `/Users/can4hou6joeng4/Documents/Obsidian/Second Brain/01-Daily/2026-03-13.md`
     - `/Users/can4hou6joeng4/Documents/Obsidian/Second Brain/00-Inbox/Daily Sync Digest - 2026-03-13.md`
   - 目标案例中看到的关键措辞是：
     - `当日未检索到符合筛选条件的 Discord 发言、@提及或回复记录。`
     - `代表性线程 - 无`
     - 分类统计全 0
     - `昨日 Discord 在目标用户与关联互动口径下无有效样本`
   - 将这类措辞归类为：**上游直接认定没有检索到样本**，而不是“有样本但分类阶段把它们清成了 0”。
   - **为什么这一步重要：** 这是判断断点位置的核心证据，能直接把排查重心从分类逻辑转移到检索链路。

5. **读取运行记录，确认任务是成功结束还是异常中断**
   - 检查 run 记录文件：
     - `/Users/can4hou6joeng4/.openclaw/cron/runs/c6e92d09-5ff6-4079-b839-a9c4fe6d2e10.jsonl`
   - 目标案例确认到的字段：
     - `runAtMs: 1773435619913`
     - `status: "ok"`
     - `model: "gpt-5.4"`
     - `provider: "local-router"`
   - 同时确认 run 记录里**没有**这些诊断信息：
     - 读取了哪些 Discord 消息
     - 哪些线程被扫描
     - 是否读主频道
     - 使用了什么筛选条件落盘
   - **为什么这一步重要：** `status: "ok"` 只能证明没 crash、没 timeout，不能证明检索覆盖面正确；这是很多“表面成功”的陷阱。

6. **把产物结论与真实数据做对照，判断是否漏扫**
   - 对照缓存或已知事实，确认目标日期是否真实存在相关活动。
   - 目标案例中确认到：`2026-03-13` 在 `#dispatch` parent channel 下至少有这些 thread：
     - `1481844448030621867` `【分析】OpenClaw 3.11与3.8版本对比 - 20260313`
     - `1481833902929739776` `【运维】定时任务未执行日志核查 - 20260313`
     - `1481917901580800183` `【阅读】总结md文件内容 - 20260313`
     - `1481963835735801878` `【分析】无开发者账号iPhone开发分发 - 20260313`
     - `1482025613966446777` `【分析】查看当前skill-vetter - 20260313`
     - `1482070694136119478` `【任务】查找OpenClaw协同CLI skill - 20260314`
   - 再结合用户已知事实：
     - `2026-03-13 在 #dispatch 主频道确实存在多条该用户本人发言`
   - 得出目标案例的高可信判断：
     - **断点发生在检索/筛选前段，不是分类统计段**
   - **为什么这一步重要：** 真实数据一旦与“无样本”产物冲突，就可以从“是否真没数据”转向“哪些数据源没有被纳入”。

7. **优先锁定最可能的漏扫层：主频道消息与 thread starter**
   - 在没有源码的前提下，优先把这些断点列为最高嫌疑：
     - 只扫了 thread replies，没扫 parent channel 主消息
     - 没把主频道开帖消息（thread starter）当成样本
     - 只看了某一类消息结构，漏掉了主频道中带 thread 的原始消息
   - 用明确表述下结论：
     - **“主频道起帖消息会不会漏”——有高风险会漏，而且当前配置看不到任何显式保护。**
   - **为什么这一步重要：** 这一步能把“怀疑漏扫”收敛成具体可修复的样本源缺口，而不是停留在抽象层面。

8. **把无法证实但高风险的点单独列为边界**
   - 目标案例中，以下点不能 100% 证实，但必须明确写出：
     1. `author.id` 是否按字符串匹配
     2. `@该用户` 如何匹配
     3. `回复该用户` 如何匹配
     4. 时间窗是否精确落实为 Asia/Shanghai 昨日边界
     5. 是否真的扫描了主频道 / threads / thread replies
   - 同时标明原因：
     - **缺少实际源码或详细运行日志**
   - **为什么这一步重要：** 这样既能保持结论强度，又不会越过证据边界做伪确定性判断。

9. **给出最小可执行修复建议**
   - 目标案例中建议的修复顺序是：
     1. 把 cron 从“纯 prompt 任务”改成“显式脚本 / 固定工具链任务”
     2. 固定执行顺序：
        - 读 parent channel 主频道消息
        - 收集昨日新开的 thread starter message
        - 读这些 thread 的 replies
        - 再读所有与目标用户相关的 reply / mention
     3. 显式把样本源写死：
        - `#dispatch` 主频道消息
        - 主频道中创建 thread 的 starter message
        - 这些 thread 的 replies
     4. 所有 Discord snowflake 一律按 string 处理：
        - `author.id === "1478785297784373490"`
        - `mentions.some(m => m.id === "...")`
     5. 把 reply / mention 判定规则落成代码
     6. 把时间窗参数落成固定函数
     7. 加检索阶段审计日志
   - **为什么这一步重要：** 排查的价值不只是解释故障，更要把“不稳定的 prompt 行为”变成“可审计、可复现、可验证的固定链路”。

## Pitfalls and solutions

❌ 只看最终结果文件“全 0”，就直接怀疑分类逻辑  
→ 这会忽略“根本没有检索到样本”的可能  
→ ✅ 先读产物措辞，若出现“未检索到符合条件样本”，优先把断点定位到检索/筛选前段

❌ 看到 job 口径写了 guild、用户 ID、昨日时间窗，就默认实现是完整的  
→ prompt 只说明“要什么”，并不等于“怎么取”已经被固定  
→ ✅ 分开审“业务口径”和“机械实现”，明确是否存在固定脚本、API 调用、分页与样本源约束

❌ 只要 run 记录 `status: "ok"`，就认为任务逻辑正确  
→ 这只能说明任务没崩溃，不能证明读对了频道、读全了样本  
→ ✅ 把运行成功与检索正确分开判断，重点看是否有扫描明细与审计日志

❌ 认为 thread 有活动，就等于主频道入口消息一定被统计到了  
→ 纯 prompt 链路里，主频道消息、thread starter、thread replies 很可能是分离处理甚至被漏掉的  
→ ✅ 单独检查 parent channel 主消息是否被纳入样本源，尤其关注 thread starter

❌ 默认 Discord Snowflake 可以安全当 number 比较  
→ 这可能带来精度或匹配异常，而且无源码时你根本无法确认运行时怎么比较  
→ ✅ 在修复建议里把所有 ID 比较收敛到字符串匹配，并写成显式代码

❌ 把“时间窗是 Asia/Shanghai 昨日”当作已被运行时严格落实  
→ 配置声明不等于 API 查询边界真的按 `00:00:00~23:59:59.999 +08:00` 执行  
→ ✅ 明确把时间窗列为“配置已声明、运行未证实”的边界项，后续用固定函数实现

## Key code and configuration

```json
{
  "id": "c6e92d09-5ff6-4079-b839-a9c4fe6d2e10",
  "name": "obsidian-discord-guild-daily-review-final",
  "schedule": {
    "expr": "0 5 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "你是“小笔（Writer）”执行每日复盘整理..."
  }
}
```

```text
/Users/can4hou6joeng4/.openclaw/cron/jobs.json
/Users/can4hou6joeng4/.openclaw/cron/runs/c6e92d09-5ff6-4079-b839-a9c4fe6d2e10.jsonl
/Users/can4hou6joeng4/Documents/Obsidian/Second Brain/01-Daily/2026-03-13.md
/Users/can4hou6joeng4/Documents/Obsidian/Second Brain/00-Inbox/Daily Sync Digest - 2026-03-13.md
```

```json
{
  "runAtMs": 1773435619913,
  "status": "ok",
  "model": "gpt-5.4",
  "provider": "local-router"
}
```

```text
仅处理 guild: 1478785964896817267
仅采集：用户 1478785297784373490 本人发言 + @该用户/回复该用户消息。
时间窗：昨日 00:00:00~23:59:59（Asia/Shanghai）。
```

```js
author.id === "1478785297784373490"
mentions.some(m => m.id === "1478785297784373490")
```

```text
建议固定执行顺序：
1. 读 parent channel 主频道消息
2. 收集昨日新开的 thread starter message
3. 读这些 thread 的 replies
4. 再读所有与目标用户相关的 reply / mention
```

## Environment and prerequisites

- 需要能访问本机 OpenClaw cron 配置与运行记录。
- 需要能读取 Obsidian 产物文件，用于核对最终输出措辞。
- 需要能检索 workspace、OpenClaw 目录和相关代码目录，以确认是否存在独立实现脚本。
- 目标案例的关键环境信息：
  - 调度表达式：`0 5 * * *`
  - 时区：`Asia/Shanghai`
  - 任务类型：`agentTurn`
  - 模型记录：`gpt-5.4`
  - provider：`local-router`
- 需要了解 Discord 的数据结构概念：
  - parent channel
  - thread starter
  - thread replies
  - `mentions`
  - `message_reference`
  - `referenced_message.author.id`
  - Snowflake ID 应按字符串处理

## Task record

Task title: OpenClaw runtime context (internal):
This context is runt...
Task summary:
- 已确认 `obsidian-discord-guild-daily-review-final` 没有在 workspace 中找到独立源码/脚本实现。
- 已确认它是通过 `/Users/can4hou6joeng4/.openclaw/cron/jobs.json` 中的 `payload.kind: "agentTurn"` 运行的纯 prompt 驱动任务。
- 已检索 `.openclaw/workspace`、`.openclaw`、相关代码目录，并使用了 job 名称、job id、用户 id、`thread starter`、`message_reference`、`mentions`、`dispatch` 等关键词；结果未发现对应 JS/TS 脚本或 skill 模板源码。
- 已核对 Obsidian 产物，发现措辞为“未检索到符合筛选条件的 Discord 发言、@提及或回复记录”，说明样本在分类前已为 0。
- 已核对 run 记录，任务状态为 `ok`，但没有扫描范围、命中数、频道覆盖、检索明细等可审计信息。
- 已结合真实线程活动与用户补充事实，得出高可信判断：问题更可能出在采样阶段漏扫/漏判，而不是分类阶段清零。
- 已识别主频道消息与 thread starter 未被显式纳入样本源是最高风险断点。
- 已列出无法 100% 证实的边界项：Snowflake 字符串匹配、mention/reply 结构化判定、Asia/Shanghai 时间窗运行时落实方式、主频道与 thread 扫描覆盖范围。
- 已形成最小修复建议：将纯 prompt 任务改为脚本化检索链路，显式纳入主频道、thread starter、thread replies，并增加字符串匹配与审计日志。

## Companion files

- `references/prompt-agentturn-cron-evidence-boundaries.md` — reference documentation
- `references/discord-daily-sampling-contract.md` — reference documentation