## Description:

ClawDoctor is a behavioral cost coach for OpenClaw fleets that analyzes sessions, identifies technical and behavioral cost waste, and produces cost reports with optional configuration fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nabilrehman](https://clawhub.ai/user/nabilrehman)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw fleet operators use ClawDoctor to review agent usage costs, understand costly session patterns, and decide whether to apply cost-saving configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private chat histories and fleet usage data during cost analysis.

Mitigation: Run it manually first, limit use to environments where transcript access is acceptable, and confirm consent and retention expectations before scheduled runs.

Risk: The skill can change fleet settings through configuration patches with weak confirmation controls.

Mitigation: Review the exact patch, affected agents, global impact, and rollback plan before allowing any fix to be applied.

Risk: Daily cron execution may repeatedly analyze sensitive history and incur avoidable analysis cost.

Mitigation: Avoid daily cron until the team has approved access, retention, and expected run cost for the fleet.

## Reference(s):

- [ClawDoctor Skill Page](https://clawhub.ai/nabilrehman/skills/clawdoctor)
- [Fix Payloads & Model Tiers](artifact/references/fix-payloads.md)
- [Report Formats](artifact/references/report-formats.md)
- [Faan AI](https://faan.ai)
- [Nabil Rehman](https://www.linkedin.com/in/nabilrehman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration/state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write pending-fixes and last-analysis state files; can propose or apply OpenClaw configuration patches after user review.]

## Skill Version(s):

4.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
