## Description: <br>
Provides a unified quota dashboard for Antigravity, GitHub Copilot, and OpenAI Codex, with model routing recommendations and reset and risk indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kr1json](https://clawhub.ai/user/kr1json) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to check provider login status, quota levels, reset timing, and task-specific model recommendations before selecting an AI model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw and Codex account state to determine provider login and quota status. <br>
Mitigation: Review the skill before installing and run it only in environments where reading those local account files is acceptable. <br>
Risk: The skill sends stored provider tokens to provider quota endpoints while checking quotas. <br>
Mitigation: Use it only with accounts and network destinations you trust, and prefer a version with explicit local-only or refresh controls. <br>
Risk: The skill makes a small Codex request during checks to refresh quota information. <br>
Mitigation: Run it only when an explicit refresh is acceptable, and monitor for unintended quota usage. <br>
Risk: Dashboard output can include account and quota details. <br>
Mitigation: Avoid sharing raw output outside trusted contexts and redact account-specific details when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kr1json/ai-quota-check) <br>
- [Publisher profile](https://clawhub.ai/user/kr1json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown dashboard with tables and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and codex binaries; may make provider quota requests and a small Codex request during checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
