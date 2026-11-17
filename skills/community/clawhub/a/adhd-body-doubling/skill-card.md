## Description:

Provides virtual ADHD body-doubling sessions with micro-step prompts, frequent check-ins, dopamine resets, and local session history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jankutschera](https://clawhub.ai/user/jankutschera)

### License/Terms of Use:

MIT

## Use Case:

External users, especially ADHD founders and productivity-focused users, use this skill to start tasks, maintain accountability during timed focus sessions, break down stuck tasks, and review local session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Focus-session details such as task descriptions, micro-steps, energy level, and outcomes may be saved locally under ~/.openclaw/skills/adhd-body-doubling/history/.

Mitigation: Avoid entering confidential task details unless local retention is acceptable, and periodically review or delete the history directory when retention is not desired.

## Reference(s):

- [Body Doubling Protocols](references/protocols.md)
- [ADHD-founder.com](https://adhd-founder.com)
- [ClawHub Skill Page](https://clawhub.ai/jankutschera/skills/adhd-body-doubling)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown conversation prompts with optional shell commands and local JSON session history files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standalone session script can save task and focus-session history under ~/.openclaw/skills/adhd-body-doubling/history/.]

## Skill Version(s):

2.1.1 (source: server release evidence; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
