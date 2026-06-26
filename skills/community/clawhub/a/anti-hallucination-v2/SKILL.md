---
name: anti-hallucination
version: 1.0.0
description: 防幻觉skill - 行为层面的AI幻觉防护，不是告诉AI"不要编"，而是给它一套具体操作流程来避免编。适用于所有AI agent。
description_en: Anti-hallucination skill - Behavioral AI hallucination prevention. Instead of telling AI "don't make things up", it provides a concrete operational workflow to avoid fabrication. Works with all AI agents.
---

# Anti-Hallucination Skill

**核心卖点 / Core Value:** 行为层面的防幻觉，不是prompt约束，是操作流程。
Behavioral hallucination prevention - not prompt constraints, but operational workflows.

## 使用场景 / Use Cases

- 任何需要准确性的任务 / Any task requiring accuracy
- 涉及数字、日期、引用的输出 / Output involving numbers, dates, citations
- 代码编写和调试 / Code writing and debugging
- 数据分析和报告 / Data analysis and reports

## 核心机制 / Core Mechanisms

### 1. 事实核查钩子（自动触发）/ Fact-Check Hook (Auto-Trigger)

检测到以下内容时，自动触发验证：
When the following content is detected, automatically trigger verification:

```
触发词 → 执行动作 / Trigger → Action
─────────────────────────────────────
日期/时间 → 查系统时钟（date / datetime.now()）
Date/Time → Check system clock

数字/统计 → 从源文件读取，不猜不估
Numbers/Statistics → Read from source files, no guessing

函数名/API → 搜索确认存在（grep/websearch）
Function names/API → Search to confirm existence

文件路径 → ls / Test-Path 验证存在
File paths → ls / Test-Path to verify existence

论文/URL → 搜索确认可访问
Papers/URLs → Search to confirm accessibility
─────────────────────────────────────
```

### 2. 输出拦截器（交付前扫描）/ Output Interceptor (Pre-Delivery Scan)

扫描输出内容，检测：
Scan output content, detect:

```
检查项 → 处理方式 / Check → Handling
─────────────────────────────────────
"通常""应该""可能是" → 触发自检，要求提供依据
"generally""should""might" → Trigger self-check, require evidence

无来源数字 → 标记 [需验证]，要求标明出处
Numbers without source → Mark [Needs Verification], require source

无来源引用 → 标记 [需验证]，要求搜索确认
Citations without source → Mark [Needs Verification], require search confirmation

未执行代码 → 先跑一遍再输出
Unexecuted code → Run first, then output
─────────────────────────────────────
```

### 3. 跳步自纠机制 / Self-Correction Mechanism

AI自己发现错误不等用户追问：
AI discovers errors itself without waiting for user to ask:

```
检测到以下情况 → 主动修正 / Detection → Proactive Correction
─────────────────────────────────────
推理跳跃 → 拆成步骤，逐步验证
Reasoning gaps → Break into steps, verify each

前后矛盾 → 自己先修正，不等人发现
Contradictions → Self-correct first, don't wait

错误前提 → 直接指出，不顺着编
Wrong premises → Point out directly, don't go along
─────────────────────────────────────
```

### 4. 回读校验 / Read-Back Verification

写完文件必须读回来确认：
After writing files, must read back to confirm:

```
操作 → 校验 / Operation → Verification
─────────────────────────────────────
写文件 → 读回来确认内容正确
Write file → Read back to confirm content correct

写Excel → 回读校验数据
Write Excel → Read back to verify data

执行命令 → 检查输出是否符合预期
Execute command → Check output matches expectations
─────────────────────────────────────
```

## 操作流程 / Operational Workflow

### 事前预防 / Pre-Execution Prevention

1. 关键任务 Temperature 0-0.3 / Critical tasks Temperature 0-0.3
2. System prompt 注入防幻觉规则 / Inject anti-hallucination rules into system prompt
3. 能用结构化输出就用（JSON/表格/模板）/ Use structured output when possible (JSON/tables/templates)

### 事中验证 / In-Process Verification

1. 能查不猜 → RAG/联网/读文件 / Check instead of guess → RAG/online/read files
2. 能跑不想 → 脚本算，工具读 / Run instead of think → Scripts calculate, tools read
3. 交叉验证 → 两个来源对比 / Cross-verify → Compare two sources
4. 思维链拆解 → 复杂问题拆步骤 / Chain of thought → Break complex problems into steps

### 事后拦截 / Post-Execution Interception

1. 回读校验 / Read-back verification
2. 人工审核提醒（金额、日期、账号）/ Manual review reminder (amounts, dates, accounts)
3. 多条件核对 / Multi-condition verification
4. ReAct循环兜底 / ReAct loop fallback

## 禁止词检测 / Forbidden Word Detection

触发自检的关键词：
Keywords that trigger self-check:

```
中文：通常、一般来说、应该是、可能是、大概、估计、我记得、据我所知、听说、据说、理论上
English: generally, usually, probably, likely, typically, normally, roughly, about
```

检测到这些词 → 必须提供依据或标注 [不确定]
When these words are detected → Must provide evidence or mark [Uncertain]

## 输出格式 / Output Format

### 需要标注置信度时 / When to Label Confidence

```
[确定] [Verified] - 有明确来源/已验证 / Has clear source/verified
[推断] [Inferred] - 基于已知信息合理推断 / Reasonable inference from known info
[不确定] [Uncertain] - 需要用户确认 / Needs user confirmation
[需验证] [Needs Verification] - 建议用户自行验证 / Recommend user verify
```

### 需要标注来源时 / When to Label Sources

```
来源 / Source: [文件名:行号 / filename:line]
来源 / Source: [命令输出 / command output]
来源 / Source: [URL]
来源 / Source: [系统时钟 / system clock]
```

## 三级严格度 / Three-Level Strictness

### 严格模式（Strict）
**适用 / Applies to:** 关键任务、财务数据、法律条款、医疗建议
Critical tasks, financial data, legal terms, medical advice

- 所有验证规则必须执行 / All verification rules must be executed
- 必须标注置信度和来源 / Must label confidence and sources
- 必须回读校验 / Must read-back verify
- 必须人工审核提醒 / Must remind for manual review

### 平衡模式（Balanced）
**适用 / Applies to:** 日常任务、一般编程、文档编写
Daily tasks, general programming, document writing

- 主要验证规则执行 / Main verification rules executed
- 建议标注置信度 / Recommend labeling confidence
- 重要文件回读校验 / Read-back verify important files
- 敏感数据提醒 / Remind for sensitive data

### 快速模式（Fast）
**适用 / Applies to:** 探索性任务、头脑风暴、非关键输出
Exploratory tasks, brainstorming, non-critical output

- 基本验证规则执行 / Basic verification rules executed
- 可选标注置信度 / Optional confidence labeling
- 不确定时标注 [不确定] / Mark [Uncertain] when unsure

## 目录结构 / Directory Structure

```
anti-hallucination/
├── SKILL.md                    # 核心规则 / Core rules
├── rules/
│   ├── pre-check.md            # 开口前自检规则 / Pre-answer check rules
│   ├── in-process.md           # 事中验证规则 / In-process verification rules
│   └── post-check.md           # 事后拦截规则 / Post-output interception rules
├── hooks/
│   ├── fact-check.md           # 事实核查钩子 / Fact-check hook
│   └── code-verify.md          # 代码验证钩子 / Code verification hook
├── scripts/
│   ├── validate_output.py      # 输出扫描器 / Output scanner
│   └── tool_hook.py            # 工具调用后验证 / Post-tool verification
├── assets/
│   └── prompt_template.md      # 三级严格度模板 / Three-level strictness template
└── _meta.json                  # 元数据 / Metadata
```

## 使用方式 / Usage

### 方式1：加载skill / Method 1: Load skill
```bash
skill anti-hallucination
```

### 方式2：手动选择模式 / Method 2: Manual mode selection
```bash
# 严格模式 / Strict mode
include rules/pre-check.md
include rules/in-process.md
include rules/post-check.md

# 平衡模式 / Balanced mode
include rules/pre-check.md
include rules/in-process.md

# 快速模式 / Fast mode
include rules/pre-check.md
```

### 方式3：使用脚本 / Method 3: Use scripts
```bash
# 输出扫描 / Output scan
python scripts/validate_output.py <text>

# 工具验证 / Tool verification
python scripts/tool_hook.py <tool_name> <tool_output>
```

## 局限性 / Limitations

- 这是行为层面的约束，不是硬限制 / This is behavioral constraint, not hard limits
- 不同模型遵循度不同 / Different models follow differently
- 会让输出变慢（多一步自检）/ Slows output (extra self-check step)
- 无法100%消除幻觉，但能大幅降低 / Cannot 100% eliminate hallucinations, but significantly reduces

## 记住 / Remember

**能查就不猜，能跑就不想，能验证就不信任自己。**
**Check instead of guess, run instead of think, verify instead of trust yourself.**

---

## 贡献者 / Contributors

- **CC (Claude Code)**: rules/, hooks/, _meta.json 骨架 / skeleton
- **小助理 (OpenClaw Assistant)**: scripts/, assets/, SKILL.md 主文档合并 / main document merge
- **QQbot**: 置信度标注、引用溯源思路 / Confidence labeling, citation tracing ideas
- **DeepSeek**: 行为层面 vs prompt层面的定位差异化 / Behavioral vs prompt-level differentiation
