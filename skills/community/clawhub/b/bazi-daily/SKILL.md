---
name: bazi-daily
description: 面向“今日运势/今天适合做X吗/今日宜忌”类咨询的八字日运解读技能。使用场景：用户在 OpenClaw 中询问当日运势、某事项是否适合今天做、今日吉凶与建议时触发。技能会自动读取当前日期，查询当日对应的流年、流月、流日，并结合用户的八字四柱进行分析；若用户为首次使用且无个人四柱记忆，先引导用户提供四柱并写入长期记忆，后续复用无需重复询问。
---

# Bazi Daily

## Knowledge Source Architecture (Mandatory)

将经典分为三个独立知识源，禁止混成单一“综合库”：

- A.《滴天髓》库（原则层）：用于“为什么”和方向性判断（气机、取用总纲、论命哲学）。
- B.《渊海子平》库（结构层）：用于格局判定、十神结构、用神框架（先定结构再谈细节）。
- C.《穷通宝鉴》库（调候层）：用于月令气候、寒暖燥湿与调候药方（对结构结论做气候校正）。

固定来源文件（仅使用本地 txt）：
- `A.滴天髓`：`references/classics/A_滴天髓.txt`
- `B.渊海子平`：`references/classics/B_渊海子平.txt`
- `C.穷通宝鉴`：`references/classics/C_穷通宝鉴.txt`

若 txt 文件不可读，直接报错"经典文本文件缺失，无法完成分析"，不得尝试其他路径。

> **当前文本覆盖缺口警告**：`B_渊海子平.txt` 缺少格局判断核心章节（成格/破格/从格/化格），`C_穷通宝鉴.txt` 缺少约 40% 天干的调候章节（乙木完整版、丁火、戊土、己土、庚金、辛金、癸水）。在涉及上述缺失内容时，输出中必须注明"当前文本节选，[B-结构]/[C-调候] 依据不完整"，不得以模型内置知识静默替代。详见 [references/classics/README.md](references/classics/README.md)。

调用顺序必须是：`B 结构 -> C 调候 -> A 解释`。
路由细则见 [references/classic-sources-routing.md](references/classic-sources-routing.md)。

## Workflow

1. 识别触发意图。
2. 从会话上下文提取 `user_id` 与 `user_timezone`。
3. 以用户时区自动计算 `today_local`（`YYYY-MM-DD`）。
4. 调 heartbeat `bazi_profile_get` 读取用户四柱档案。
5. 若未命中四柱档案，请用户补充四柱并调 heartbeat `bazi_profile_upsert` 写入长期记忆。
6. 根据 `today_local` 查询 `bazi_daily_calendar`。
7. 按“五步编排”完成分析并输出结论、依据和建议。

默认年度数据源文件：`assets/bazi_daily_calendar_2026.sql`。
导入脚本：`scripts/import_bazi_calendar.py`。
经典文本预处理脚本：`scripts/extract_classics_text.py`。

## Five-Step Orchestration (Mandatory)

在通过日期与流运查询闸门后，必须按以下步骤执行：

1. `step1 解析命盘`
   - 提取四柱、十神分布、日主强弱初判、月令、格局候选（可多候选）。
2. `step2 结构优先（渊海子平）`
   - 用 B 库先判结构与格局成立条件，给出主格/兼格与用神框架。
3. `step3 调候校正（穷通宝鉴）`
   - 用 C 库对寒暖燥湿做修正，必要时覆盖或微调 step2 的用神次序。
4. `step4 气机解释（滴天髓）`
   - 用 A 库解释最终结论背后的气机逻辑，使结论成体系、可说明。
5. `step5 输出`
   - 输出“结论 + 依据 + 建议”，并标明依据来自 A/B/C 哪一类规则。

## Mandatory Pre-Analysis Gates

每次输出运势分析前，必须先完成以下两个步骤：
1. 获取当前日期：基于 `user_timezone` 计算 `today_local`（`YYYY-MM-DD`）。
2. 查询数据表：使用 `today_local` 查询 `bazi_daily_calendar` 以获取 `flow_year`、`flow_month`、`flow_day`。

未完成以上两个步骤时，禁止进入“运势结论/宜忌建议”输出。

## Trigger Phrases

将下列表达视为高优先级触发：
- “今日运势”
- “今天适合 xxx 吗？”
- “今天宜做什么/忌做什么？”
- “我今天的运气怎么样？”
- “帮我看今天的八字运势”

若用户没有显式说“八字”，但语义是“今天是否适合某事”，默认按本技能流程处理。

## First-Time Onboarding

当找不到用户四柱记忆时：
1. 明确告知需要四柱后才能进行个性化日运分析。
2. 请用户直接提供四柱，格式优先：`年柱/月柱/日柱/时柱`。
3. 若用户不清楚四柱，建议前往“万年历”查询：<https://wannianrili.bmcx.com/>，输入生日后获取四柱再回传。
4. 校验四柱完整性与格式：四项都存在且非空，且每柱须为有效干支组合（2 个汉字，第 1 字为十天干，第 2 字为十二地支）；格式不合法时要求用户重新输入，不得写入。
5. 调 heartbeat `bazi_profile_upsert` 将结构化结果写入长期记忆。
6. 写入成功后继续本次分析，不要求用户重新提问。

长期记忆建议键：
- `bazi_profile.pillars.year`
- `bazi_profile.pillars.month`
- `bazi_profile.pillars.day`
- `bazi_profile.pillars.hour`
- `bazi_profile.source`（如 `user_provided`）
- `bazi_profile.updated_at`（UTC 时间，格式 `YYYY-MM-DDTHH:mm:ssZ`）

若用户后续主动更正四柱，以最新输入覆盖旧值。

heartbeat 请求响应与错误码约定见 [references/heartbeat-contract.md](references/heartbeat-contract.md)。

## Date And Lookup Rules

1. 自动读取当前日期，禁止要求用户手动输入日期。
2. 优先使用会话上下文中的 `user_timezone` 计算当日日期。
3. 若 `user_timezone` 缺失，回退 `Asia/Shanghai` 并记录 `timezone_fallback=true`。
4. 查询数据表时使用标准日期键（`YYYY-MM-DD`），即 `today_local`。
5. 期望查得字段：`flow_year`、`flow_month`、`flow_day`。
6. 若当天无记录，明确告知“缺少当日流运数据”，并仅给出有限建议，不伪造结果。
7. 每次运势分析请求都必须执行一次日期计算与一次数据表查询，不得跳过。

8. 当前内置日历数据为 `assets/bazi_daily_calendar_2026.sql`，从 `2026-03-03` 起覆盖至 2026 年末。年度结束或数据缺口期间，除”缺少当日流运数据”提示外，额外提示”请联系管理员更新年度日历数据”。
9. 年度日历更新流程：准备新年度 xlsx → 运行 `scripts/import_bazi_calendar.py` 生成 SQL → 导入 OpenClaw 内置表（详见 `references/import-command-template.md`）。新数据应至少在年度切换前 30 天就绪。

数据表字段约定见 [references/bazi-calendar-schema.md](references/bazi-calendar-schema.md)。
数据文件导入规范见 [references/bazi-calendar-schema.md](references/bazi-calendar-schema.md) 中的 “Data Source File” 与 “Import Mapping”。
导入命令模板见 [references/import-command-template.md](references/import-command-template.md)。

## Analysis Rules

1. 结构判定优先级高于主观经验；先判“是否成格/破格”，再谈强弱喜忌。
2. 调候可修正结构结论，但不可跳过结构直接给药方。
3. 解释层必须回扣气机，不得只给“吉/凶”标签。
4. 明确区分三类依据：
- 结构依据（B《渊海子平》）
- 调候依据（C《穷通宝鉴》）
- 原理依据（A《滴天髓》）
5. 先给“今日总体倾向”，再回答用户具体问题，再给“宜/忌”。
6. 输出“宜”与“忌”各 2-4 条，保持可执行。
7. 避免绝对化、宿命化表达；用“倾向/建议”措辞。

## Evidence Tagging Rules

每条关键结论至少绑定一个来源标签：

- `[B-结构]`：格局、十神结构、用神框架判断。
- `[C-调候]`：寒暖燥湿、月令气候修正。
- `[A-原理]`：气机方向、总纲解释。

若三源结论冲突，按优先级处理并显式说明：
1. 先保留 `B` 的结构边界；
2. 再用 `C` 做季节性校正；
3. 最后用 `A` 解释“为何这样取舍”。

## Failure Handling

1. heartbeat 读取失败时，按“未知档案”处理并进入首次引导；同时提示“记忆服务暂不可用，本次可先临时分析”。
   若用户不清楚四柱，补充推荐“万年历”：<https://wannianrili.bmcx.com/>。
2. heartbeat 写入失败时，继续使用用户本次输入完成分析；同时提示“本次已解读，但暂未保存，下次可能需要再次提供”。
3. 当日流运缺失时，明确告知“缺少当日流运数据，仅基于四柱给出有限建议”；该提示必须建立在“已执行当日查询且未命中”之上。

## Response Template

按以下顺序组织回答：
1. 今日日期（`YYYY-MM-DD`）
2. 当日流运（流年/流月/流日）
3. 命盘摘要（十神/强弱初判/月令/格局候选）
4. 结构结论（`[B-结构]`）
5. 调候校正（`[C-调候]`）
6. 气机解释（`[A-原理]`）
7. 对用户提问的直接结论
8. 今日“宜”列表（2-4 条）
9. 今日“忌”列表（2-4 条）
10. 一句风险提示（非决定性，仅供参考）

## Guardrails

- 不编造缺失的四柱与流运数据。
- 不编造经典原文；如记忆不确定，改用“原则性转述”并标注“意译”。
- 不输出医疗、法律、投资等确定性结论。
- 用户未提供时柱时，不自动推断；要求补全。
- 禁止跳过 `B->C->A` 顺序直接下结论。

## Mandatory Logging Fields

每次请求**必须**记录以下字段，用于排障与 UAT 复盘：
- `user_id`
- `user_timezone`
- `today_local`
- `timezone_fallback`
- `memory_hit`
- `calendar_hit`
- `heartbeat_get_status`
- `heartbeat_upsert_status`
- `structure_source_hit`（B）
- `climate_source_hit`（C）
- `principle_source_hit`（A）
- `final_yongshen_framework`
- `climate_adjustment_applied`

上述字段不得省略；若某字段在当次请求中不适用（如首次引导无 `heartbeat_upsert_status`），记录为 `null`。

## UAT Cases

1. 首次用户输入“今日运势”，期望：要求四柱 -> heartbeat 写入成功 -> 返回完整解读。
2. 同一用户再次输入“今天适合谈合作吗？”，期望：不再询问四柱，直接返回结论与宜忌。
3. 用户时区为 `Asia/Shanghai`，在 00:05 与 23:55 测试，期望：`today_local` 与用户本地日期一致。
4. 构造当日无流运记录，期望：输出缺失提示，不编造流年流月流日。
5. 模拟 heartbeat upsert 失败，期望：本次照常解读，附“未保存”提示。
6. 模拟 heartbeat get 失败，期望：进入首次引导，流程不断。
7. 构造“结构与调候结论不一致”案例，期望：输出中明确展示 `B->C->A` 取舍链路。
8. 检查回答文本，期望：关键结论至少各含一个 `[B-结构]/[C-调候]/[A-原理]` 标签。
