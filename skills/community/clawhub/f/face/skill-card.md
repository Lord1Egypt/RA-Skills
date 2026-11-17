## Description:

Put a human face on your agent with fast avatar shortlists, gender control, transparent options, and reusable profile links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find a small set of human-looking avatar options for an agent, persona, group, or Telegram surface while keeping final selection under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Avatar search filters and page or image requests are sent to Generated Photos endpoints.

Mitigation: Use the skill only when those external requests are acceptable, and avoid sending unrelated user data in requests.

Risk: An avatar could be chosen, applied, or stored without the user's explicit intent.

Mitigation: Present a short numbered shortlist and require explicit approval before applying an avatar or suggesting long-term identity storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/face)
- [Generated Photos Face Listings](https://generated.photos/faces/beautified/{gender}/young-adult)
- [Generated Photos Image Host](https://images.generated.photos)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown with numbered links and optional inline Python extraction commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns 3 to 6 avatar options with detail, preview, and transparent preview links when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
