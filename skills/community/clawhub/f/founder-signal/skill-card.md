## Description:

Founder Signal turns verified Reddit and V2EX evidence into a small, reviewable signal package for founders evaluating product demand and positioning across one or more configured product profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toliuweijing](https://clawhub.ai/user/toliuweijing)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and product teams use this skill to configure product profiles, discover Reddit and V2EX demand signals, verify candidate evidence, score findings, and generate review artifacts plus Draft review pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Draft review pages may expose configured product names, source URLs, scores, generated recommendations, and failure details because Draft publication is attempted automatically for every run.

Mitigation: Use the skill only when public Draft publication is acceptable, or require a version that keeps reviews local by default and asks before publishing.

Risk: Research quality depends on verified Reddit or V2EX evidence and saved snapshots; missing or stale evidence can produce weak or misleading demand signals.

Mitigation: Review the source URLs, verification status, selected candidate, and generated Action Card before relying on recommendations.

## Reference(s):

- [Founder Signal on ClawHub](https://clawhub.ai/toliuweijing/skills/founder-signal)
- [Draft CLI dependency](https://clawhub.ai/toliuweijing/draft-cli)
- [Founder Signal Profiles](profiles/README.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and public run reviews, JSON run artifacts and configuration, local files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes runtime artifacts under the Founder Signal home directory and attempts Draft public-page publication for each run.]

## Skill Version(s):

0.2.14 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
