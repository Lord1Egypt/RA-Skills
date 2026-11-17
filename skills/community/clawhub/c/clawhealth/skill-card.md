## Description:

Performs a two-phase audit with a fast structural scan and a detailed expert review focusing on security, cron jobs, config, and skill quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlinrabens](https://clawhub.ai/user/merlinrabens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit local OpenClaw installations, cron jobs, configuration, skills, and possible security hygiene issues before publishing or during periodic health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw configuration, cron prompts, skills, workspace files, and possible secrets during deeper review.

Mitigation: Run the quick Phase 1 scan first, review the reported paths, and give explicit permission before Phase 2 opens files likely to contain credentials or customer data.

## Reference(s):

- [ClawCheck README](README.md)
- [Remediation Guide](references/remediation.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Configuration guidance]

**Output Format:** [JSON for the deterministic scan and Markdown for the deep audit report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python 3 and inspects local OpenClaw files.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
