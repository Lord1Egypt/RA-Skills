## Description:

Audits a public website's technical readiness for AI answer engines and produces a prioritized, evidence-backed fix list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aureliusclaw](https://clawhub.ai/user/aureliusclaw)

### License/Terms of Use:

MIT

## Use Case:

Website owners and developers use geo-scan to assess whether public pages are crawlable and quotable by answer engines, then prioritize technical and content improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because of gaps in its stated time limits and robots.txt and file-read scope; the scan evidence is incomplete.

Mitigation: Review the stated time limits, robots.txt handling, and file-read scope before installing, and treat the scan as partial.

## Reference(s):

- [Source repository](https://github.com/AureliusClaw/geo-scan)
- [ClawHub skill release](https://clawhub.ai/aureliusclaw/skills/geo-scan)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [A scored website audit with evidence, prioritized actions, and per-page findings, as text, Markdown, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores technical readiness; it does not establish whether an answer engine will cite a site.]

## Skill Version(s):

1.2.7 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
