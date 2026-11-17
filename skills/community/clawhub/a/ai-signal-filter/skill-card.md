## Description:

从海量AI动态中筛选真正有决策价值的信号，每条必须回答"所以呢"和"该做什么"。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ah0210](https://clawhub.ai/user/ah0210)

### License/Terms of Use:

MIT-0

## Use Case:

AI practitioners, developers, product builders, and decision makers use this skill to turn broad AI news into concise Chinese decision signals with sources, confidence labels, and concrete next actions. It is intended for recurring AI industry monitoring, filtering, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad AI-news prompts may trigger web searches, sub-agent runs, or persistent memory updates.

Mitigation: Use the skill only for explicit AI signal report requests and review it before installation if those behaviors are not desired.

Risk: Personalization and history files can retain long-term preferences, source scoring, and prior signal records.

Mitigation: Check or clear memory/signal/profile.md and memory/signal/history.md when persistent personalization is not wanted.

Risk: AI-news sources can be noisy, low-confidence, or misleading.

Mitigation: Require source URLs, confidence labels, quality gates, and low-confidence placement in the waiting/observation section.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ah0210/skills/ai-signal-filter)
- [Search strategy](references/search-strategy.md)
- [Quality gates](references/quality-gates.md)
- [Output format](references/output-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Structured Chinese Markdown report with execution metadata, news briefs, signal analysis, source URLs, confidence labels, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory/history files for personalization and only saves report archives after user confirmation.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
