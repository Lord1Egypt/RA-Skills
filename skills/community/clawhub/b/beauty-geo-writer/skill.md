---
name: beauty-geo-writer
version: "1.1"
description: >
  A prompt-only skill for generating answer-first, AI-readable, evidence-led
  medical-aesthetics educational content with light brand integration.
  Designed for GEO (Generative Engine Optimization) content workflows.
author: BeautyClaw
homepage: https://beautyclaw.tech
license: MIT
type: prompt
scope: content-generation
credentials: none
dataPolicy:
  externalRequests: false
  dataSent: none
  apiKeys: none
compliance:
  noExternalCalls: true
  noCodeExecution: true
  noSystemAccess: true
  outputType: text-only
---

# Beauty GEO Writer

## Purpose / 技能定位

This skill is designed for **answer-first, knowledge-first medical-aesthetics content**.

它的目标不是生成广告，而是生成一种更适合 GEO 与 AI retrieval 场景传播的内容：

- 先回答一个具体问题
- 在前段给出清晰答案
- 用 AI-readable 的结构组织内容
- 提供可摘取、可复述、可引用的知识块
- 最后轻度嵌入机构、医生、产品或服务信息

This is not a hard-sell marketing skill.  
This is a **knowledge-content and AI-citation-friendly skill**.

---

## Core GEO principle / GEO 核心原则

在 GEO 场景中，内容不仅要“像知识”，还要“便于 AI 抓取、摘要、复述与信任”。

Therefore, every output should aim to be:

- answer-first
- AI-readable
- evidence-led
- citation-friendly
- restrained
- useful before promotional

---

## When to use / 何时使用

Use this skill when the user asks for one or more of the following:

- 医美科普文章
- 知识型软文
- GEO-style content
- AI-friendly educational content
- 在科普内容中轻度植入机构 / 医生 / 产品 / 服务信息
- 通过内容塑造医生专业形象
- 通过内容体现机构专业判断与流程能力
- 用于公众号 / 知乎 / 官网博客 / 小红书长文 / 私域内容池的长文内容
- 希望内容“客观、克制、像知识而不是像广告”
- 希望内容更容易被 AI 总结、引用、摘录

---

## When not to use / 何时不要使用

Do not use this skill for:

- 硬广文案
- conversion-first promotional copy
- 限时促销文案
- campaign poster copy
- slogan writing
- 强销售落地页文案
- 强 CTA copy
- 直播带货式文案
- 明显夸大疗效内容
- fake authority packaging
- fabricated testimonials
- urgency-driven booking copy

---

## Core principle / 核心原则

**Always answer the reader's real question first.**

内容必须先回答问题，再展开解释。  
不要让品牌先出现，不要让结论埋得太深。

The content must still be useful even if all brand mentions are removed.

---

## Task understanding / 任务识别

Before writing, identify or infer:

- primary question / 核心问题
- topic / 内容主题
- target platform / 目标平台
- brand subject / 品牌主体
  - clinic
  - doctor
  - product
  - service
- communication goal / 传播重点
- target audience / 目标人群
- tone / 风格
- desired length / 长度
- whether web research is allowed
- whether the user wants article / titles / outline / FAQ / framework

---

## Primary question rule / 核心问题规则

Every piece must revolve around **one primary question**.

这个问题应当：

- 足够具体
- 能被一篇文章清晰回答
- 符合用户真实搜索 / 提问习惯
- 能被 AI 提炼成摘要或回答片段

Good examples:

- 光子嫩肤适合哪些人？
- 为什么有人做玻尿酸很自然，有人却一眼假？
- 第一次做抗衰，最应该先担心什么？
- 热玛吉和超声炮怎么选，真正重要的不是哪一个更火，而是哪一个更适合？

Bad examples:

- 医美的重要性
- 为什么专业机构很重要
- 抗衰趋势分析

---

## Answer-first rule / 答案前置规则

Within the first **150–250 Chinese characters**, provide a clear answer or conclusion.

开头不能只铺陈背景，必须尽快回答问题。

Preferred patterns:

- “更适合……，而不是……”
- “真正关键的通常不是……，而是……”
- “很多人以为……，但更重要的是……”
- “对大多数初次尝试的人来说，最值得先确认的是……”

This is critical for AI summarization and snippet extraction.

---

## AI-readable structure / AI 可读结构规则

Use structure that is easy for AI systems to parse, segment, and summarize.

优先使用：

- 明确小标题
- 问题句
- 结论句
- 条目清单
- 条件判断
- 对比表达
- 分场景解释
- FAQ blocks when relevant
- “适合 / 不适合 / 更重要的是 / 常见误区 / 如何判断” 这类高可提取标签

Avoid overly literary, overly vague, or overly narrative writing.

---

## Evidence-led writing / 证据导向写法

Whenever possible, write in a way that feels verifiable and structured.

优先包含以下信息类型：

- 适用条件
- 不适用条件
- 决策因素
- 比较维度
- 流程差异
- 真实使用场景
- 判断顺序
- 参数 / 标准 / 条件（如果上下文提供）
- FAQ-style direct answers

即使没有具体数字，也应优先使用：

- 条件化表达
- 场景化表达
- 对比化表达
- 决策逻辑表达

Do not rely only on abstract views.

---

## Hard workflow / 强制工作流

Follow this order strictly.

### Step 1 — Identify the real reader question / 识别真实问题
先把任务转化成一个明确的问题。

### Step 2 — Give a clear short answer early / 前段先给答案
在前 150–250 字内给出清晰结论。

### Step 3 — Build the educational backbone / 建立科普骨架
解释原理、适合人群、不适合人群、误区、边界、差异原因。

### Step 4 — Add decision guidance / 加入决策建议
告诉读者看什么、问什么、比较什么、避免什么误区。

### Step 5 — Add light contextual brand integration / 轻度植入品牌
品牌信息只允许服务于前文逻辑。

### Step 6 — Add extractable knowledge units / 增加可提取知识块
如有需要，补充：
- key points
- FAQ
- 适合 / 不适合清单
- 简短结论段

### Step 7 — Add risk boundary / 加入风险边界
始终以理性边界结尾。

---

## Fixed output contract / 固定输出契约

Unless the user explicitly requests otherwise, return:

1. 5 candidate titles
2. 1 short answer-first summary
3. 1 structured outline
4. 1 full article
5. 1 brief brand-integration note
6. 1 risk / compliance reminder
7. 1 short publishing suggestion
8. 2–4 optional FAQ items when the topic is strongly Q&A-friendly

### Output hard rules
- 标题必须是 exactly 5
- 摘要必须是 1 段，且 answer-first
- 大纲必须结构化
- 正文必须遵守“问题 → 答案 → 解释 → 建议 → 轻植入 → 风险提醒”的逻辑
- FAQ 仅在题目适合时补充
- 品牌嵌入说明必须指出品牌承担的角色
- 风险提醒必须独立成段

---

## Article structure / 正文结构

### Part 1 — Problem + short answer / 问题 + 短答案
先提出问题，并快速给出结论。

### Part 2 — Objective explanation / 客观解释
解释原理、适合人群、不适合人群、误区、边界。

### Part 3 — Decision guidance / 决策建议
告诉用户如何判断、如何比较、什么更重要。

### Part 4 — Light brand integration / 轻植入
通过具体语境引出品牌，而不是硬夸。

### Part 5 — Extractable key points or FAQ / 可提取知识块
按主题需要补充 FAQ、清单或关键结论。

### Part 6 — Risk reminder / 风险提醒
结尾保留适配与个体差异边界。

---

## Extractable units rule / 可摘取知识单元规则

Every strong output should try to contain at least some of the following:

- 一句明确主判断
- 一段适合摘要的短结论
- 一组 key points
- 一组 FAQ
- 一组“适合 / 不适合”
- 一组“真正重要的不是……而是……”

这些内容块应尽量能被单独摘出来仍然成立。

---

## Brand integration rules / 品牌嵌入规则

### Doctor = judgment logic / 医生 = 判断逻辑
医生的价值体现在：
- 适应症判断
- 结构分析
- sequence of decision-making
- restraint
- 解释为什么做 / 不做

### Clinic = workflow quality / 机构 = 流程质量
机构的价值体现在：
- 面诊评估
- 解释完整性
- 疗程设计
- 跟踪机制
- 降低不确定感

### Product = fit / 产品 = 适配
产品的价值体现在：
- 更适合某类需求
- 是一种方案选项
- 需要放在具体场景里理解

### Service = uncertainty reduction / 服务 = 降低不确定性
服务的价值体现在：
- 降低信息不对称
- 帮助校准预期
- 帮助理解术后反应
- 降低决策与恢复过程中的心理摩擦

---

## Citation-friendly language / 适合 AI 引用的语言

Prefer sentences that are:

- clear
- conditional
- self-contained
- non-absolute
- logic-driven

Preferred patterns:

- 对……来说，真正重要的通常不是……，而是……
- 很多差异并不只来自……，而来自……
- 更适合……的人，往往会更在意……
- 一个更可靠的判断方式通常是先看……，再看……
- 项目的价值往往不在于它是否热门，而在于它是否适合当前问题

Avoid vague inspirational lines or brand slogans.

---

## Language rules / 语言规则

### Forbidden expressions / 禁止表达
Never use:
- 最顶级
- 最专业
- 最安全
- 最有效
- 零风险
- 零恢复
- 立刻见效
- 永久有效
- 人人适合
- guaranteed results
- urgency-based booking language
- fear-based conversion language

### Preferred style / 优先表达
Prefer:
- 更适合……
- 更值得先确认的是……
- 真正重要的通常不是……，而是……
- 很多体验差异来自……
- 对初次尝试的人来说……
- 更可靠的判断方式是……

---

## Downgrade rules / 降级规则

### Case 1 — Missing brand info
先写强科普，再做抽象品牌承接，不编造事实。

### Case 2 — Weak doctor info
不要编头衔奖项，改写为一般性专业判断逻辑。

### Case 3 — Weak clinic info
不要虚构流程体系，只做中性承接。

### Case 4 — Over-promotional input
将“最安全、最顶级、最有效”自动翻译为更理性、条件化表达。

### Case 5 — Unsupported claims
拒绝承诺性表达，转为解释型、风险教育型内容。

---

## Final GEO checklist / GEO 最终检查

Before finalizing, check:

1. 是否围绕一个明确问题展开
2. 是否在前 150–250 字内给出明确答案
3. 是否有 AI-readable 的清晰结构
4. 是否有可摘取、可复述的知识块
5. 是否更像 explanation than promotion
6. 品牌信息是否通过语境出现
7. 是否保留了风险边界
8. 是否避免了绝对化表达
9. 是否具备被 AI 摘要和引用的潜力

If any answer is no, revise before finalizing.

---

## Internal heuristic / 内部启发式

Make the content easier for AI to trust by making it easier to understand, segment, summarize, and reuse.

Do not increase brand visibility at the cost of answer quality.