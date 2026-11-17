## Description:

德胧舆情情报综合工具箱 helps agents collect hotel-industry public-opinion signals, summarize web and video monitoring results, classify risks, and draft Feishu-ready alert or daily-report content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to monitor hotel and competitor public-opinion topics, analyze complaint or incident risk, and prepare Feishu-formatted reports, alerts, and response plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded Feishu delivery can send monitoring output to an unintended or unauthorized recipient.

Mitigation: Replace the recipient with an approved destination before deployment and review message-routing settings for each scheduled workflow.

Risk: Persistent scheduled monitoring can continue collecting and sending public-opinion results after the intended campaign or review period ends.

Mitigation: Make scheduled runs explicit opt-in, document how to disable them, and set an expiry or periodic owner review.

Risk: Mutable BettaFish package, Git, and container installation instructions can pull unpinned third-party code.

Mitigation: Pin package versions, repository commits, and container digests before installation, then scan dependencies in the target environment.

Risk: The web-search override broadens data-access behavior for monitoring tasks.

Mitigation: Remove the override unless needed, or scope search permissions and review collected results before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/delonix-intelligence-suite-v2)
- [BettaFish public-opinion analysis project](https://github.com/666ghj/BettaFish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with shell-command examples, Feishu card JSON examples, monitoring configuration snippets, and structured risk-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include web-search prompts, public-opinion risk levels, response-plan checklists, and Feishu-ready report content.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
