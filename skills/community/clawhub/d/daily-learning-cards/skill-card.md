## Description: <br>
Daily Learning Cards extracts learning topics, decisions, pitfalls, concepts, and notable quotes from OpenClaw conversation memory, then generates daily cards, weekly summaries, and weekly exams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlarkspur](https://clawhub.ai/user/vlarkspur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to turn daily AI conversations across channels such as Feishu, WebUI, DingTalk, WeCom, and QQBot into reviewable learning cards, weekly summaries, and quiz material. It is intended for users who want scheduled capture, consolidation, delivery, and self-testing of conversation-derived knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes private OpenClaw conversation memory and may retain summaries or raw excerpts. <br>
Mitigation: Require explicit opt-in, limit enabled source channels, add redaction before processing, and define retention or deletion controls for generated cards, backups, and summaries. <br>
Risk: Scheduled cron jobs can automatically send derived conversation content to external messaging destinations. <br>
Mitigation: Verify recipients before enabling cron, require user confirmation for delivery targets, and disable outbound delivery until the configured target is reviewed. <br>
Risk: Artifact behavior includes hardcoded Feishu targets and a hardcoded API key for external AI processing. <br>
Mitigation: Replace hardcoded destinations and credentials with user-provided configuration or environment secrets, rotate exposed credentials, and require explicit consent before external AI calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlarkspur/daily-learning-cards) <br>
- [Publisher profile](https://clawhub.ai/user/vlarkspur) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [extract-rules.md](artifact/prompts/extract-rules.md) <br>
- [summary-template.md](artifact/prompts/summary-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown learning cards and summaries, generated exam text, JSON extraction data, shell command guidance, and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled daily and weekly outputs; stores cards and related learning material under OpenClaw memory paths and can deliver summaries to configured messaging channels.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
