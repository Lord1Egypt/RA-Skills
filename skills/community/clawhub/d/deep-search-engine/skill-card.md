## Description:

Searches Chinese and international channels for published material, checks candidate pages against titles, publication dates, and text fingerprints, and returns confidence-graded findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Communications and research teams use this skill to check whether a release or article appeared, trace reposts, and map coverage across available search channels. It checks candidate pages for title, publication-date, and body-fingerprint evidence, then reports confidence levels and unresolved items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may disclose confidential or unpublished material to external search services.

Mitigation: Use only material approved for external searching; omit confidential or unpublished details unless disclosure is acceptable.

Risk: Search and verification results can be unreliable; dates or fingerprints may come from unrelated or non-visible page content, and a PASS may lack date evidence.

Mitigation: Treat script results as candidate signals. Confirm the publication date from page metadata or an attributed date line and confirm fingerprint matches in visible article text before reporting a high-confidence result.

Risk: Some referenced paths were unresolved during scanning, leaving partial coverage.

Mitigation: Review the source set and unresolved references before relying on findings, and describe coverage limits and pending items in the report.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haiyangchenbj/skills/deep-search-engine)
- [Channel Matrix](artifact/references/channel-matrix.md)
- [Media Pool](artifact/references/media-pool.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Confidence-graded findings JSON with a concise human-readable summary and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification evidence, confidence levels, and items requiring follow-up.]

## Skill Version(s):

0.4.1 (source: evidence.json release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
