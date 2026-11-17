## Description:

Interpret Microsoft Defender for Cloud Secure Score and generate a prioritized remediation roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security teams, cloud engineers, and security leaders use this skill to analyze user-provided Microsoft Defender for Cloud Secure Score exports, recommendations, and alerts, then turn the findings into prioritized remediation work and a leadership-ready posture narrative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Azure CLI fixes may be inappropriate for a specific tenant if applied without review.

Mitigation: Review proposed changes with the responsible Azure owner and apply them through a controlled change process.

Risk: Users could accidentally provide credentials, access keys, or secret values when pasting cloud security data.

Mitigation: Use exported data or read-only CLI output only, and confirm pasted raw data contains no credentials before analysis.

Risk: Incomplete Defender exports can lead to an incomplete remediation roadmap.

Mitigation: Provide Secure Score, active recommendations, and security alerts when available, and document any missing inputs in the analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/skills/defender-posture-reviewer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, narrative sections, and inline Azure CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided exports or read-only CLI output; does not require credentials or direct Azure account access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
