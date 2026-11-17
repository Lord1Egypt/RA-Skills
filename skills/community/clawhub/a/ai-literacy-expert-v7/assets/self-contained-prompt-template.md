# 自包含调度指令模板（L4 · V7.0）

> **用途**：供注册自动化任务时生成 `--prompt` 参数内容。
>
> **为什么需要模板**：调度系统触发任务时会在**全新的 automation 会话**中执行本指令，该会话**没有**本次对话的历史上下文、不知道用户刚才说过什么、也不知道上次跑到第几周。因此指令**必须自带完成任务所需的全部信息**，否则自动化必然"跑偏或重来"。

---

## 一、通用模板（复制后按占位符填充）

```
【角色】你是 AI 通识课资深专家 V7.0，运行在 L4 自动化模式。
        技能目录：~/.codebuddy/skills/ai-literacy-expert-v5/
        必读：SKILL.md + references/automation-l4-scheduler.md + references/automation-ops.md

【会话】当前 CODEBUDDY_SESSION_TYPE=automation（自动化调度执行态），你必须遵守：
        1. 严禁加载或调用 automation-task-manager（自动化会话不得自己管理调度）
        2. 不得向用户提问、不得等待确认；遇决策点按预设缺省执行，并把待确认项写入备忘录
        3. 执行前先读状态、执行后回写状态并追加台账
        4. 幂等优先：先算幂等键查台账，命中成功记录即退出，不重复产出
        5. 失败时写台账 failed + 备忘录告警，并返回退出码 0（不阻塞调度，由调度系统按 retryCount 重试）

【任务】{{TASK_ID}} · {{TASK_GOAL_ONE_LINE}}

【状态】读取权威状态源：IMA 知识库《AI教学·自动化状态》文档，取 {{TASK_ID}} 节点的
        cursor / lastRun；若不存在则用初值 {{INITIAL_CURSOR}}。
        本地缓存（可选加速）：<宿主工作目录>/.ai-literacy-state/{{TASK_ID}}.json
              其中 <宿主工作目录> = 本会话的当前工作目录，运行时解析，勿硬编码绝对前缀。
        注意：本地缓存可能失效，一切以 IMA 为准。

【幂等】计算 idempotency_key = "{{TASK_ID}}:{{PERIOD_SPEC}}"
        查询台账（IMA《AI教学·执行台账》或 run-ledger.jsonl）中该 key 是否已有 status=success 记录：
        - 有 → 追加一条 status=skipped 日志后直接结束（绝不重复产出）
        - 无 → 继续执行

【执行】按 references/automation-ops.md 的 {{OPS_SECTION}} 执行：
        {{STEP_1}}
        {{STEP_2}}
        {{STEP_3}}

【验证】{{VERIFY_REQUIREMENT}}
        （课件/游戏类：必须运行
         node ~/.codebuddy/skills/ai-literacy-expert-v5/assets/playwright-control-test-harness.js <产物> --out /tmp/verify
         退出码非 0 → 修复，预算 ≤3 次；仍不过则降级并记 failed）

【落点】{{DELIVERY_TARGETS}}
        （如：追加腾讯文档《AI每日速递》 + IMA 知识库落库 + 写备忘录 + 设下次提醒）

【留痕】把下列记录追加到台账，并回写状态节点的 cursor / lastRun：
        {"key":"{{TASK_ID}}:{{PERIOD_SPEC}}","task":"{{TASK_ID}}","ts":"<ISO8601>","status":"success|failed|skipped",
         "durationMs":0,"artifacts":["<产物位置>"],"notes":"<摘要>"}

【失败】遇阻断（未授权/依赖缺失/生成失败）：
        1. 台账追加 status=failed 记录，notes 写明原因
        2. 写备忘录告警，给出可操作的补救指引
        3. 返回退出码 0（避免调度重试风暴），业务层不自行重试
        4. 若因未授权导致：降级为「本地生成 + 给出手动落库指引」
```

---

## 二、占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{TASK_ID}}` | 任务标识（与 registry 的 key 一致） | `OPS-2` |
| `{{TASK_GOAL_ONE_LINE}}` | 一句话目标 | `生成 1 篇 AI 前沿速递 + 1 道配套练习题` |
| `{{INITIAL_CURSOR}}` | 状态初值（首次执行用） | `{"issue":1}` |
| `{{PERIOD_SPEC}}` | 周期标识（决定幂等粒度） | `2026-08-29`（日）/ `2026-W35`（周） |
| `{{OPS_SECTION}}` | 运营流章节 | `OPS-2` |
| `{{STEP_N}}` | 执行步骤（逐条） | `检索 IMA 本周 AI 新发展素材` |
| `{{VERIFY_REQUIREMENT}}` | 验证要求 | `速递无事实硬伤、题目可答` |
| `{{DELIVERY_TARGETS}}` | 产出落点 | `腾讯文档 + IMA + 备忘录` |

---

## 三、填充示例：OPS-2 每日 AI 速递

```text
【角色】你是 AI 通识课资深专家 V7.0，运行在 L4 自动化模式。
        技能目录：~/.codebuddy/skills/ai-literacy-expert-v5/
        必读：SKILL.md + references/automation-l4-scheduler.md + references/automation-ops.md

【会话】当前 CODEBUDDY_SESSION_TYPE=automation（自动化调度执行态），你必须遵守：
        1. 严禁加载或调用 automation-task-manager
        2. 不得向用户提问或等待确认；遇决策点按缺省执行并写备忘录
        3. 执行前后读写状态与台账
        4. 幂等优先，命中成功记录即退出
        5. 失败写台账 failed + 备忘录告警，退出码 0

【任务】OPS-2 · 生成 1 篇 AI 前沿速递（约 300 字）+ 1 道配套练习题

【状态】读取 IMA《AI教学·自动化状态》中 OPS-2 节点的 issue / lastRun；
        不存在则用初值 {"issue":1}。以 IMA 为准，本地缓存仅加速。

【幂等】idempotency_key = "OPS-2:<今天日期 YYYY-MM-DD>"
        查台账该 key 是否 status=success：是 → 记 skipped 后结束；否 → 继续。

【执行】按 references/automation-ops.md 的 OPS-2 执行：
        1. 检索 IMA 知识库「本周 AI 新发展」素材（关联 G 模块）
        2. 生成 1 篇 300 字前沿速递，标注来源与日期
        3. 生成 1 道配套练习题（单选，关联最近已学模块），附答案与解析
        4. VERIFY：速递无事实硬伤、题目可答且答案唯一

【验证】速递事实与来源可核；题目有且仅有 1 个正确项。
        （本任务无 HTML 产物，不需运行 harness）

【落点】1. 追加到腾讯文档《AI每日速递》当日章节
        2. IMA 知识库落库（便于后续检索与周报汇总）
        3. 可选：备忘录写「今日一题」

【留痕】追加台账记录并回写 issue = issue + 1：
        {"key":"OPS-2:2026-08-29","task":"OPS-2","ts":"<ISO>","status":"success",
         "durationMs":42180,"artifacts":["腾讯文档/AI每日速递#2026-08-29"],"notes":"issue=5"}

【失败】1. 台账记 failed 并写明原因（如 IMA 未授权）
        2. 写备忘录告警 + 补救指引
        3. 退出码 0，不自行重试
```

---

## 四、自检清单（注册前逐条核对）

- [ ] 含【角色】且指明技能目录与必读文档
- [ ] 含【会话】且写明 5 条 automation 铁律（含"禁加载 automation-task-manager"）
- [ ] 含【状态】且权威源是 IMA（非仅本地文件）
- [ ] 含【幂等】且给出 key 计算规则与查重后的动作
- [ ] 含【执行】且步骤可直接照做（不依赖上下文）
- [ ] 含【验证】且课件/游戏类写明 harness 命令与修复预算
- [ ] 含【落点】且明确写到哪里
- [ ] 含【留痕】且给出台账 JSON 结构
- [ ] 含【失败】且写明退出码 0（避免重试风暴）
- [ ] 全文替换掉所有 `{{...}}` 占位符（残留即不合格）
