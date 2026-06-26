## Description: <br>
Monitors flight prices, helps users create local watch tasks, and sends price-change alerts with flight details and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-0x7fffffff](https://clawhub.ai/user/coder-0x7fffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to watch selected flight routes, compare price changes against thresholds, and receive reminders when prices move enough to act. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel details may be sent to a fixed DingTalk recipient if DINGTALK_TARGET_ID is not changed. <br>
Mitigation: Set DINGTALK_TARGET_ID to the intended recipient before enabling alerts and verify the target in a test notification. <br>
Risk: Shell-command message sending is built from dynamic flight and message data. <br>
Mitigation: Review or patch the alert-sending path before automatic operation, and keep automatic alerts disabled until the command construction is confirmed safe. <br>
Risk: Bundled task state can contain stale route, price, or recipient-related monitoring data. <br>
Mitigation: Clear data/tasks.json before installation or first use, then create fresh tasks for the current user. <br>
Risk: Installation guidance mentions sudo npm usage for permission problems. <br>
Mitigation: Use a user-scoped Node/npm setup or another least-privilege installation method instead of sudo npm installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coder-0x7fffffff/flight-price-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/coder-0x7fffffff) <br>
- [FlyAI CLI usage documentation](references/flyai-cli-docs.md) <br>
- [Skill introduction](references/introduction.md) <br>
- [Pricing strategy](references/pricing-strategy.md) <br>
- [FlyAI documentation](https://flyai.alibaba.com/docs) <br>
- [Fliggy Open Platform](https://open.fliggy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style assistant responses with inline shell commands, flight lists, task confirmations, and DingTalk alert text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store monitoring task state in data/tasks.json and depends on FlyAI CLI plus a configured DingTalk target.] <br>

## Skill Version(s): <br>
2.2.2 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
