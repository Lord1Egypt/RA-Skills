## Description:

Turns a company name, six-digit A-share code, or supplied watchlist into a dated announcement digest with exact titles, source locations, and key figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

A-share investors and research teams use this skill to list a company’s or supplied watchlist’s announcements for a chosen date window, with each item tied to its published title, date, and source. It marks unavailable information explicitly and leaves ratings, target prices, and market outlook for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential use with a dynamically chosen service and installation from unpinned sources as review-worthy risks.

Mitigation: Verify the API key destination independently and pin the installer and source to reviewed versions before installation.

Risk: Company or watchlist data may be sent externally, and the host’s granted file access may affect exposure.

Mitigation: Check what data will be sent and review the file access granted to the host before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-announcement-daily-cn)
- [Cue data access setup](https://cuecue.cn/hub/mcp)
- [Cue document reader setup](https://cuecue.cn/hub/omni-reader)
- [Cue API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown announcement digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A dated, itemized list with exact announcement titles, key figures, source locations, related-item comparisons, and explicitly named missing information; investment judgments are marked for human review.]

## Skill Version(s):

0.1.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
