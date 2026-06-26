## Description: <br>
AI-powered context management for OpenClaw sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect session token usage, generate AI summaries, and optionally compress long sessions by resetting and reinjecting summarized context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local OpenClaw session history and preserve full conversation backups. <br>
Mitigation: Run read-only summarize first, inspect generated summaries for secrets or stale instructions, and keep backups in trusted local storage. <br>
Risk: Using replace mode can reset and rewrite an OpenClaw session with compressed context. <br>
Mitigation: Use --replace only with an explicit session key after confirming the backup location and summary accuracy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plgonzalezrx8/context-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write summaries and session backups under memory/compressed/ and update config.json when commands are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
