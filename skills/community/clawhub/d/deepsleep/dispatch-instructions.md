# DeepSleep 阶段二：晨报分发指令（v3.0）

⚠️ **时间预算：10 分钟。高效执行。**

> **v3.0 变更**：正常运行时 dispatch 由 pack 在同一 session 中直接调用（见 pack-instructions.md 第6步）。本文件仍保留独立 dispatch 的完整指令，用于：
> - pack 失败后的独立补救运行
> - 手动触发 dispatch
> - 理解 dispatch 完整逻辑

## 第-1步：去重检查（防重复发送）
检查 `~/clawd/memory/dispatch-lock.md`：
1. 读取文件内容
2. 如果日期 = 目标日期 → **已发过，直接退出**
3. 如果文件不存在或日期不匹配 → 继续执行

锁文件在**所有发送完成后**写入（非开始前），确保崩溃可重跑。

## 第0步：检查 pack 产出（失败恢复）
读取 `~/clawd/memory/YYYY-MM-DD.md`（目标日期）。

**如果 pack 失败（文件不存在或无 `## DeepSleep Daily Summary`）**：
1. `sessions_list(kinds=['group','main'], activeMinutes=1440, messageLimit=1)` 发现活跃群
2. 对每个群 `sessions_history(sessionKey=<key>, limit=30)` 拉取精简历史（并行）
3. 生成精简版摘要写入 daily file（模板同 pack-instructions.md）
4. 继续正常的第1-4步

> 当 dispatch 被 pack 在同一 session 中调用时，跳过此步。

## 第1步：读取目标日期的摘要
读取 `~/clawd/memory/YYYY-MM-DD.md`。

### 📋 检查 dispatch_policy
解析摘要中的 `<!-- dispatch_policy: xxx -->` 注释：
- `active` → 正常发送晨报
- `silent` → **跳过第2步的消息发送，直接进入第3步更新快照**

如果找不到 dispatch_policy 注释（旧版 pack 产出），默认为 `active`。

## 第1.5步：解析群映射
从摘要的 `### 群名 <!-- chat:oc_xxx -->` 注释提取每个群的 chat_id。
注释缺失时，查阅兜底映射文件：
```
read(file="~/clawd/skills/deepsleep/chat-id-mapping.local.md")
```

## 第2步：发送每群晨报（仅 dispatch_policy=active 时执行）

### 📊 智能发送决策（v3.0 新增）
不是所有群都需要收到晨报。逐群判断：

| 条件 | 是否发送 |
|---|---|
| 群有新的实质对话内容 | ✅ 发送 |
| 群无新对话，但有 P0 到期事项 | ✅ 发送（仅含提醒） |
| 群无新对话，有 OQ 悬挂 ≥7 天 | ✅ 发送（含 ⚠️ OQ 提醒） |
| 群无新对话，无到期事项，OQ 都在正常悬挂范围 | ❌ 不发送（只更新快照） |

对决定发送的群，用 `message(action='send', channel='feishu', target='chat:<chat_id>')` 发送：

```
📋 昨日工作小结（YYYY-MM-DD）

[该群专属摘要]

🔗 关联提示：[如有跨群关联，附上简短提示]

🔮 Open Questions
- 问题 [已悬挂 N 天]
- ⚠️ 问题 [已悬挂 14 天 — 建议推进]

📋 今日待办
- 行动项
- 🔥 P0 到期：[到期事项]
```

⚠️ **视角规则**：
- 摘要 = "**昨天**做了什么"（过去时）
- 待办 = "**今天**要做什么"（将来时）
- ❌ 不写"今天做了什么 / 明天要做什么"

⚠️ **隐私**：每个群只收到自己的摘要。不跨群，不含 MEMORY.md 私人信息。跨群关联只提示话题关联，不暴露另一群的具体对话内容。

## 第3步：检查 schedule.md
读取 `~/clawd/memory/schedule.md`，找今天到期的事项。

### 到期提醒分级（v3.0 新增）
- **P0 到期/过期**：在相关群的晨报中标 🔥，Phase 3 中也主动提醒
- **P1 到期**：在晨报中提及
- **P2 到期**：仅在 daily summary 中记录
- **P0 过期 3 天+**：每天持续提醒直到完成或手动取消

## 第4步：生成每群记忆快照 — 滚动 Merge + 重要度

**这一步决定了 agent 明天是否还有记忆。没有快照 = 明天失忆。**

### Merge 算法（v3.0 增强）
对每个群：
1. 读取现有快照 `~/clawd/memory/groups/<chat_id>.md`
2. 读取 daily summary 中该群的段落
3. Merge 规则：
   - **🔴 P0 条目**：保留最近 **7 天**（战略决策需要更长记忆）
   - **🟡 P1 条目**：保留最近 **5 天**
   - **🟢 P2 条目**：保留最近 **3 天**
   - **静默日延续条目**：不计入窗口，直到 OQ/待办解决才清除
   - **Open Questions**：保留所有未解决的（永不过期），标注首次提出日期和悬挂天数
   - **待办 `- [ ]`**：永不过期；`- [x]` 完成超过 3 天的清除
4. **跨群关联提示**：如果该群有关联群，在快照末尾附注

### 静默日快照处理（dispatch_policy=silent 时）
- **不清除现有快照进展条目**
- 只更新时间戳 + 静默天数标注
- 保留所有 OQ 和未完成待办
- 15+ 天静默：不更新快照文件

### 快照格式（v3.0）：
```markdown
# [群名] 近期记忆
> 更新时间：YYYY-MM-DD HH:MM
> 连续静默 N 天，最后活跃：YYYY-MM-DD（仅静默日）

## 最近进展
- 🔴 [YYYY-MM-DD] 战略决策...（保留7天）
- 🟡 [YYYY-MM-DD] 重要进展...（保留5天）
- 🟢 [YYYY-MM-DD] 常规记录...（保留3天）

## 🔮 Open Questions
- 问题1 [首次: MM-DD, 悬挂 N 天]
- ⚠️ 问题2 [首次: MM-DD, 悬挂 14 天]

## 📋 待办
- [ ] 未完成待办
- [x] 已完成（3天后清除）

## 🔗 关联群
- ↔ [关联群名]：关联话题描述
```

⚡ 并行写入多个群的快照文件。

## 第5步：写入发送日志
追加到 `~/clawd/memory/dispatch-log.md`：

```markdown
## YYYY-MM-DD HH:MM
- 目标日期：YYYY-MM-DD
- dispatch_policy：active / silent
- 发送群数：N（活跃 M / 跳过 K）
- 成功：[群名1, 群名2, ...]
- 跳过：[群名3（无新内容）, ...]
- 失败：无 / [群名4（原因：xxx）]
- 快照更新：N 个文件
- 锁文件：已写入
- 耗时：约 Xs
- 一体化模式：是/否（pack 同 session 调用）
```

滚动保留最近 30 条。

## 第6步：写入 dispatch-lock.md
```
write(file="~/clawd/memory/dispatch-lock.md", content="YYYY-MM-DD")
```

## 群名与 chat_id 映射（兜底）
优先从摘要的 `<!-- chat:oc_xxx -->` 注释解析。
兜底：`read(file="~/clawd/skills/deepsleep/chat-id-mapping.local.md")`
最后手段：从 `sessions_list` 的 session key 中提取。
