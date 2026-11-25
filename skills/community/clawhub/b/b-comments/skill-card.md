## Description:

Collects comments and replies from public Bilibili videos in user-approved steps, with optional CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users can collect public Bilibili video comments and replies for audience or feedback research, review results in steps, and export collected data as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious, citing behavior beyond its stated purpose, risky security settings, possible token exposure, and incomplete analysis.

Mitigation: Install only if the capability is needed and the reported risks are acceptable; review the skill before use and follow its step-by-step confirmation rules.

Risk: The documented default service URL uses plain HTTP, which can expose the account token in transit.

Mitigation: Use a trusted HTTPS service endpoint with certificate validation enabled, and keep the saved token and exported comment data private.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mystery77777777/skills/b-comments)
- [Bilibili](https://www.bilibili.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV files, Shell commands, Guidance]

**Output Format:** [JSON command results and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns incremental results per collection step; each paid step requires user confirmation. CSV exports include a BOM for spreadsheet compatibility.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
