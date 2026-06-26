---
name: "diagnose-scheduled-job-trigger-vs-execution-failure"
description: "用于排查“定时任务没执行”这类问题，并区分到底是未触发、已触发但执行失败，还是运行环境/授权失效导致的假象。遇到 cron 异常、任务未跑、自动任务失灵、网关重启后要验证恢复、怀疑是模型导致任务失败、需要查看日志作证、需要给出证据口径、要确认 `deactivated_workspace` / OAuth token 失效 / timeout 是否为根因时，都应触发本技能。也适用于“任务其实有 run 记录，但结果是 error”“想确认调度正常还是执行链路坏了”“修复授权后要做回归验证”等场景。"
metadata: { "openclaw": { "emoji": "🕒" } }
---

# 诊断定时任务是“未触发”还是“执行失败”

帮助你用日志和运行记录证明 cron/定时任务的真实故障位置，避免把“调度正常但执行失败”误判为“任务根本没跑”。

## When to use this skill
- 当你需要判断“定时任务没执行”到底是调度器没触发，还是任务已被拉起但在执行阶段失败。
- 当你要为事故结论提供证据，尤其是需要证明“不是模型本身导致没跑”，而是 workspace、授权、会话、token 或超时问题。
- 当你已经修复了授权、配置或网关，想验证系统是否真正恢复，而不是只看服务进程是否在线。
- 当用户描述为“cron 挂了”“自动任务最近都失效”“重启后想确认恢复”“日志里有 `deactivated_workspace` / `oauth token invalid` / timeout”等情况。

## Steps

1. **先把问题拆成两条证据链：调度是否发生、执行是否成功。**  
   先明确不要直接接受“任务没执行”的表述，而要分别查：
   - 网关/调度日志里是否有 cron 触发痕迹
   - 任务注册信息、最近运行时间、运行状态、错误码  
   这样做的原因是：很多故障并不是“没调度”，而是“调度正常但执行失败”，两者结论完全不同。

2. **列出当前系统中的定时任务，并核对最近一次运行记录。**  
   重点抓每个任务的：
   - 任务名
   - 最近运行时间
   - 状态：`ok` / `error`
   - 错误详情  
   本次排查中，确认系统里有 **9 个 cron 任务**，且多个任务都带有明确的最近运行时间与错误状态，例如：
   - `obsidian-discord-guild-daily-review-final`
   - `juejin-daily-checkin-lottery`
   - `seedpool-daily-auto-publish`
   - `dispatch-thread-rename-backstop`  
   这样做的原因是：只要“最近运行时间”存在，就能证明任务并非完全没被调度。

3. **用“最近运行时间 + error 状态”证明任务其实被触发过。**  
   本次实际查到的关键证据是：
   - `obsidian-discord-guild-daily-review-final`
     - 最近运行：`2026-03-12 05:00`
     - 状态：`error`
     - 错误：`{"detail":{"code":"deactivated_workspace"}}`
   - `juejin-daily-checkin-lottery`
     - 最近运行：`2026-03-12 09:10`
     - 状态：`error`
     - 错误：`{"detail":{"code":"deactivated_workspace"}}`
   - `seedpool-daily-auto-publish`
     - 最近运行：`2026-03-12 09:30`
     - 状态：`error`
     - 错误：`{"detail":{"code":"deactivated_workspace"}}`
   - `dispatch-thread-rename-backstop`
     - 最近运行：`2026-03-12 23:30` 左右
     - 状态：`error`
     - 错误：`{"detail":{"code":"deactivated_workspace"}}`
     - 且连续错误 `9` 次  
   这样做的原因是：这组证据足以支撑“调度器在跑，任务也被拉起了，但执行时失败”。

4. **继续向前翻运行历史，判断是长期配置问题还是近期退化。**  
   本次实际核对到：
   - Discord 日整理：`3/05`、`3/06`、`3/07`、`3/08`、`3/09`、`3/10` 都有 `ok`
   - 掘金签到：`3/05` 到 `3/11` 多日都有 `ok`
   - Seedpool 日报：`3/09`、`3/10`、`3/11` 都有 `ok`  
   这样做的原因是：如果同一批任务前几天长期正常，就更像“最近运行环境或授权状态变了”，而不是 cron 从一开始就没配好。

5. **汇总错误类型，不要只盯一个模型或一次失败。**  
   本次实际观察到三类错误：
   - `deactivated_workspace`
   - `Encountered invalidated oauth token for user, failing request`
   - `Error: cron: job execution timed out`  
   这样做的原因是：如果错误集中在 workspace、OAuth、超时层，而不是输出内容异常，就应把排查重点放在运行环境、鉴权和会话，而不是先怪模型能力。

6. **核对历史 runs 用过的模型/供应商，避免把“碰巧用了某模型”误当根因。**  
   本次实际看到历史上跑过多个模型/供应商：
   - `openai-codex / gpt-5.3-codex`
   - `openai-codex / gpt-5.4`
   - `aigocode / claude-sonnet-4-6`
   - `aigocode / claude-opus-4-6`
   - `minimax-portal / MiniMax-M2.5`  
   这样做的原因是：如果多个供应商和模型都跑过，而最近主错误仍然统一是 `deactivated_workspace`，那更像共享执行环境失活，而不是某个模型“把任务搞没了”。

7. **先给出保守结论：能证明异常存在，但不能越过证据下结论。**  
   在未拿到更多上下文前，本次形成的正确表述是：  
   > 定时任务并非未触发，而是在最近几次调度中于执行阶段集中失败；主要错误为 `deactivated_workspace`，另有 OAuth token 失效与超时情况。现有日志不足以证明是模型能力本身导致，更像是 workspace / 会话 / 鉴权层异常影响了任务执行。  
   这样做的原因是：事故表述需要和证据严格对齐，先区分“可证实”和“待确认”。

8. **如果用户补充了业务背景，把日志证据与背景信息闭环。**  
   本次用户补充了关键事实：
   - 此前 `Codex team` 被踢出
   - 之后才出现 `deactivated_workspace`
   - 已重新授权
   - 已重配 `openclaw.json`
   - 已重启网关  
   结合前面的日志证据，就可以把根因从“待确认”升级为：
   > 由于此前 Codex team 被踢出，相关 workspace 失活，导致 cron 任务虽被调度但在执行阶段报 `deactivated_workspace` 并失败。  
   这样做的原因是：日志通常证明“现象和直接错误”，而补充背景有时才能把因果链真正闭合。

9. **修复后先做“链路验证”，不要只看网关进程在线。**  
   本次恢复验证按三步执行：
   1. 看当前 cron 状态里是否还残留 `deactivated_workspace`
   2. 手动触发 `2~3` 个代表任务
   3. 用 run 结果和实际产出/投递结果判断是否恢复  
   这样做的原因是：单看“服务重启成功”无法证明自动任务链路恢复，必须看到真实任务走完。

10. **选轻任务、内容任务、复杂任务各一个做回归。**  
    本次实际选了：
    - 轻任务：`juejin-daily-checkin-lottery`
    - 内容任务：`seedpool-daily-auto-publish`
    - 复杂任务：`obsidian-discord-guild-daily-review-final`  
    这样做的原因是：不同任务覆盖不同故障面，能避免“只测简单任务就误判全面恢复”。

11. **先确认任务是否成功入队，再确认是否真正进入执行。**  
    本次回归时先确认：
    - 三个任务都已成功入队
    - 后续日志出现了新 session / `auto-recall` / `agent_end` 痕迹  
    这样做的原因是：入队成功只能证明调度入口可用；出现执行痕迹，才能证明执行链路开始恢复。

12. **对轻任务和内容任务，用最终状态和交付结果证明已恢复。**  
    本次实际验证到：
    - `juejin-daily-checkin-lottery`
      - 新 run 已创建
      - 执行状态：`ok`
    - `seedpool-daily-auto-publish`
      - 执行状态：`ok`
      - `delivered = true`
      - `deliveryStatus = delivered`  
    这样做的原因是：这能证明“调度 → 执行 → 结果投递”的完整链路已恢复，不再卡在 `deactivated_workspace`。

13. **对复杂任务，单独验证“被拉起”与“最终落盘/产出”两个层次。**  
    本次复杂任务的现状是：
    - 已被成功拉起
    - 日志中有：
      - `cron:c6e92d09-...`
      - `auto-recall`
      - 新 session 已创建
    - 但截至核验时：
      - `cron.runs` 里还没有新的 `finished` 结果
      - 目标文件未生成：
        - `01-Daily/2026-03-12.md`
        - `00-Inbox/Daily Sync Digest - 2026-03-12.md`  
    这样做的原因是：复杂任务常常不是“能启动”就等于“已恢复”，还要看是否走到最终落盘或交付。

14. **把恢复结论分级，不要二元化成“好了/没好”。**  
    本次最终结论是：  
    > 当前系统已从“全线失效”恢复到“部分恢复且核心链路可用”状态。  
    更细分为：
    - cron 调度入口：已恢复
    - 模型执行链路：已恢复
    - 至少 2 个代表任务：已实跑成功
    - 复杂 Obsidian 日整理任务：已能启动执行，但尚未完成验证  
    这样做的原因是：分层结论更符合真实状态，也更适合后续继续追踪。

15. **给出下一步操作建议：继续盯复杂任务或补跑下一轮。**  
    本次建议是：
    - 继续盯复杂任务 `5~10` 分钟，看最终结果
    - 或再手动补跑一次复杂任务 / 等下一次定时触发
    - 若成功生成：
      - `01-Daily/2026-03-12.md`
      - `00-Inbox/Daily Sync Digest - 2026-03-12.md`
      则可把结论升级为“主任务链路已恢复正常”  
    这样做的原因是：恢复验证要有闭环，不应停在“看起来好像好了”。

## Pitfalls and solutions

❌ 直接把“任务没执行”当成“cron 没触发”  
→ 只看表象会把执行失败误判成调度失败  
✅ 同时核对“最近运行时间”和“最终状态”；只要有 run 时间，就优先判断为“已触发过，再看为何失败”

❌ 看到最近失败发生在某个模型上，就断言是模型导致  
→ 同一批任务历史上可能跑过多个模型/供应商，且共享错误可能来自 workspace 或鉴权层  
✅ 先看错误码是否统一，如 `deactivated_workspace`、`oauth token invalid`、timeout；若错误集中在运行环境层，就不要把锅直接甩给模型能力

❌ 只看最近一次失败，不查历史成功记录  
→ 你会错失“这是近期退化而不是长期配置错误”的关键证据  
✅ 向前翻多天 runs，确认任务此前是否长期 `ok`

❌ 修复后只看“网关已重启 / 服务在线”就宣布恢复  
→ 进程在线不等于 cron、执行链路、投递链路都恢复  
✅ 至少手动回归一个轻任务、一个内容任务、一个复杂任务，并查看 run 结果与实际产出

❌ 复杂任务一旦被拉起，就判定“完全恢复”  
→ 复杂任务可能中途卡住、未落盘、未投递  
✅ 把“已启动执行”和“最终完成落盘/交付”分开验证

❌ 在证据不足时写“模型导致定时任务都没执行”  
→ 这个说法混淆了未触发与执行失败，也可能超出证据范围  
✅ 先用更严谨口径：  
“任务并非未触发，而是在执行阶段失败；主要错误为 `deactivated_workspace`，更像 workspace / 授权 / 会话层异常。”

## Key code and configuration

### 事故判断结论模板（证据未闭环时）
```text
经核查，当前异常并非“定时任务没有被调度”，而是“任务已按计划触发，但在执行阶段失败”。多个任务最近一次运行均记录为 error，主要错误码为 `deactivated_workspace`，另有 `invalidated oauth token` 与执行超时。历史 runs 显示这些任务在前几天长期正常，因此更接近近期运行环境/工作区状态异常，而非 cron 调度器失效。现有证据不足以直接证明是模型本身导致任务不执行。
```

### 事故判断结论模板（根因已由补充背景闭环时）
```text
经核查，异常并非 cron 未触发，而是任务触发后在执行阶段失败。主要报错为 `deactivated_workspace`。结合后续排查结果，可确认该错误与此前 Codex team 被踢出、导致 workspace 授权/可用性失效有关，而非单纯调度器失灵。现已重新授权、更新 `openclaw.json` 并重启网关。
```

### 恢复验证结论模板（部分恢复）
```text
当前系统已从“全线失效”恢复到“部分恢复且核心链路可用”状态。

- cron 调度入口：已恢复
- 模型执行链路：已恢复
- 至少 2 个代表任务：已实跑成功
- 复杂任务：已能启动执行，但尚未完成验证

这说明系统已明显恢复，不再是此前那种因 workspace 失活导致的全面执行失败；但复杂型任务还需要继续观察 1 轮，才能确认完全恢复。
```

### 本次实际核验到的关键证据片段
```text
obsidian-discord-guild-daily-review-final
- 最近运行：2026-03-12 05:00
- 状态：error
- 错误：{"detail":{"code":"deactivated_workspace"}}

juejin-daily-checkin-lottery
- 最近运行：2026-03-12 09:10
- 状态：error
- 错误：{"detail":{"code":"deactivated_workspace"}}

seedpool-daily-auto-publish
- 最近运行：2026-03-12 09:30
- 状态：error
- 错误：{"detail":{"code":"deactivated_workspace"}}

dispatch-thread-rename-backstop
- 最近运行：2026-03-12 23:30 左右
- 状态：error
- 错误：{"detail":{"code":"deactivated_workspace"}}
- 连续错误：9 次
```

### 本次恢复验证的成功证据片段
```text
juejin-daily-checkin-lottery
- 新 run 已创建
- 执行状态：ok

seedpool-daily-auto-publish
- 新 run 时间：今天 10:11 后
- 执行状态：ok
- delivered = true
- deliveryStatus = delivered

obsidian-discord-guild-daily-review-final
- 日志中已出现：
  - cron:c6e92d09-...
  - auto-recall
  - 新 session 已创建
- 但截至核验时仍未见 finished 落盘结果
```

### 复杂任务是否真正恢复的落盘检查点
```text
01-Daily/2026-03-12.md
00-Inbox/Daily Sync Digest - 2026-03-12.md
```

## Environment and prerequisites
- 你需要能访问：
  - cron/调度日志
  - 网关或执行器日志
  - 任务注册列表
  - `cron.runs` 或等价运行历史
  - 任务产出物或投递状态
- 你需要能查看任务的：
  - 最近运行时间
  - 状态字段（如 `ok` / `error`）
  - 错误详情
  - 运行所用模型/供应商
- 如果要做恢复验证，最好具备：
  - 手动触发任务的权限
  - 查看新 session / `auto-recall` / `agent_end` 等执行痕迹的权限
  - 查看目标文件、产出落盘、消息投递状态的权限
- 本次已知与故障相关的环境动作包括：
  - 重新授权
  - 更新 `openclaw.json`
  - 重启网关
- 本次实际遇到的典型错误类型：
  - `deactivated_workspace`
  - `Encountered invalidated oauth token for user, failing request`
  - `Error: cron: job execution timed out`