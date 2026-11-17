## Description:

Diagnoses Douyin account operational health by retrieving RedFox profile and recent content data, scoring account quality across multiple dimensions, and producing risk alerts plus optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External Douyin operators, creators, MCNs, brands, and business development teams use this skill to assess account health, benchmark competitors, screen potential partners, and prioritize improvements from account and recent-content metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried Douyin nicknames or IDs are sent to RedFox and returned profile and work metadata may be displayed in the report.

Mitigation: Disclose the external RedFox lookup to the user and require explicit confirmation before submitting account identifiers.

Risk: The artifact includes behavior that can fall back to a shared embedded RedFox API key.

Mitigation: Remove or rotate the embedded default key and require a user-provided REDFOX_API_KEY before external lookups.

Risk: Providing secrets through command-line arguments can expose them through shell history, logs, or process listings.

Mitigation: Prefer environment variables or a secret manager for RedFox credentials and avoid passing API keys with --api-key.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/douyin-account-diagnosis-redfox)
- [README](README.md)
- [English README](README.en.md)
- [Core Workflow](references/core_workflow.md)
- [Diagnosis Rules](references/diagnosis_rules.md)
- [API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown diagnostic report with tables, scores, risk alerts, recent-content details, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include returned Douyin profile fields, recent work metadata, engagement metrics, risk labels, and clickable content links.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
