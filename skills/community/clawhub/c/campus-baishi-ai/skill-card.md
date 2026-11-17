## Description:

校园百事 is a Chinese-language campus guide assistant that helps students query and share school-specific forum submissions about dining, housing, study spaces, campus tips, Q&A, reports, and nearby activities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangleizhui](https://clawhub.ai/user/kangleizhui)

### License/Terms of Use:

MIT-0

## Use Case:

Students and campus community users use this skill to retrieve school-specific campus information from submitted forum records, contribute new campus tips, ask anonymous questions, and report problematic content. Agents using the skill are guided to bind a user's school, avoid fabricating missing records, and route posts into campus categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to collect and store forum passwords in plaintext.

Mitigation: Do not send passwords to this skill or allow reusable passwords to be stored in JSON; require forum-native login or scoped tokens before deployment.

Risk: The skill retains account and school binding data and includes inconsistent privacy expectations.

Mitigation: Clearly disclose retained account and school data, minimize stored data, and provide deletion and correction paths.

Risk: Image content from forum posts may be processed by a vision service.

Mitigation: Disclose image processing behavior, limits, and deletion options before relying on the skill with user-submitted media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangleizhui/skills/campus-baishi-ai)
- [Flarum read/search API reference](references/flarum-read-api.md)
- [Campus forum](https://xysq.kcucu.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Chinese natural-language responses with optional Markdown, API request guidance, and local JSON account configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce forum search, registration, posting, reporting, and image-description requests against the campus forum service.]

## Skill Version(s):

1.0.6 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
