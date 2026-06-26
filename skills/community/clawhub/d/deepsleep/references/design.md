# DeepSleep 设计文档

## 版本
- v2.0 (2026-03-29): 初始发布，三阶段架构
- v2.1 (2026-03-31): 7 项健壮性改进
- v2.2 (2026-04-01): Silent Day Carry-Forward + Decay 四级衰减
- v3.0 (2026-04-04): 9 项功能升级（统一 cron、静默快速路径、重要度分层、跨群关联、OQ 健康追踪、Schedule 优先级、记忆质量审计）

## 架构

纯 Agent tool-call 方案。无外部脚本依赖，全部通过 OpenClaw cron → isolated agentTurn → agent 读指令文件执行。

### v3.0 架构（单 cron 一体化）

```
23:50  cron "deepsleep" (unified)
         → agentTurn (isolated session, timeout 900s)
         → 读 pack-instructions.md
         │
         ├── PACK PHASE
         │   ├── 第-1步: 锁定日期（防 midnight 竞态）
         │   ├── 第0步: sessions_list → 活跃/静默判断
         │   │
         │   ├── [活跃日]
         │   │   ├── 第1步: sessions_history 并行拉取
         │   │   ├── 第2步: 筛选+摘要+重要度分层+跨群关联+OQ健康检查
         │   │   ├── 第3步: schedule 更新（优先级+去重）
         │   │   ├── 第4步: 写 daily file (dispatch_policy: active)
         │   │   ├── 第4.5步: 自检
         │   │   └── 第5步: 更新 MEMORY.md (仅P0, guard rail)
         │   │
         │   └── [静默日 — 快速路径, <5000 tokens]
         │       ├── 读最近 daily file
         │       ├── 按衰减级别 carry-forward
         │       └── 写 daily file (dispatch_policy: silent)
         │
         └── DISPATCH PHASE（第6步，同 session 直接执行）
             ├── 去重检查 dispatch-lock.md
             ├── 读 dispatch_policy
             ├── active → 智能发送决策（逐群判断是否有实质内容）
             ├── silent → 跳过发送，只更新快照
             ├── 快照 merge（按重要度分层保留 7/5/3 天）
             ├── 写发送日志
             └── 写锁文件

随时   Phase 3: Session Memory Restore
         → 群 session 收到消息时
         → 读 memory/groups/<chat_id>.md 恢复记忆
         → 优先加载 🔴P0 + 🟡P1
         → 检查跨群关联
         → 检查 schedule.md P0 到期项

每周日 Phase 4: Memory Quality Audit (可选)
         → 随机抽查 2-3 群的原始对话 vs 摘要
         → 检查遗漏、过度压缩、分类错误
         → 写 audit-log.md
```

### v2.x 架构（已弃用的双 cron 方案）

```
23:40  cron "deepsleep-pack"   → 写 daily file
00:10  cron "deepsleep-dispatch" → 读 daily file → 发送 → 写快照
```

**为什么合并？**
1. 两个 cron 各自要启动 isolated session、加载指令文件、理解上下文——重复的 2-3 万 token 开销
2. pack 产出的摘要已在内存中，dispatch 重新读取并理解是浪费
3. 分开带来的 timing gap（pack 失败但 dispatch 不知道）需要复杂的失败检测逻辑
4. 合并后 dispatch 可以直接用 pack 的上下文，更快更准确

## 关键设计决策

### 1. 纯 Agent，无 Python 脚本
早期设计过 Gemini 粗加工 + Claude 精加工的双 LLM 管道，但实测发现 agent 直接用 sessions_history tool 拉取 + 自行总结更简单可靠。

### 2. schedule.md 是唯一调度源
Markdown 表格，Key 列去重。v3.0 新增 Priority 列（P0/P1/P2），不同优先级有不同提醒策略。

### 3. 隐私隔离
每群只收到自己的摘要。跨群关联只提及话题关键词，不暴露另一群的具体对话。DM 内容只进 MEMORY.md。

### 4. 幂等性
Pack 检查 daily file 是否已有 DeepSleep 章节（存在则替换）。Dispatch 通过 lock 文件防重复。

### 5. dispatch_policy 标记（v3.0 新增）
Pack 在 daily file 中设置 `<!-- dispatch_policy: active|silent -->`，dispatch 据此决定是否发送晨报。这解耦了"pack 判断"和"dispatch 执行"，让逻辑更清晰。

### 6. 记忆重要度分层（v3.0 新增）
🔴P0 战略决策、🟡P1 重要进展、🟢P2 常规记录。不同级别在快照中保留不同天数（7/5/3天），Phase 3 加载时优先加载高优。

**为什么？** 之前所有记忆"平等"对待，但"Jeffrey 决定用 910B 架构"和"讨论了一下 Moltbook 帖子"的重要度天差地别。分层后 token 使用更高效，关键记忆保留更久。

### 7. 跨群关联（v3.0 新增）
扫描所有群的摘要关键词，检测重叠话题。只提示关联关系，不泄露具体内容。

**为什么？** 视频训练实验室和千问微调群讨论相关话题时，agent 在一个群里只有该群的上下文，错失了整合信息的机会。

### 8. OQ 健康追踪（v3.0 新增）
每个 OQ 标注首次提出日期和悬挂天数。7天⚠️、14天建议升级/搁置、30天归档。

**为什么？** 之前 OQ 永不过期导致"僵尸 OQ"堆积。有些问题已经不再重要但一直占着快照空间。

### 9. 智能发送决策（v3.0 新增）
不是每个群都需要每天收到晨报。只有真正有内容/有 P0 到期/有 stale OQ 的群才收到消息。

**为什么？** 连续静默日发"没事发生"的晨报是噪音。群成员会习惯性忽略，降低有效信息的关注度。

### 10. 记忆质量审计（v3.0 新增）
每周抽查：拉原始对话 vs 看 pack 摘要，检查遗漏和误分类。

**为什么？** Pack 的摘要质量完全是 LLM 黑盒。没有反馈环就无法持续改进。审计结果可以反哺到 pack 的 filtering 逻辑。

## v3.0 改进清单

| # | 优先级 | 问题 | 方案 |
|---|---|------|------|
| 1 | 🔴 P0 | 静默日浪费 5-8 万 token 拉无用历史 | 静默日快速路径：不拉 history，仅文件搬运 |
| 2 | 🔴 P0 | 静默日晨报是噪音 | dispatch_policy:silent 时不发消息 |
| 3 | 🟡 P1 | 两个 cron 浪费启动开销 | 合并为单 cron，pack+dispatch 同 session |
| 4 | 🟡 P1 | OQ 永不过期导致僵尸堆积 | OQ 健康追踪：7d⚠️ / 14d升级 / 30d归档 |
| 5 | 🟡 P1 | 所有记忆平等对待浪费 token | 重要度分层 P0/P1/P2，不同保留窗口 |
| 6 | 🟡 P2 | 跨群信息割裂 | 跨群关联检测，话题级别提示 |
| 7 | 🟡 P2 | Schedule 无优先级 | P0/P1/P2 + 差异化提醒频率 |
| 8 | 🟢 P3 | 摘要质量无反馈 | 每周质量审计 Phase 4 |
| 9 | 🟢 P3 | 对话结束→pack 延迟最长 24h | (考虑中) mini-pack 触发机制 |

### 关于第 9 项（对话密度触发 mini-pack）的思考

v3.0 暂不实现。原因：
1. 需要持续监控对话密度，要么在 heartbeat 中做（增加 heartbeat 复杂度），要么加新 cron（违背精简原则）
2. Phase 3 已经能在群消息到来时加载快照，mini-pack 的增量价值有限
3. 如果真正需要"实时记忆"，应该用不同的架构（如 write-ahead log），而不是在 pack 上打补丁

**未来方向**：如果需求明确，可以考虑在 heartbeat 中加一个轻量检测——"距上次 pack 已过 N 小时 + 期间有 M 条新消息 → 触发 mini-pack"。但目前 23:50 的每日 pack 已经足够。

## 运行时文件

```
memory/
├── YYYY-MM-DD.md          # 每日摘要（pack 产出，含重要度+跨群关联）
├── schedule.md            # 中长期任务（Key 去重 + P0/P1/P2 优先级）
├── dispatch-lock.md       # dispatch 去重锁
├── dispatch-log.md        # dispatch 发送日志（含 send/skip 统计）
├── audit-log.md           # 每周质量审计日志（v3.0 新增）
├── groups/
│   ├── <chat_id>.md       # 每群记忆快照（🔴7d/🟡5d/🟢3d 分层保留）
│   └── ...
```

## Token 经济性对比

| 场景 | v2.1 | v3.0 | 节省 |
|---|---|---|---|
| 活跃日 pack | ~8万 | ~6万 | -25%（重要度过滤减少输出） |
| 活跃日 dispatch | ~3万 | 0（同 session） | -100% |
| 静默日 pack | ~8万 | <0.5万 | -94% |
| 静默日 dispatch | ~3万 | ~0.2万 | -93% |
| **日均（50% 静默率）** | **~11万** | **~3.4万** | **-69%** |

## 已废弃

`references/archived/` 下的 Python 脚本是 v1.x 方案残留：
- `sleep_phase.py` — Gemini API 总结
- `wake_phase.py` — 晨醒消息 JSON
- `extract_conversations.py` — JSONL 提取
- `schedule_engine.py` / `schedule.json` — 旧调度器

v2.x 的双 cron 配置（deepsleep-pack + deepsleep-dispatch）已被 v3.0 的单 cron 替代。
