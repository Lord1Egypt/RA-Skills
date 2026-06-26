---
name: "discord-thread-naming-backstop-workflow"
description: "用于执行 Discord 线程命名兜底（backstop）巡检与改名，专门处理某个 guild 下指定 parent channel 中“最近新建但未命名规范”的线程，补上 prehook 漏网，而不是批量回扫历史。遇到“线程重命名兜底”“dispatch 线程命名规范”“只检查最近 20 分钟线程”“JSON 污染标题”“长标题截断”“按规则静默改名或告警”“Discord thread-list / channel-edit / channel-info 重试与一致性检查”等场景时就应触发。即使用户没说 backstop，只要意图是低扰动修正新线程标题，也应使用此技能。"
metadata: { "openclaw": { "emoji": "🧵" } }
---

# 执行 Discord 线程命名兜底巡检与静默改名

这个技能帮助你在严格范围内为 Discord 新线程做命名兜底，避免误扫历史线程、误改旧标题，且在失败时有一致的告警与回补闭环。

## When to use this skill
- 当你需要只检查某个父频道下“最近新建”的线程，并对漏掉 prehook 的异常标题做低扰动修正。
- 当用户强调“不要回扫历史”“只处理最近 20 分钟”“今天但明显是截断/JSON 污染的也可处理”时。
- 当你需要按固定命名模板 `【类型】目标 - YYYYMMDD` 自动推断新名，并在失败时做重试、一致性校验、P2/RESOLVED 通知。
- 当任务要求成功时尽量静默，避免刷屏，只在最终失败或“先失败后成功”时发送通知。

## Steps

1. **锁定执行范围**
   - 只针对以下固定范围执行：
     - `guildId="1478785964896817267"`
     - `channelId="1478785965580357754"`（🎛️丨dispatch）
     - 只处理线程，不改 parent channel。
   - 为什么：这个任务的核心就是“兜底漏网的新线程”，范围一旦放宽，就会误改历史线程或错误频道。

2. **按指定接口读取线程列表**
   - 仅使用：
     ```text
     message(action="thread-list", guildId="1478785964896817267", channelId="1478785965580357754", includeArchived=false, limit=50)
     ```
   - 若第一次失败，立即重试 1 次；两次都失败才进入 P2 告警。
   - 本次实际执行中，`thread-list` 成功读取，且后续复核时也再次成功。
   - 为什么：用户明确限制了读取方式；先读列表再筛选，能保证行为可审计且可控。

3. **用 Asia/Shanghai 时区判定候选线程**
   - 将当前时间视为 `Asia/Shanghai`，本次记录中的执行时点为：
     - `2026-03-14 10:35`
     - `2026-03-14 10:38`
     - `2026-03-14 10:40`
     - `2026-03-14 10:42`
   - 只保留满足任一条件的线程：
     - `thread_metadata.create_timestamp` 在最近 20 分钟内；
     - 或者创建于今天，且名称明显属于“主消息截断 / 长标题 / JSON 污染”异常，例如：
       - 长度 `> 60`
       - 含 `{` `}` `[` `]` `\"`
       - 含代码块、URL、键值对痕迹
       - 明显是口语长句截断，如“请你为我…/帮我…/当前…/那么…/另外关于…”
   - 必须跳过：
     - 创建时间早于今天的历史线程；
     - 今天但超过 20 分钟，且只是“普通旧标题但不规范”的线程。
   - 为什么：这是防止兜底任务退化为历史清扫任务的关键边界。

4. **先检查是否已经合规**
   - 用以下规则判断线程名是否已规范：
     ```regex
     ^【[^】]+】.+ - \d{8}$
     ```
   - 已匹配规范的线程直接跳过，不做任何改动。
   - 本次实际执行中，可见线程要么已合规，要么属于不应处理的历史线程。
   - 为什么：兜底任务应只修复漏网异常，不应对已合规对象重复操作。

5. **限制处理数量**
   - 单次运行最多处理 `3` 个线程。
   - 为什么：即使有异常，也要控制改动规模，避免一次任务影响过大或在异常场景下放大错误。

6. **为每个待修正线程生成操作 ID**
   - 格式：
     ```text
     rename-<threadId>-<YYYYMMDDHHmmss>
     ```
   - 为什么：后续重试、告警、回补都依赖这个 opId 做单次运行内去重与追踪。

7. **推断新线程名**
   - 使用模板：
     ```text
     【{类型}】{目标} - {YYYYMMDD}
     ```
   - 约束：
     - 时区：`Asia/Shanghai`
     - 总长度：`<= 100`
   - 类型只允许以下之一：
     ```text
     任务 / 分析 / 阅读 / 修复 / 运维 / 文档 / 复盘 / 审查 / 复核 / 评估
     ```
   - 优先级规则：
     - 含 `配置/部署/环境/服务/监控/cron/openclaw.json/模型切换/供应商接入/密钥/代理` → 优先 `【运维】`
     - 含 `规则/规范/SOP/制度/约定/命名/模板/文档/说明/公告` → 优先 `【文档】`
     - 含 `报错/异常/失败/修复/故障/bug` → 优先 `【修复】`
   - 目标提取前先归一化：
     - 只保留 `8~28` 字的“动作 + 对象”核心短语；
     - 去掉口语前缀、JSON 尾巴、代码块、URL、长数字串、参数串、键值对；
     - 无法稳定提取时，使用 `未命名任务`。
   - 为什么：线程标题来自自然语言主消息时，经常混入口语、JSON 或参数噪音，先归一化才能稳定命名。

8. **执行重命名，并做容错**
   - 第一次改名：
     ```text
     message(action="channel-edit", target="<threadId>", name="<newName>")
     ```
   - 若失败，再执行一次相同参数的 `channel-edit`。
   - 若仍失败，再执行：
     ```text
     message(action="channel-info", target="<threadId>")
     ```
   - 一致性判定：
     - 若当前名称已符合规则，或已等于 `newName` → 视为成功，不报 P2；
     - 若仍不符合 → 发送最终失败 P2。
   - 为什么：Discord 侧偶发瞬时失败并不等于最终失败，做最终一致性检查能避免误报。

9. **按结果决定是否静默**
   - 正常成功时保持静默。
   - 如果本次没有候选线程，也保持静默。
   - 本次实际执行结果：
     - 最近 20 分钟内新建线程：`0`
     - 今日且属于“主消息截断/长标题/JSON污染”的候选：`0`
     - 需改名线程：`0`
     - 因此本轮静默退出：无改名、无 P2、无 RESOLVED。
   - 为什么：这类 backstop 任务通常高频运行，成功时静默可避免通知噪音。

10. **仅在需要时发送 P2 或 RESOLVED**
    - 列表两次失败时，发送 1 条 P2，且：
      - `threadId=list`
    - 单个线程最终失败时，发送 1 条 P2。
    - 同一 `opId` 里若先失败、后经重试或一致性检查判定成功，发送 1 条 `RESOLVED` 到 `1478996389727043584`。
    - 单次运行同一线程只允许最终输出 `0` 或 `1` 条消息，禁止重复刷屏。
    - 为什么：这个任务强调“低噪音 + 可追踪”，通知必须少而准。

## Pitfalls and solutions

- ❌ 把“今天但超过 20 分钟、只是普通旧标题不规范”的线程也纳入改名 → 这会把兜底任务变成历史修复任务，违背范围约束 → ✅ 只处理最近 20 分钟，或“今天且明显是截断/JSON 污染”的异常标题。

- ❌ 看到标题不规范就直接改名 → 可能误改本来已经符合 `^【[^】]+】.+ - \d{8}$` 的线程，或者误动历史线程 → ✅ 先做正则校验，再结合创建时间和异常特征筛选。

- ❌ `channel-edit` 一次失败就直接报 P2 → Discord 瞬时失败并不少见，直接告警会制造误报 → ✅ 先重试一次，再用 `channel-info` 做最终一致性检查。

- ❌ 成功时也发通知 → 高频巡检会刷屏，掩盖真正异常 → ✅ 正常成功与“无候选线程”都保持静默。

- ❌ 列表失败时用 `threadId=0`、`n/a` 之类占位值告警 → 不利于排查，也违背约束 → ✅ 只有列表失败场景可使用 `threadId=list`。

- ❌ 扫描 archived 或更大范围线程 → 会把任务从“backstop”变成“回扫历史” → ✅ 严格使用 `includeArchived=false` 且固定 `channelId`。

## Key code and configuration

### 线程列表读取

```text
message(action="thread-list", guildId="1478785964896817267", channelId="1478785965580357754", includeArchived=false, limit=50)
```

### 命名规范正则

```regex
^【[^】]+】.+ - \d{8}$
```

### 新名称模板

```text
【{类型}】{目标} - {YYYYMMDD}
```

### 类型白名单

```text
任务
分析
阅读
修复
运维
文档
复盘
审查
复核
评估
```

### 重命名动作

```text
message(action="channel-edit", target="<threadId>", name="<newName>")
```

### 最终一致性检查

```text
message(action="channel-info", target="<threadId>")
```

### P2 模板（仅最终失败时发送到 `1478996389727043584`，纯文本）

```text
━━━━━━━━━━━━━━
🚨 任务告警 · dispatch-thread-rename-backstop
等级：P2
状态：🔴 失败
日期：YYYY-MM-DD (Asia/Shanghai)

对象：threadId=<id> opId=<opId>
原因：<最终失败摘要，不超过60字>
影响：线程命名规范可能未及时生效
动作：请人工介入排查并重试

追踪：#cron #dispatch #naming #incident
━━━━━━━━━━━━━━
```

### RESOLVED 模板（仅“先失败后成功”时发送到 `1478996389727043584`，纯文本）

```text
━━━━━━━━━━━━━━
✅ 任务回补 · dispatch-thread-rename-backstop
状态：🟢 RESOLVED
日期：YYYY-MM-DD (Asia/Shanghai)

对象：threadId=<id> opId=<opId>
说明：重命名过程中出现瞬时失败，已自动恢复并满足命名规范
结果：<最终名称>

追踪：#cron #dispatch #naming #resolved
━━━━━━━━━━━━━━
```

### 本次执行结论样例

```text
thread-list succeeded on first attempt. Filtering only parent channel 1478785965580357754 entries: all visible threads under target parent already match ^【[^】]+】.+ - \d{8}$, or are historical. Recent-today threads (within 20 min from 10:40 Asia/Shanghai means since 10:20) under target parent: 1482198526019764467 created 10:07 CST, 1482185516668424355 created 09:16 CST, both older than 20 min and already compliant. No today abnormal long/JSON-polluted noncompliant titles found. No rename actions needed; remain silent.
```

## Environment and prerequisites

- 可调用 Discord 相关消息动作：
  - `thread-list`
  - `channel-edit`
  - `channel-info`
- 具备目标 guild / channel 的读取与线程改名权限。
- 任务运行时必须能以 `Asia/Shanghai` 为基准做日期与“最近 20 分钟”判断。
- 只读取：
  - `guildId="1478785964896817267"`
  - `channelId="1478785965580357754"`
- 目标通知频道：
  - `1478996389727043584`
- 单次最多处理 `3` 个线程。
- 仅改名线程，不改 parent channel。

## Companion files

- `references/dispatch-thread-rename-notification-templates.md` — reference documentation