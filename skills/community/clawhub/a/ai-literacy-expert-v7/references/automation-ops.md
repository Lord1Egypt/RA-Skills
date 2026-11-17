# 持续运营自动化工作流（V7.0 · L4 调度驱动型）

> V7.0 把 V6.0 的「运营流设计图纸」升级为「**可注册、可无人值守、跨会话续跑、幂等不重复、留痕可审计**」的真实自动化任务。
>
> **调度契约（必读）**：`references/automation-l4-scheduler.md`
> **指令模板**：`assets/self-contained-prompt-template.md`
> **任务台账**：`assets/automation-registry.json` ｜ **执行台账**：`assets/run-ledger-template.jsonl`
>
> **运行假设**：触发调度由宿主提供（WorkBuddy 调度系统 + `automation-task-manager`）；本技能负责**流程编排、状态推进与内容生成**。automation 会话内**严禁**加载 `automation-task-manager`。

---

## 总览：六类运营流（覆盖全部模块 × 六大能力）

| 流 | 触发（cron） | 产出 | 落点 | 覆盖模块 | 覆盖能力 |
|----|------|------|------|----------|----------|
| **OPS-1** 新生 4 周上手自动驾驶 | 每周一 08:00 `0 0 8 * * 1` | 每周课件+游戏+自测+周计划 | 日历+闹钟+IMA+腾讯文档 | E·N + A/B/C/D | 课件·游戏·备课·评估 |
| **OPS-2** 每日 AI 速递 | 工作日 08:30 `0 30 8 * * 1-5` | 1 篇前沿速递 + 1 道练习题 | IMA→腾讯文档→备忘录 | G | 课件 |
| **OPS-3** 考前复习自动提醒 | 考前 1 天 19:00（once） | 复习清单 + 闹钟 + 自测题 | 闹钟+备忘录+IMA | 已完成模块( A→G ) | 评估 |
| **OPS-4** 教研组周报 | 每周五 17:00 `0 0 17 * * 5` | 本周备课/评估/协作汇总 | 腾讯文档→分享→备忘录 | A→G | 协作·评估 |
| **OPS-5** 模块轮转课件 ⭐新增 | 每周三 10:00 `0 0 10 * * 3` | 按 A→G+E·N 轮转产出课件/游戏 | IMA+预览+腾讯文档 | **A→G + E·N 全模块** | 课件·游戏 |
| **OPS-6** 学习进度周检与补学回流 ⭐新增 | 每周日 20:00 `0 0 20 * * 0` | 自测+薄弱点诊断+补学建议/课件 | IMA+备忘录+日历 | A→G | 评估·推荐·课件 |

> **覆盖结论**：A、B、C、D、E、E·N、F、G **全部模块**与**六大能力**均已被至少一条运营流覆盖并可被调度 → 达成 L4「全模块全功能自动化」。

---

## 通用执行骨架（所有 OPS 共用）

每个 OPS 在 automation 会话中执行时，都走同一套骨架：

```
① 读状态（IMA《AI教学·自动化状态》→ 该 OPS 节点的 cursor / lastRun）
② 算幂等键（idempotency_key = "<OPS-x>:<周期标识>"）→ 查台账
   ├─ 命中 success → 记 skipped 后退出（不重复产出）
   └─ 未命中     → 继续
③ 执行（复用 V6.0 的 BUILD / VERIFY / DELIVER / REPORT / LEARN）
④ 回写状态（cursor 推进、lastRun 更新）
⑤ 追加台账（JSONL 一行）
⑥ 失败 → 记 failed + 备忘录告警 + 退出码 0（不阻塞调度）
```

---

## OPS-1 · 新生 4 周 AI 上手自动驾驶（⭐ BNBU/SAI 旗舰流）

**来源**：`module-e-bnbu-sai.md`「4 周 AI 实战上手加速包」+ 博智坊六期主题。
**状态推进**：`cursor.week` 1→4（W1 大模型基础 / W2 Vibe Coding / W3 AIGC / W4 3D重建&CV）。

### 编排
```
T0（一次性，可选）：开班日建 4 周日历课表 + IMA 落库 + 设每周一推进提醒
每周一 08:00（调度触发）：
  读 cursor.week → 生成本周包（课件1 + 游戏1 + 自测1 + 周计划）
  → VERIFY（课件/游戏跑 harness，预算 ≤3）
  → DELIVER（日历排课 + 闹钟 + IMA + 腾讯文档周包）
  → 回写 cursor.week += 1
W4 末：综合测评 → LEARN 输出「上手认证达标评估」→ 腾讯文档结课报告 → 自动停用本任务
```

### 注册命令（须先向用户展示预览并获确认）
```bash
cd ~/.codebuddy/skills/automation-task-manager
./scripts/scheduler-api.sh create \
  --name "AI教学·BNBU新生4周上手自动驾驶" \
  --cron "0 0 8 * * 1" \
  --frequency-type "daily" \
  --timeout 900 --retry-count 2 \
  --description "OPS-1 · V7.0：每周一 08:00 推进一周 AI 上手包（课件+游戏+自测+周计划）" \
  --prompt "$(cat /tmp/ops1-prompt.txt)"
```

`/tmp/ops1-prompt.txt`（按自包含模板填充，可直接使用）：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/automation-ops.md、references/module-e-bnbu-sai.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-1 · 推进 BNBU/SAI 新生 4 周 AI 上手计划的本周包。
【状态】读 IMA《AI教学·自动化状态》OPS-1 节点 cursor.week（初值 1）。主题：W1大模型基础/W2 Vibe Coding/W3 AIGC/W4 3D重建与CV。若 week>4 则生成结课测评后停用本任务并结束。
【幂等】key = "OPS-1:<ISO周 如2026-W35>"；台账命中 success → 记 skipped 退出。
【执行】1.按本周主题生成课件HTML(1)+游戏HTML(1)+自测题(1套)+周计划 2.课件/游戏运行 playwright-control-test-harness.js 实测，未过则修复，预算≤3 3.达标后分发。
【验证】harness 退出码必须为 0；未过且超预算 → 降级(仅分发已通过部分)+记 failed 明细。
【落点】日历排本周课表 + 闹钟提醒 + IMA 落库 + 腾讯文档《AI上手·第N周》周包。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts,cursor:{week:N+1}} 并回写 cursor.week。
【失败】台账记 failed + 备忘录告警 + 退出码 0，不自行重试。
```

---

## OPS-2 · 每日 AI 速递（保持前沿敏感度）

**状态推进**：`cursor.issue` 递增（期号）。

### 编排
```
触发 → 检索 IMA「本周 AI 新发展」(G 模块素材)
     → 生成 1 篇 300 字速递（标注来源与日期）+ 1 道配套练习题（关联最近已学模块）
     → VERIFY（速递无事实硬伤、题目可答且答案唯一）
     → DELIVER（腾讯文档《AI每日速递》追加 + IMA 落库 + 可选备忘录）
     → 回写 issue += 1
```

### 注册命令（须先预览确认）
```bash
./scripts/scheduler-api.sh create \
  --name "AI教学·每日AI速递" \
  --cron "0 30 8 * * 1-5" \
  --frequency-type "daily" \
  --timeout 900 --retry-count 2 \
  --description "OPS-2 · V7.0：工作日 08:30 生成 1 篇 AI 前沿速递 + 1 道练习题" \
  --prompt "$(cat /tmp/ops2-prompt.txt)"
```

`/tmp/ops2-prompt.txt`：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/module-g-latest-developments.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-2 · 生成 1 篇 AI 前沿速递(约300字)+1 道配套练习题。
【状态】读 IMA《AI教学·自动化状态》OPS-2 节点 issue（初值 1）。
【幂等】key = "OPS-2:<今天 YYYY-MM-DD>"；台账命中 success → 记 skipped 退出。
【执行】1.检索 IMA 知识库本周 AI 新发展素材(G模块) 2.生成300字速递，标注来源与日期 3.生成1道单选题(关联最近已学模块)+答案与解析 4.核对事实与答案唯一性。
【验证】速递事实可核、无硬伤；题目有且仅有一个正确项。（本任务无 HTML 产物，不需 harness）
【落点】追加腾讯文档《AI每日速递》当日章节 + IMA 落库 + 可选备忘录「今日一题」。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts,cursor:{issue:N+1}} 并回写 issue。
【失败】台账记 failed + 备忘录告警 + 退出码 0，不自行重试。
```

---

## OPS-3 · 考前复习自动提醒（评估闭环的守门员）

**类型**：`once`（按实际考试日期填写 cron）；可由 OPS-1 或用户设的考试日历引发。

### 编排
```
触发(考前 1 天 19:00) →
  读「已完成模块」→ 生成复习清单 + 抽取 10 道自测题(Runbook D 简化)
  → DELIVER：① 闹钟「考前复习」② 备忘录「复习清单+自测链接」③ IMA 存自测题
  → 考试后：自动 RUN Runbook D 测评 → LEARN 回流薄弱点
```

### 注册命令（once · 须先预览确认；cron 按实际考试日期调整）
```bash
./scripts/scheduler-api.sh create \
  --name "AI教学·考前复习提醒" \
  --cron "0 0 19 14 1 *" \
  --frequency-type "once" \
  --effective-start "2026-01-14" --effective-end "2026-01-14" \
  --timeout 300 --retry-count 3 \
  --description "OPS-3 · V7.0：考前 1 天 19:00 生成复习清单与自测题" \
  --prompt "$(cat /tmp/ops3-prompt.txt)"
```

`/tmp/ops3-prompt.txt`：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/assessment-guide.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-3 · 考前 1 天生成复习清单与自测题。
【状态】读 IMA《AI教学·自动化状态》OPS-3 节点 exam 信息 与 已完成模块列表（缺失则用 A/B/C/D 基础模块）。
【幂等】key = "OPS-3:<exam-id>"；台账命中 success → 记 skipped 退出。
【执行】1.据已完成模块生成复习清单(按薄弱点优先排序) 2.抽取10道自测题(单选为主,含答案解析) 3.设考前复习闹钟。
【验证】复习清单覆盖已完成模块；自测题可答、答案唯一。
【落点】①闹钟「考前复习」②备忘录「复习清单+自测链接」③IMA 存自测题(可回看)。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts}。
【失败】台账记 failed + 备忘录告警 + 退出码 0。
```

---

## OPS-4 · 教研组周报（协作沉淀）

### 编排
```
触发(每周五 17:00) → 汇总本周：
  - 新增/迭代课件游戏（IMA 已落库清单）
  - 评估完成数与平均薄弱点（OPS-6 / Runbook D 数据）
  - 协作备课室变更（腾讯文档版本）
  → DELIVER：腾讯文档《教研组周报》+ 分享 + 备忘录待办
  → LEARN：把高频薄弱点写入下周 OPS-2 速递选题
```

### 注册命令（须先预览确认）
```bash
./scripts/scheduler-api.sh create \
  --name "AI教学·教研组周报" \
  --cron "0 0 17 * * 5" \
  --frequency-type "daily" \
  --timeout 600 --retry-count 2 \
  --description "OPS-4 · V7.0：每周五 17:00 汇总本周备课/评估/协作并生成周报" \
  --prompt "$(cat /tmp/ops4-prompt.txt)"
```

`/tmp/ops4-prompt.txt`：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/collaboration-guide.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-4 · 生成本周教研组周报。
【状态】读 IMA《AI教学·自动化状态》OPS-4 节点 与 本周台账记录（ISO 周）。
【幂等】key = "OPS-4:<ISO周 如2026-W35>"；台账命中 success → 记 skipped 退出。
【执行】汇总本周：1)新增/迭代课件与游戏(IMA落库清单) 2)评估完成数与平均薄弱点(取 OPS-6/Runbook D 数据) 3)协作备课室变更(腾讯文档版本)。生成结构化周报。
【验证】数据来源可追溯(附 IMA 落库清单/评估数据/协作版本)；缺失数据标注"本周无"而非编造。
【落点】腾讯文档《教研组周报》+ 分享教研组 + 备忘录待办。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts}；LEARN：把高频薄弱点写入下周 OPS-2 速递选题。
【失败】台账记 failed + 备忘录告警 + 退出码 0。
```

---

## OPS-5 · 模块轮转课件（⭐ 覆盖 A→G + E·N 全模块）

**目的**：让**所有模块**都能周期性地自动产出教学产物，而不是只有院校流被自动化。
**状态推进**：`cursor.module` 按序轮转（见下），走完一轮后回到起点并 `round += 1`。

轮转序（覆盖全部模块与单元）：
```
A1→A2→A3→B1→B2→C1→C2→C3→C4→C5→D1→D2→E1→E2→E3→E4→E5→E·N→F1→F2→F3→F4→G1→G2→G3 →(回到 A1, round+1)
```

### 编排
```
触发(每周三 10:00) → 读 cursor.module
  → BUILD：按 p5js-courseware-guide.md 该单元章节生成课件 HTML
          （逢 E·N / F / G 单元，可叠加生成游戏，参考 p5js-game-design-guide.md）
  → VERIFY：跑 playwright-control-test-harness.js，未过则修复，预算 ≤3
  → DELIVER：IMA 落库 + 预览面板 + 腾讯文档索引追加
  → 回写 cursor 推进到下一单元
```

### 注册命令（须先预览确认）
```bash
./scripts/scheduler-api.sh create \
  --name "AI教学·模块轮转课件" \
  --cron "0 0 10 * * 3" \
  --frequency-type "daily" \
  --timeout 900 --retry-count 2 \
  --description "OPS-5 · V7.0：每周三 10:00 按 A→G+E·N 轮转生成一个单元的互动课件（含实测）" \
  --prompt "$(cat /tmp/ops5-prompt.txt)"
```

`/tmp/ops5-prompt.txt`：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/p5js-courseware-guide.md、references/p5js-game-design-guide.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-5 · 按轮转序为下一个单元生成互动课件(必要时含游戏)。轮转序：A1,A2,A3,B1,B2,C1,C2,C3,C4,C5,D1,D2,E1,E2,E3,E4,E5,E·N,F1,F2,F3,F4,G1,G2,G3；末位后回到 A1 且 round+1。
【状态】读 IMA《AI教学·自动化状态》OPS-5 节点 cursor.module（初值 "A1"）与 round（初值 1）。
【幂等】key = "OPS-5:<ISO周 如2026-W35>"；台账命中 success → 记 skipped 退出。
【执行】1.按 p5js-courseware-guide.md 该单元章节生成单文件互动课件 HTML(实例模式/响应式/CDN降级/中文注释) 2.E·N/F/G 单元额外生成一个配套游戏 HTML 3.对每个 HTML 运行 node assets/playwright-control-test-harness.js <file> --out /tmp/verify 实测。
【验证】harness 退出码必须为 0；未过则修复后复测，预算≤3；仍不过→只分发已通过产物并记 failed 明细。
【落点】IMA 知识库落库 + 预览面板可开 + 腾讯文档《课件索引》追加条目。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts,cursor:{module:下一单元,round},verify:{controls,pass,gate}} 并回写 cursor。
【失败】台账记 failed(含未过控件明细) + 备忘录告警 + 退出码 0。
```

---

## OPS-6 · 学习进度周检与补学回流（⭐ 评估→推荐→课件 闭环自动化）

**目的**：把 V6.0 的 LEARN 回流从「建议」变成「**自动执行的闭环**」——每周自动测、自动诊、自动出补学方案。

### 编排
```
触发(每周日 20:00) → 读已完成模块与历史薄弱点
  → BUILD：生成本周自测题组（能力四，约 20 题）→ 诊断薄弱点
  → LEARN：薄弱点 → 自动生成补学路径（能力五）+ 补学课件建议（能力一）
  → DELIVER：IMA 存学习报告 + 备忘录写补学计划 + 日历排下周补学时段
  → 回写 lastDiagnosis（供 OPS-4 周报与 OPS-2 选题使用）
```

### 注册命令（须先预览确认）
```bash
./scripts/scheduler-api.sh create \
  --name "AI教学·学习进度周检与补学回流" \
  --cron "0 0 20 * * 0" \
  --frequency-type "daily" \
  --timeout 900 --retry-count 2 \
  --description "OPS-6 · V7.0：每周日 20:00 自测诊断薄弱点并自动生成补学路径与课件建议" \
  --prompt "$(cat /tmp/ops6-prompt.txt)"
```

`/tmp/ops6-prompt.txt`：
```text
【角色】你是 AI 通识课资深专家 V7.0，L4 自动化模式。技能目录 ~/.codebuddy/skills/ai-literacy-expert-v5/。必读 SKILL.md、references/automation-l4-scheduler.md、references/assessment-guide.md、references/recommendation-engine.md。
【会话】CODEBUDDY_SESSION_TYPE=automation：1)严禁加载 automation-task-manager 2)不提问不等待确认 3)先读状态后回写 4)幂等优先 5)失败记台账+备忘录告警+退出码0。
【任务】OPS-6 · 本周学习进度周检 + 薄弱点诊断 + 自动生成补学方案。
【状态】读 IMA《AI教学·自动化状态》OPS-6 节点 lastDiagnosis 与 已完成模块、历史薄弱点。
【幂等】key = "OPS-6:<ISO周 如2026-W35>"；台账命中 success → 记 skipped 退出。
【执行】1.按已完成模块生成自测题组(约20题,多题型) 2.评分并诊断薄弱点(按模块/知识点聚合) 3.据薄弱点调用推荐引擎生成补学路径 4.为每个薄弱点给出具体补学课件/游戏建议(指明模块单元,如 C3 验证闭环)。
【验证】诊断须有据(附各题作答情况与知识点归属)；补学建议须可执行(指明具体模块单元与产物类型)，不得空泛。
【落点】IMA 存学习报告 + 备忘录写补学计划 + 日历排下周补学时段。
【留痕】追加台账 {key,task,ts,status,durationMs,artifacts,notes:薄弱点摘要} 并回写 lastDiagnosis(供 OPS-4 周报与 OPS-2 选题)。
【失败】台账记 failed + 备忘录告警 + 退出码 0。
```

---

## 运营流的通用约束（V7.0 强化）

1. **授权优先**：任何 IMA/腾讯文档写入前确认授权；未授权 → 降级为「本地生成 + 操作指引」并记 `failed`。
2. **最小打扰**：默认「静默生成 + 关键节点 1 条提醒」；可设「仅周报」「全静默」。
3. **可中断/可恢复**：状态写入 IMA，用户说「暂停自动驾驶」「4 周改 6 周」即可热更新 cursor。
4. **不越权**：不自动发邮件/外发敏感信息；分享范围限班级/备课组（回扣 F2 隐私、商用标准 §6）。
5. **幂等不重复**（V7.0 新增）：每条流必须定义幂等键并在 prompt 中写明查重逻辑。
6. **留痕可审计**（V7.0 新增）：每次执行必须追加台账一行，成功/跳过/失败三态齐全。
7. **配额管理**（V7.0 新增）：宿主上限 100 个任务，本技能建议 ≤10；注册前先 `list` 查余量。

---

## 与请求驱动流的衔接

运营流**复用**请求驱动的 runbook，不是孤岛：

| 运营流 | 复用的 runbook |
|--------|----------------|
| OPS-1 每周包 | Runbook A/B/C/D 的定时版 |
| OPS-3 自测 | Runbook D 简化版 |
| OPS-5 轮转课件 | Runbook A（+B）定时版 |
| OPS-6 周检 | Runbook D + E + A 的闭环串联 |

所有 BUILD / VERIFY / DELIVER / REPORT / LEARN 阶段与 `workflow-orchestrator.md` 完全一致。

> **一句话**：V6.0 是「**请求驱动的工作流**」；V7.0 是「把这套工作流**按时间自动点火**，并保证它在没人看着的时候也**跑得对、记得住、不重复、可查证**」。
