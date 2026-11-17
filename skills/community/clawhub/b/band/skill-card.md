## Description:

Use BAND through the band-mcp tools to review groups, posts, notices, comments, events, members, and recent chat activity, or to publish a post or comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People who belong to BAND groups can use this skill to review group activity, announcements, posts, comments, calendar events, members, and recent chat messages. It can also publish a post or comment after the user reviews and explicitly confirms the preview.

### Deployment Geography for Use:

Global (connects only to BAND's US API host)

## Known Risks and Mitigations:

Risk: The security review found no issues, but it was partial and two references could not be resolved.

Mitigation: Consider that uncertainty when deciding whether to install; the review is favorable but incomplete.

Risk: Published posts and comments are visible to band members, may trigger notifications, and cannot be undone through this skill.

Mitigation: Review the preview and require explicit user confirmation before submitting; make later edits or deletions in BAND.

## Reference(s):

- [BAND](https://band.us)
- [@chrischall/band-mcp on npm](https://www.npmjs.com/package/@chrischall/band-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and confirmation previews; chat access is limited to the latest message per channel.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
