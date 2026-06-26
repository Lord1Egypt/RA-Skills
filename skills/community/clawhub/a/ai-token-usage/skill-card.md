## Description: <br>
AI Token消耗监控 reads local OpenClaw session logs to summarize token usage, detect abnormal consumption, and suggest optimization steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local session logs, understand token usage and cost patterns, and identify unusually high consumption before it leads to overspend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs to calculate token usage. <br>
Mitigation: Use it only where local session log access is acceptable, and require confirmation before log access if accidental invocation is a concern. <br>
Risk: The skill stores aggregate usage statistics locally. <br>
Mitigation: Review generated memory/token-usage-YYYY-MM-DD.json files according to local retention and privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/ai-token-usage) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save aggregate token usage statistics as local JSON files under memory/token-usage-YYYY-MM-DD.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
