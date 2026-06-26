## Description: <br>
Agent Quantizer helps OpenClaw users reduce token and API overhead through session statistics, context compression, cache reuse, prompt trimming, heartbeat checks, cron auditing, model routing guidance, and skill organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tryxin](https://clawhub.ai/user/tryxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect token-heavy sessions, apply cache and compression workflows, review local automation health, and receive shell-command guidance for maintaining OpenClaw state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite session history and user prompt files with limited guardrails. <br>
Mitigation: Back up sessions and prompt files before compression or trimming, prefer dry-run modes where available, and review generated summaries before relying on them. <br>
Risk: AI-assisted compression may expose sensitive session content to a model call. <br>
Mitigation: Avoid AI compression for sessions containing secrets and use the local sliding-window mode when sensitive content may be present. <br>
Risk: Skill organization and cleanup workflows can move or remove local OpenClaw state. <br>
Mitigation: Review proposed moves and cleanup targets before confirmation, and verify backup locations before running destructive operations. <br>


## Reference(s): <br>
- [ClawHub agent-quantizer release page](https://clawhub.ai/tryxin/agent-quantizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local shell-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run previews, token statistics, cache status, file-change summaries, and configuration recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
