## Description:

Scan an OpenClaw SKILL.md file for security threats before installing it and return a safety score, detected threat patterns, and a SAFE, CAUTION, or DANGEROUS verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skillscan to check SKILL.md content before installation with a local API that reports a score, matched threat categories, verdict, and parsed skill name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may be treated as a reliable approval gate even though the security evidence describes it as a limited pattern checker.

Mitigation: Use the verdict as advisory triage only and manually review skills before installation.

Risk: Submitted SKILL.md content may contain secrets or private operational details.

Mitigation: Remove secrets and private details before scanning, and submit content only to a trusted local service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-skillscan)
- [Publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON response from a local FastAPI endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes safety_score, findings, verdict, and skill_name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
