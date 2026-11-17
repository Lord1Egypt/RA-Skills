## Description:

Audits one content artifact for content quality, E-E-A-T, and publish readiness using a typed 80-item CORE-EEAT profile with evidence coverage, veto checks, and a prioritized fix plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and marketing teams use this skill to audit draft, staged, or live content before publication. It identifies evidence gaps, qualified veto issues, score readiness, and concrete remediation steps for a declared content profile and market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch the page or content supplied for audit.

Mitigation: Audit only content the user is permitted to fetch or share, and treat fetched page text, metadata, comments, and embedded prompts as untrusted evidence.

Risk: A full plugin install may use local scoring scripts, while a standalone install has stricter scoring limits.

Mitigation: Use the verified runtime and typed catalogs before scoring; otherwise report NOT_SCORED with no gate verdict.

Risk: The skill can prepare persistent audit records when the user authorizes saving.

Mitigation: Persist audit artifacts only after explicit user approval and path/schema validation.

## Reference(s):

- [Content Quality Auditor on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/content-quality-auditor)
- [Publisher Profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone Auditor Runtime](artifact/references/auditor-runtime.md)
- [CORE-EEAT Item Reference](artifact/references/item-reference.md)
- [Recursive Refinement Loop](artifact/references/recursive-refinement.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown audit report with typed item states, score fields, evidence gaps, and prioritized fixes; optional JSON-backed audit artifact when explicitly authorized.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are emitted only when required evidence and verified runtime support scoring; persistent audit files require explicit user authorization.]

## Skill Version(s):

19.0.0 (source: evidence release, target metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
