## Description: <br>
Cyber Growth is a cyberpunk/EVA-themed personal growth tracker that records XP events, status dashboards, reports, milestones, and optional automated daily settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m17y](https://clawhub.ai/user/m17y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other ClawHub users use this skill to track personal growth events, XP, domains, milestones, and periodic progress reports from agent work. It supports manual command use and optional automation for event accumulation, nightly settlement, and morning reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent automatic logging can capture work activity or sensitive text beyond a user's intent. <br>
Mitigation: Use manual mode or explicit opt-in automation only, and avoid recording secrets, credentials, private customer details, or untrusted text. <br>
Risk: Scheduled reports or Feishu-style forwarding can disclose growth records to unintended recipients. <br>
Mitigation: Enable cron, heartbeat reports, or forwarding only after recipients, channels, and data fields are reviewed. <br>
Risk: The record-writing implementation has unsafe input handling when passing shell inputs into Python. <br>
Mitigation: Fix input handling before automatic logging, and review script changes before deployment. <br>


## Reference(s): <br>
- [Cyber Growth ClawHub release](https://clawhub.ai/m17y/cyber-growth) <br>
- [Skill Tree](references/skill-tree.md) <br>
- [Protocols](references/protocols.md) <br>
- [Cyber Lexicon](references/cyber-lexicon.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write local JSON and JSONL growth records under ~/.openclaw/memory; optional Feishu forwarding is available when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
