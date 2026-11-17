## Description:

Use when an agent needs to surface skill/capability candidates that first-pass registry, package, or search queries would likely miss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run find-stage discovery for skills, MCPs, CLIs, plugins, registries, extensions, SaaS/provider routes, repo tools, and native runtime capabilities. It helps produce traceable candidate pools, source gaps, query branches, and raw signals for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate pools and raw signals may be mistaken for adoption, safety, or maintenance recommendations.

Mitigation: Treat output as find-stage evidence only and review each candidate separately before installation, enablement, or operational use.

Risk: The documented upgrade routes include unpinned npx usage and unrestricted git pull commands.

Mitigation: Review the source and changes, and run upgrade commands only when the publisher and target repository are trusted.

## Reference(s):

- [Candidate Pool Contract](references/candidate-pool-contract.md)
- [Research Brief Contract](references/research-brief-contract.md)
- [Source Family Checklist](sources.yaml)
- [Curated Discovery-Source Registry](source-registries/curated-skill-lists.yaml)
- [Repository](https://github.com/its-How/aha-skills-finder)
- [ClawHub Skill Page](https://clawhub.ai/its-how/skills/aha-skills-finder)
- [Publisher Profile](https://clawhub.ai/user/its-how)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or JSON-compatible research brief and candidate pool artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Find-stage output preserves source gaps, false positives, query branches, candidate identities, and raw signals without ranking candidates for adoption.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
