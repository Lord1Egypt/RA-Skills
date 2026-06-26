## Description: <br>
Agent Sbti runs a 20-question SBTI personality test, summarizes the user's style, and generates or applies an OpenClaw SOUL.md personality configuration in complement, same-style, mixed, or custom modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users can take a personality questionnaire and configure an agent's communication and behavior style. The skill supports preview, confirmation, backup, and rollback flows for SOUL.md configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently modify the agent's SOUL.md configuration. <br>
Mitigation: Review the generated configuration preview before confirming, keep backups enabled, and use rollback if the resulting agent behavior is not desired. <br>
Risk: Activation and confirmation handling is broad for a skill that changes persistent configuration. <br>
Mitigation: Use clear SBTI test/configuration prompts and confirm only after inspecting the exact change; prefer narrower trigger and confirmation handling before broad deployment. <br>
Risk: Backup and rollback routines operate on local persistent configuration files. <br>
Mitigation: Verify the backup path exists and test rollback in a non-critical workspace before relying on it for important configurations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/torchesfrms/agent-sbti) <br>
- [README.md](artifact/README.md) <br>
- [SPEC.md](artifact/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation responses with SOUL.md configuration snippets and JSON-like change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write to ~/.openclaw/workspace/SOUL.md after confirmation and stores backups under ~/.openclaw/workspace/backup/agent-sbti/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
