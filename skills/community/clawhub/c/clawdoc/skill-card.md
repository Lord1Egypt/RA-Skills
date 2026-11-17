## Description:

Clawdoc diagnoses OpenClaw and JSONL agent session failures, cost spikes, and performance issues using 14 local pattern detectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashishjaingithub](https://clawhub.ai/user/ashishjaingithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Clawdoc to inspect local agent session logs, identify reliability and cost patterns, and produce diagnosis reports with actionable prescriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private local agent session logs when an agent invokes broad diagnostic commands or natural-language triggers.

Mitigation: Prefer explicit /clawdoc commands with specific session paths and review logs before sharing generated reports.

Risk: Persistent learning writes can add diagnosis output to repository files when enabled.

Mitigation: Enable CLAWDOC_LEARNINGS=1 only in trusted repositories where .learnings/LEARNINGS.md updates are expected.

## Reference(s):

- [Clawdoc ClawHub release](https://clawhub.ai/ashishjaingithub/skills/clawdoc)
- [OpenClaw project](https://github.com/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided JSONL session files and can optionally write persistent learnings when CLAWDOC_LEARNINGS=1 is enabled.]

## Skill Version(s):

0.12.0 (source: server release metadata, frontmatter, CHANGELOG released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
