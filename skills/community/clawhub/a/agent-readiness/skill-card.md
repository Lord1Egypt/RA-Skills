## Description:

Run website agent readiness audits (AEO, llms.txt, structured data, AI crawler access), preview branch audits, changed-page sitemap audits, local/private preview audits with explicit opt-in, sitemap origin rewriting, static-output audits, regression comparisons, site fixes, schema validation, and llms.txt generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arberx](https://clawhub.ai/user/arberx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and website operators use the skill to assess a site's readiness for AI discovery, structured data, and crawler access, compare audits over time, and generate or apply targeted site improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scanning covered only part of the listed components, and tool-misuse analysis was degraded.

Mitigation: Review the release contents and requested tool actions before running the skill.

Risk: The package can change within major version 8.

Mitigation: Review the exact package release before installation and use a pinned version when repeatable behavior is required.

Risk: There may be a mismatch between fix instructions and declared write permissions.

Mitigation: Review proposed file changes and limit writes to the intended site files before applying fixes.

## Reference(s):

- [Canonry Agent Readiness](https://canonry.ai)
- [Project repository (linked in skill frontmatter)](https://github.com/Canonry/agent-readiness)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Configuration files]

**Output Format:** [JSON and Markdown audit reports, recommendations, and optional website content or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce llms.txt, llms-full.txt, robots.txt, or entities.json; site fixes can modify project files.]

## Skill Version(s):

8.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
