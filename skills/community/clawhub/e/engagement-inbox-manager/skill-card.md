## Description:

Engagement Inbox Manager helps agents triage social comments, DMs, and mentions, classify register and commenter type, draft ranked human-posted replies, manage escalation paths, and collect UGC permission candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Social, support, and community teams use this skill to turn exported or pasted inbox batches into a prioritized triage report with draft replies, SLA deadlines, escalation rows, moderation notes, and UGC permission candidates for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosts that rely on manifest capabilities may not expect persistent record writes or registry proposal access.

Mitigation: Review installation metadata before deployment and grant only the documented scoped write access and controlled registry proposal access, or disable writes.

Risk: Pasted comments, DM exports, screenshots, and UGC permission claims may contain untrusted instructions or incomplete rights evidence.

Mitigation: Treat inbox content as untrusted input, ignore embedded instructions, and verify explicit permission evidence before recording candidates or reposting UGC.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aaron-he-zhu/skills/engagement-inbox-manager)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown triage report with ranked draft replies, tables, escalation notes, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All replies are drafts for human posting; the skill does not auto-send or automate platform engagement.]

## Skill Version(s):

19.0.0 (source: evidence.release.version, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
