## Description:

Active Learning Agent continuously observes Feishu workplace context, builds timelines across messages, meetings, documents, and calendar events, and proactively delivers analyses, summaries, alerts, and drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cscguochang](https://clawhub.ai/user/cscguochang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams using Feishu can use this skill to track evolving work topics across private chats, group chats, meetings, recordings, documents, and calendars. It helps assemble timelines, surface inconsistencies, prepare concise summaries, and draft follow-up artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests recurring access to private Feishu chats, meetings, recordings, documents, and calendars, which can expose sensitive workplace content.

Mitigation: Require explicit source-by-source consent, disable private chats and transcripts by default, and limit access to only the sources needed for the user's workflow.

Risk: The skill stores long-term summaries and work profiles in memory files.

Mitigation: Define retention, review, correction, and deletion controls for memory files before enabling recurring runs.

Risk: The skill can send outbound Feishu messages based on inferred context.

Mitigation: Keep outbound messages private unless the user confirms sharing, and review drafts before sending to broader channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cscguochang/skills/active-learning-agent)
- [Artifact README](artifact/README.md)
- [Artifact Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and concise Feishu-ready text with optional document drafts and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent memory and activity logs when deployed with the configured Feishu tools.]

## Skill Version(s):

2.4.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
