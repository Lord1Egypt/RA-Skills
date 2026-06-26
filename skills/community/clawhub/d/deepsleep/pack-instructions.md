# DeepSleep 阶段一：深度睡眠打包指令（v3.0）

⚠️ **时间预算：15 分钟。高效执行，不要浪费 tool call。**

## 第-1步：锁定日期（防 midnight 竞态）
Pack 在 23:50 启动，可能跨过午夜。
**在脚本最开头立即确定目标日期，后续所有步骤都使用这个固定日期。**

具体做法：
1. 用 `session_status` 或 `exec` 获取当前时间
2. **如果当前时间在 23:00-23:59** → 目标日期 = 今天（正常情况）
3. **如果当前时间在 00:00-00:39** → 目标日期 = **昨天**（说明已跨午夜，但 pack 的内容仍属于昨天）
4. 将目标日期记为 `PACK_DATE`（格式 YYYY-MM-DD），后续所有文件名、标题都用 `PACK_DATE`

⚠️ **绝对不要在后续步骤中重新获取日期**。一旦锁定，全程使用 `PACK_DATE`。

## 第0步：发现活跃 session + 静默日快速判断
用 `sessions_list(kinds=['group', 'main'], activeMinutes=1440, messageLimit=1)` 获取过去24小时活跃的群和主 session。

### 🔇 静默日快速路径（v3.0 核心优化：省 token）
**如果 sessions_list 返回为空（或所有 session 的最后一条消息都是 heartbeat/系统消息），这是一个"静默日"。**

⚡ **v3.0 改进：静默日不拉历史、不发晨报。直接做文件搬运即可。**

静默日执行路径：
1. 读取最近的 daily file（昨天，或向前追溯最多 7 天）中的 `## DeepSleep Daily Summary`
2. 计算连续静默天数（见衰减规则）
3. 按衰减级别生成 carry-forward 摘要
4. **跳过第1-2步**（不拉 sessions_history = 省 5-8 万 token）
5. 直接进入第4步写入 daily file
6. 在 daily file 中设置 `dispatch_policy: silent`（dispatch 读到此标记后只更新快照，不发晨报消息）
7. 跳过第5步（MEMORY.md 无新内容可更新）

**静默日总 token 消耗目标：< 5000 token**（仅文件读写，无 LLM 摘要生成）

### 🕰️ 静默日衰减机制（Silent Day Decay）

| 连续静默天数 | 行为 |
|---|---|
| **1-3 天** | 完整 carry-forward：OQ + 待办 + 行动项 + 各群进展标记 |
| **4-7 天** | 精简 carry-forward：只保留 OQ + 未完成待办。去掉行动项和群进展标记 |
| **8-14 天** | 最小 carry-forward：只保留 OQ。待办降级为"长期搁置"。OQ 中超过 7 天未进展的标注 ⚠️ |
| **15+ 天** | 归档：OQ 写入 `MEMORY.md ## Open Questions (Archived)`，daily file 仅一行说明，不触发 dispatch |

**如何计算连续静默天数：**
1. 从昨天的 daily file 检查是否包含"连续静默 N 天"
2. 如果有 → 今天 = N + 1
3. 如果没有（昨天是活跃日）→ 今天 = 1
4. 如果昨天没有 daily file → 向前扫描找到最近的文件，计算间隔天数

**恢复活跃时的处理：**
当静默期结束（sessions_list 有活跃 session），正常走第1-2步。
- 如果之前已归档到 MEMORY.md → Phase 3 加载可恢复上下文
- 如果静默 < 15 天 → 快照文件仍有最新 carry-forward 内容

**如果有活跃 session**，正常继续第1步。

## 第1步：批量拉取对话历史
对每个活跃 session 用 `sessions_history(sessionKey=<key>, limit=50)` 拉取对话。
⚡ 尽可能在同一个 tool call batch 中并行拉取多个 session 的历史。不要串行！

## 第2步：筛选 + 生成摘要 + 重要度标注

对每段对话内容，按以下标准决定保留什么：
- ✅ 决策、教训、偏好、关系、进展 → 保留
- ❌ 临时内容（天气、心跳、例行操作）、MEMORY.md 中已有的 → 跳过

### 📊 记忆重要度分层（v3.0 新增）
对每条保留的摘要条目，标注重要度：
- **🔴 P0 — 战略决策**：影响项目方向、长期计划、关键里程碑（如"确定用 910B 架构"）
- **🟡 P1 — 重要进展**：功能完成、问题解决、技术选型（如"v2.1 发布到 GitHub"）
- **🟢 P2 — 常规记录**：日常讨论、信息交换、待确认事项

摘要格式示例：
```
- 🔴 确定百万路视频架构采用全昇腾 910B 方案，放弃 A100 路线
- 🟡 DeepSleep v2.2 Silent Day 功能实现并推送 GitHub
- 🟢 讨论了 Moltbook 帖子回复策略
```

Phase 3 加载时，如果 token 紧张，优先加载 🔴 和 🟡，跳过 🟢。

### 🔗 跨群关联检测（v3.0 新增）
在生成摘要时，检查不同群之间是否存在关联话题：
1. 扫描所有群的摘要关键词
2. 如果两个群的摘要涉及相同主题（如"视频训练"出现在多个群），标注关联：
   ```
   ### 🔗 跨群关联
   - 视频训练实验室 ↔ 千问微调实验室：都在讨论 Qwen-VL 微调，可合并推进
   - SAMR群 ↔ 外卖巡检群：食品安全主题交叉，SAMR 政策可指导巡检规则
   ```
3. 跨群关联写入 daily summary 的独立段落（在各群摘要之后、OQ 之前）
4. Phase 3 加载时，如果当前群有关联群，附带提示

### OQ 健康检查（v3.0 新增）
在第2步末尾，对所有 Open Questions 执行健康检查：
- 计算每个 OQ 的存活天数（从首次记录到今天）
- **7 天未进展**：标注 ⚠️ 提醒（"此问题已悬挂 N 天，建议主动推进或降级"）
- **14 天未进展**：建议升级为 schedule.md 的显式任务，或标记为"搁置"
- **30 天未进展**：归档到 MEMORY.md，从 daily carry-forward 中移除

如果某个群今天完全没有用户消息（只有系统/心跳），跳过该群。
但是！**不要跳过有未解决 OQ 或未完成待办的群**——即使今天没有新对话，这些群仍需出现在摘要中以保持连续性。

## 第3步：Schedule 远期记忆

对话中提到的远期事项写入 `~/clawd/memory/schedule.md`。

**去重规则**：schedule.md 表格的第一列是 `Key`。
- 写入前先读取现有内容，检查 Key 是否已存在
- 已存在 → 只更新状态列，不追加新行
- 不存在 → 追加新行

### 📋 Schedule 优先级 + 到期提醒（v3.0 新增）

**优先级规则**：
- **P0 — 必须当天完成**：到期日当天出现在晨报中，并且触发 Phase 3 中的主动提醒
- **P1 — 重要但可延期**：到期日当天出现在晨报中
- **P2 — 长期/低优**：到期时仅在 daily summary 中提及，不出现在晨报

**提醒频率**（到期日倒数）：
| 距到期天数 | P0 行为 | P1 行为 | P2 行为 |
|---|---|---|---|
| 到期日 | 晨报 + Phase3 主动提醒 | 晨报提醒 | daily summary 提及 |
| 前1天 | 晨报预警 | — | — |
| 过期1天 | 晨报标红 + 提醒 | 晨报提及 | — |
| 过期3天+ | 晨报持续提醒直到完成/取消 | — | — |

检查 schedule.md 中已到期事项，写入当天摘要。P0 过期项醒目标注。

## 第4步：写入 memory/YYYY-MM-DD.md（幂等）

写入前检查文件中是否已存在 `## DeepSleep Daily Summary` 标题：
- 已存在 → 替换该章节
- 不存在 → 追加新章节

⚠️ **标题必须严格为 `## DeepSleep Daily Summary`**，不要变体。

### v3.0 摘要模板：
```markdown
## DeepSleep Daily Summary
<!-- dispatch_policy: active -->
<!-- pack_version: 3.0 -->

> Auto-discovered N active groups (24h). schedule.md: [items due / none].

### [群名1] <!-- chat:oc_xxx -->
- 🔴 战略级决策摘要
- 🟡 重要进展
- 🟢 常规记录

### [群名2] <!-- chat:oc_yyy -->
- 摘要...

### 🔗 跨群关联（如有）
- 群A ↔ 群B：关联描述

### 直接对话
- N 条 DM（不含具体内容）

### 🔮 Open Questions
- 问题1 [首次提出: MM-DD, 已悬挂 N 天]
- ⚠️ 问题2 [首次提出: MM-DD, 已悬挂 14 天 — 建议推进或搁置]

### 📋 Today (Next Day)
- 行动项（读者视角）
- 🔥 P0 到期：[schedule 中到期的 P0 事项]

### 待办
- [ ] 即时 action items
```

**静默日模板**（v3.0）：
```markdown
## DeepSleep Daily Summary
<!-- dispatch_policy: silent -->
<!-- pack_version: 3.0 -->
<!-- silent_days: N -->

> 静默日（过去24h无活跃对话）。延续自 YYYY-MM-DD。连续静默 N 天。

### [群名] <!-- chat:oc_xxx -->
- （延续自 YYYY-MM-DD，当日无新对话）

### 🔮 Open Questions
- 问题 [首次提出: MM-DD, 已悬挂 N 天]

### 📋 Today (Next Day)
- 搬运的未完成行动项

### 待办
- [ ] 搬运的未完成待办
```

⚠️ **关键**：每个群标题后必须带 `<!-- chat:oc_xxx -->` 注释。chat_id 从 session key 提取。

## 第4.5步：自检（必须执行！）
1. 每个群 `###` 标题是否都带有 `<!-- chat:oc_xxx -->` 注释？
2. chat_id 是否以 `oc_` 开头？
3. `dispatch_policy` 注释是否正确（active / silent）？
4. 重要度标注是否覆盖所有条目？
5. OQ 是否都标注了首次提出日期和悬挂天数？
6. 如有跨群关联，是否已写入 `### 🔗 跨群关联` 段落？

## 第5步：更新 MEMORY.md（隐私安全 + Guard Rail）

⚡ 只在有 🔴 P0 级别新信息时才更新。🟡🟢 级别的信息只保留在 daily file 中。

**Guard Rail**：
1. **只允许的操作**：
   - 在 `## Current Status` 更新日期和项目状态
   - 在已有项目段落末尾追加新进展
   - 新增全新的项目/技能段落
   - 更新 `## Preferences & Notes` 下的条目
   - 归档 15+ 天的 OQ 到 `## Open Questions (Archived)`
2. **禁止的操作**：
   - ❌ 删除任何已有段落
   - ❌ 改写已有的人物信息、配置、经验教训
   - ❌ 重组文件结构
   - ❌ 修改代码示例中的命令/参数
3. **Merge not append**：已有的原地更新，不追加重复

## 第6步：Pack+Dispatch 一体化执行（v3.0 新增）

⚠️ **v3.0 将 pack 和 dispatch 合并为单 cron**。Pack 完成后，直接在同一 session 中执行 dispatch。

Pack 写完 daily file 后，**立即读取 dispatch-instructions.md 并执行 dispatch 流程**。

这避免了：
- 两个 cron 的调度开销（省约 2-3 万 token 的 cron 启动开销）
- 时间窗口中 pack 失败但 dispatch 不知道的风险
- pack 产出的上下文已经在内存中，dispatch 不需要重新读取和理解

**执行 dispatch 时，跳过 dispatch-instructions.md 的第0步**（pack 已确认产出存在）。

## ⚠️ DM 隐私边界规则
1. `### 直接对话` 段落：只写"有 N 条 DM"
2. `### 🔮 Open Questions` 和 `### 📋 Today`：仅放群内产生的条目
3. 原则：daily summary 是公开广播，MEMORY.md 是私人日记
