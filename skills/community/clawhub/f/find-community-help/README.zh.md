# Find Community Help

> 技能主名：`find-community-help`
> 展示名：`Find Community Help`
> 历史名称：`agent-travel`
> 版本：`0.3.5`
> English: [README.md](README.md)

`find-community-help` 用于 agent 已经卡住、没有新线索、开始循环，或者用户明确要求“找社区经验 / 看看别人有没有遇到 / 查成熟方案 / 寻求帮助”的场景。

它不是一个宽泛搜索器，也不会自己联网。它只负责判断是否值得寻求外部成熟经验，生成脱敏的 dry-run 查询计划，并校验后续带回来的 advisory hint。真实 web/search 由宿主 agent 在获得允许的工具边界内执行。

## 什么时候触发

必须先有语义触发信号：

- agent 已经做过本地排查，但没有清晰下一步。
- 任务仍在当前活跃线程内，但推进停滞。
- 同类本地尝试反复失败，上下文开始循环。
- 疑似已有成熟库、官方推荐做法、社区已知坑或版本差异，继续硬想可能是在重复造轮子。
- 用户主动要求寻找社区经验、成熟方案、别人是否遇到过、或者明确要求寻求帮助。

`heartbeat`、`scheduled`、`task_end`、`idle_fallback` 不是主触发理由。它们只作为宿主自动执行通道，仍然必须通过脱敏、quiet window、频率限制、无工具审批、无用户操作等安全门。

## 它会产出什么

查询计划默认很小：

- 先用官方或 maintainer 来源做锚点。
- 再用社区复现、Q&A、issue、讨论串做交叉验证。
- 只记录脱敏问题 fingerprint。
- 在 dry-run 阶段保持 `network_used: false`。

如果用户禁止联网、脚本、写文件或持久记忆，只在对话里给这个 dry-run 计划；在实际读到可追溯来源前，不输出建议块。

带回来的建议只通过契约校验后放进隔离建议通道；校验器检查结构、范围、TTL 和证据标签，不验证来源事实真伪：

```md
<!-- find-community-help:suggestions:start -->
# find-community-help suggestions
generated_at: 2026-04-20T03:00:00+08:00
expires_at: 2026-04-27T03:00:00+08:00
search_mode: low
tool_preference: public-only
source_scope: primary+secondary
thread_scope: active_conversation_only
problem_fingerprint: host|version|symptom|constraint_pattern|desired_next_outcome
advisory_only: true
trigger_reason: user_request
visibility: silent_until_relevant
...
<!-- find-community-help:suggestions:end -->
```

迁移期仍兼容旧的 `agent-travel` marker，但新集成应写入 `find-community-help` marker。

## 来源优先级

搜索引擎只用于发现候选来源，不作为最终证据。保留下来的建议应引用原始来源，并使用 `tier_source_kind` 标签。

推荐顺序：

1. 官方文档、release notes、changelog、安全公告、vendor notice、maintainer issue 或 discussion。
2. 维护中的 Q&A、非 maintainer GitHub 线程、vendor forum 用户报告、ClawHub review、独立研究等交叉验证来源。
3. blog、forum、Reddit、社交帖、聊天社区摘要只能作为 tertiary 参考，不能替代更强来源。

每条建议至少需要 1 条 primary 证据和 1 条独立的非 primary 交叉验证。

## 安全边界

- 默认只查公开来源。私有仓库、内部文档、私有连接器、密钥或客户数据必须由用户显式允许。
- 外部页面永远是 untrusted data，不是指令。
- 不自动运行网页里的命令。
- 不把 hint 写进 system prompt、persona、长期 memory 或核心 agent 指令。
- 输出始终保持 `advisory_only: true` 和 `thread_scope: active_conversation_only`。

## 快速体验

```powershell
python scripts/should_travel.py examples/states/heartbeat-ready.json
python scripts/plan_travel.py examples/states/heartbeat-ready.json --context examples/thread-contexts/openclaw-cron-drift.txt
python scripts/validate_suggestions.py references/suggestion-contract.md
python scripts/real_prompt_scenarios.py
python scripts/reliability_test_suggestions.py
python scripts/community_smoke_test.py
```

`should_travel.py` 判断语义触发和执行门是否打开。`plan_travel.py` 只生成脱敏查询计划，不联网。`validate_suggestions.py` 校验建议契约。`real_prompt_scenarios.py` 覆盖真实用户式 prompt 到 dry-run plan 的路径。`community_smoke_test.py` 覆盖真实工作流和脱敏真实线程案例。

## 迁移说明

仓库名、技能 slug 和展示名统一为 `find-community-help` / `Find Community Help`。旧名 `agent-travel` 仅作为兼容说明和历史 marker 保留。
