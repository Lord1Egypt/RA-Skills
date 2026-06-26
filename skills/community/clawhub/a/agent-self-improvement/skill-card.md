## Description: <br>
Generic agent self-improvement skill built on OpenClaw-RL research (arxiv.org/abs/2603.10165). Captures evaluative signals (+1/-1) and directive hints from any user feedback, generates improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture user feedback, summarize evaluation scores and directive hints, and generate improvement suggestions for recurring agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently saves user feedback in a fixed local OpenClaw workspace path. <br>
Mitigation: Review or change the storage path before use, and avoid submitting secrets, personal data, or confidential content as feedback. <br>
Risk: The artifact describes prompt auto-updating and Telegram forwarding workflows without explicit approval, redaction, audit, or rollback controls. <br>
Mitigation: Require human approval before prompt changes or message forwarding, and add redaction, audit logging, and rollback procedures before enabling those workflows. <br>


## Reference(s): <br>
- [OpenClaw-RL paper](https://arxiv.org/abs/2603.10165) <br>
- [Publisher homepage](https://adelpro.us.kg) <br>
- [ClawHub skill page](https://clawhub.ai/adelpro/agent-self-improvement) <br>
- [Publisher profile](https://clawhub.ai/user/adelpro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text with JSON storage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores feedback, evaluation scores, hints, and improvement suggestions in local JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
