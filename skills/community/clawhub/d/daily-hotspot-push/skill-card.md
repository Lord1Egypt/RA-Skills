## Description: <br>
A self-contained OpenClaw skill for creating, querying, updating, and removing scheduled daily news and hotspot subscriptions with timezone handling, OpenClaw cron scheduling, and QQBot-oriented delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zykkk-power](https://clawhub.ai/user/zykkk-power) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw and QQBot users use this skill to schedule recurring or test news briefings, manage delivery time and topics, and keep subscription state aligned with OpenClaw cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring cron jobs can continue sending news briefings after the user no longer wants them. <br>
Mitigation: Review created cron jobs and remove subscriptions that are no longer needed. <br>
Risk: Subscription topics, destination identifiers, and timezone settings are stored locally for delivery. <br>
Mitigation: Avoid sensitive topics or destination identifiers when that local storage or delivery-channel use is not acceptable. <br>
Risk: News content is fetched at execution time and may reflect source quality, recency, or duplication issues. <br>
Mitigation: Prefer reliable sources, filter repeated items, and keep each pushed briefing concise as described by the skill behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zykkk-power/daily-hotspot-push) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise Chinese news briefings at execution time and stores subscription and timezone state locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
