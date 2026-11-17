## Description:

Virtual course teaching assistant for Discord that answers course-related questions using RAG over course materials and supports professor-administered Canvas LMS sync, dashboard, and update workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeron-g](https://clawhub.ai/user/zeron-g)

### License/Terms of Use:

MIT-0

## Use Case:

Course instructors and teaching staff use this skill to run a Discord-based virtual teaching assistant that answers student course questions from indexed official materials. Professors can also use it to sync Canvas content, route multiple course sections, review dashboards, and manage approved course information updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines student-facing Q&A with broad Canvas admin capabilities, sensitive student-data access, persistent indexing, and audit logging.

Mitigation: Deploy it as an instructor/admin tool with a least-privilege Canvas token, staff-only log channels, explicit student notice for logging or forwarding, and only the Canvas sync scopes needed for the course.

Risk: Canvas content sync and file handling can expose unsafe filename containment or Canvas URL origin validation issues when processing untrusted course content.

Mitigation: Fix filename containment and validate Canvas URL origins before syncing untrusted Canvas content; keep enrollment and discussion-reply sync disabled unless there is a concrete instructional need.

Risk: Canvas write operations, such as announcements or grade-related updates, can affect live courses if triggered incorrectly.

Mitigation: Restrict write commands to configured administrator users, show the exact target and content before execution, require explicit confirmation, and log all Canvas writes.

## Reference(s):

- [Course TA on ClawHub](https://clawhub.ai/zeron-g/skills/course-ta)
- [Course TA Setup Guide](references/setup-guide.md)
- [OpenClaw](https://github.com/nichochar/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with optional shell commands and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces student-facing answers, professor/admin confirmations, Canvas dashboard summaries, audit log entries, and markdown memory files for retrieval.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
