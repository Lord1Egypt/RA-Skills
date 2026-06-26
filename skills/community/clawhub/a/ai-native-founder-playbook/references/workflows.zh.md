# 工作流

用这些 workflow 把 startup strategy 转化为可执行的 AI-agent 循环。

## Idea Validation Loop

目的：防止在证据不足时过早 build。

步骤：

1. 用一句话写 problem hypothesis：target segment、painful workflow、frequency、severity、current workaround、proposed outcome。
2. 让 reasoning assistant 把它改写到可测试。
3. 要求 AI 给出反对该 hypothesis 的最强论证。
4. 映射 direct competitors、indirect substitutes、adjacent products、potential acquirers、incumbents。
5. 说明每类 competitor 为什么可能赢。
6. 手写 discovery questions。
7. 让 AI 标记 leading、future-facing、too broad、socially desirable 的问题。
8. 访谈真实 target users。
9. 每五次访谈后，分开综合支持和挑战 hypothesis 的证据。
10. 如果证据支持问题存在，只 build 一个最小 prototype 来测试 core interaction。

Prompt pattern:

```text
Act as a skeptical startup advisor. Here is my problem hypothesis:
<hypothesis>

Separate facts from assumptions. Rewrite it as a testable hypothesis, then list the strongest disconfirming evidence I should look for before building.
```

## MVP Build Loop

目的：快速 build，但不让 agentic coding 造成 product、architecture 或 security debt。

步骤：

1. 写 `MVP_SCOPE.md`，列出 included features、excluded features 和 feature amendment criteria。
2. 写 coding agents 可读的 architecture/context document。
3. 定义未来 6 个月真实 scale，不按幻想规模设计。
4. 有意识选择 dependencies，并记录 tradeoffs。
5. 使用短 coding-agent sessions，每次只做一个任务。
6. 每次 session 开始时提供 scope、architecture context、constraints、verification expectations。
7. 每次 session 结束时写 decision log：改了什么、为什么、引入什么 assumptions、后续检查是什么。
8. 真实用户接触产品前做 security review。
9. launch 前定义 activation、retention、revenue、referral 和 false-positive signals。
10. 每周 review user feedback，并分成 product signal、onboarding signal、positioning signal、outlier requests。

Coding-agent session template:

```text
Task:
<one implementation goal>

Context:
- Read MVP_SCOPE.md.
- Read the architecture context file.
- Preserve existing architectural decisions unless the task explicitly revises them.

Constraints:
- Do not add out-of-scope features.
- Add or update tests for changed behavior.
- Document any new architectural assumption.

Verification:
- Run the relevant tests or explain exactly why they cannot run.
```

## PMF Diagnostic Loop

目的：避免把早期兴奋误判成 product-market fit。

适用场景：

- signup spike 但 activation 弱。
- 有 revenue 但 retention 差。
- 用户口头称赞但不回来。
- 三轮以上 iteration 没有推动 PMF benchmarks。

步骤：

1. 收集 activation、Day 7、Day 30、retention、revenue、referral、qualitative feedback。
2. 要求 AI 给出最 skeptical interpretation。
3. 按行为而不是 persona 切 segment。
4. 判断 gap 是 product、positioning、onboarding、pricing 还是 audience。
5. 决策：adjust、narrow、pivot、pause 或 return to Idea。

Prompt pattern:

```text
Here are our PMF metrics and feedback:
<data>

Make the strongest skeptical case against our traction. Then identify whether we have a segment responding differently, whether the gap is product or positioning, and what would have to be true for this product to reach genuine PMF.
```

## Launch Operating System Loop

目的：用 repeatable systems 替代 founder attention，同时强化 product 和 operations。

步骤：

1. 用 coding agent 做 technical debt audit。
2. 把 findings 分成 release blockers、next-sprint work、acceptable debt、monitoring items。
3. 盘点 founder-owned recurring tasks、decisions、approvals、workflows。
4. 每项标记为 automate、delegate、document 或 founder-only。
5. 为可自动化 workflow 设计 triggers、inputs、decision rules、outputs、owners、escalation paths。
6. 建立 lightweight product management system：sprint cadence、minimum spec template、bug triage tree、weekly metrics brief。
7. 让 security 与 compliance 成为 recurring workstreams。
8. 复查 acquisition 是否 channel-driven，unit economics 是否可解释。

Prompt pattern:

```text
Audit this launch-stage operation. Classify every founder-owned workflow as automate, delegate, document, or founder-only. For each automation candidate, propose trigger, input, decision rule, output, owner, and escalation path.
```

## Scale Moat Loop

目的：把 domain expertise、customer data、integrations 和 workflows 转化为 defensible advantage。

步骤：

1. 建 founder bottleneck map，测试 founder 离开一周会停掉什么。
2. 把 institutional knowledge 写成 playbooks、decision rules 和 reusable agent context。
3. 准备 enterprise readiness artifacts：documentation、SLAs、support playbooks、incident response、observability、procurement answers、compliance evidence。
4. 建 GTM engine：segmentation、messaging、sales playbooks、analyst narrative、outbound cadence、CRM hygiene、pipeline reporting。
5. 找出 generic competitors 一定会做错的 vertical edge cases。
6. 把 edge cases 转成 tests、validations、prompts、integrations、support workflows 或 eval suites。
7. 审计 user interaction data，找能改善 product 的 behavioral patterns。
8. 映射 customer integrations 并估算 switching cost。
9. 决定哪些 integrations、APIs、webhooks、SDKs 或 automations 能加深 workflow lock-in。

Prompt pattern:

```text
Here is our current product, customers, integrations, and usage data:
<context>

Identify three defensible advantages we can compound over the next two quarters: domain edge cases, proprietary behavioral data, and workflow lock-in. For each, propose a product action, an agent workflow, a metric, and a proof point for enterprise buyers.
```
