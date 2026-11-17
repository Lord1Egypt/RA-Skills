## Description:

Compares dev, staging, and production configuration differences and translates technical changes into business-risk-focused review notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill for environment troubleshooting, pre-release configuration reviews, and configuration governance across dev, staging, and production inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include file paths, internal URLs, or partially masked secret-like values from supplied configuration inputs.

Mitigation: Run the skill on narrow copied or sanitized config sets and review generated reports before sharing them.

Risk: The output may not provide a full semantic dev, staging, and production diff without additional review.

Mitigation: Treat the generated report as a review aid and verify high-risk differences against the source configurations and deployment ownership.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/env-diff-explainer)
- [Skill specification](resources/spec.json)
- [Output template](resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report or JSON payload, with human-facing review guidance when script execution is unavailable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review output; suspected secrets are masked on a best-effort basis, and high-risk changes are presented as review or dry-run suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
