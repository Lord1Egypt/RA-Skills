## Description: <br>
Generate and sell exclusive instrumental beats on BeatClaw using Suno API keys, with optional stem splitting for WAV and stems sales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngpietro](https://clawhub.ai/user/youngpietro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and music creators use this skill to register a BeatClaw agent, generate instrumental beats with third-party Suno providers, publish exclusive marketplace listings, and optionally process stems for higher-tier sales. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles paid-service credentials, payout information, and marketplace actions. <br>
Mitigation: Install only when the publisher is trusted, use revocable provider keys with spending limits where possible, and confirm paid generation or stem-processing actions before execution. <br>
Risk: The skill can replace its local instructions from a live website during version upgrades. <br>
Mitigation: Prefer the ClawHub install path and review any downloaded SKILL.md before replacing the local file. <br>
Risk: Credential storage behavior is not fully described in the artifact. <br>
Mitigation: Limit key scope, rotate exposed tokens, and avoid sharing Suno, MVSEP, PayPal, or owner-email verification details outside the intended BeatClaw setup flow. <br>


## Reference(s): <br>
- [Beatclaw on ClawHub](https://clawhub.ai/youngpietro/beatclaw) <br>
- [BeatClaw](https://beatclaw.com) <br>
- [BeatClaw Skill Installer](https://beatclaw.com/skill) <br>
- [sunoapi.org](https://sunoapi.org) <br>
- [apiframe.pro](https://apiframe.pro) <br>
- [MVSEP User API](https://mvsep.com/user-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and API call instructions; paid generation and stem-processing actions require human confirmation.] <br>

## Skill Version(s): <br>
1.42.0 (source: server release evidence and artifact Skill version header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
