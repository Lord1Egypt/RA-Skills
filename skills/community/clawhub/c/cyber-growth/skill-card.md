## Description:

Cyber Growth is a cyberpunk and EVA-themed personal growth tracker that records XP events, shows progress dashboards, generates weekly and monthly reports, and can prepare optional Feishu Bitable sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m17y](https://clawhub.ai/user/m17y)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to track personal growth, task completion, learning, fixes, and skill-area progress through local shell commands and scheduled reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic activity logging can capture sensitive work details in local growth records or scheduled reports.

Mitigation: Require explicit opt-in before automatic logging or external reporting, and avoid recording secrets or sensitive task details.

Risk: Crafted logged text may trigger local command execution because inputs are not safely serialized.

Mitigation: Fix the scripts to serialize user-controlled values safely before writing JSON or passing values into embedded Python and shell commands.

Risk: Invalid XP, date, or month values can corrupt tracking data or produce unreliable reports.

Mitigation: Validate numeric XP and date/month inputs before recording or settlement.

## Reference(s):

- [Cyber Growth Skill Page](https://clawhub.ai/m17y/skills/cyber-growth)
- [Publisher Profile](https://clawhub.ai/user/m17y)
- [Skill Tree](references/skill-tree.md)
- [Protocols](references/protocols.md)
- [Cyber Lexicon](references/cyber-lexicon.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown-style reports with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON and JSONL growth records under the user's OpenClaw memory directory when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
