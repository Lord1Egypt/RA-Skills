## Description: <br>
Course TA is a virtual course teaching assistant for Discord that answers course-scoped student questions from course materials and supports instructor setup, Canvas sync, admin edits, rate limiting, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-g](https://clawhub.ai/user/zeron-g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and course staff use this skill to operate a Discord-based teaching assistant that answers student questions from official course materials, routes work by course section, and supports Canvas-backed course administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to Canvas and Discord for real courses and may access student LMS records. <br>
Mitigation: Install only when the operator is authorized for the affected courses and use a least-privilege Canvas token. <br>
Risk: Course records, credentials, logs, and synchronized content may be stored in local skill data directories. <br>
Mitigation: Protect credential and data directories and disable enrollment, submission, or grade sync unless the course workflow requires it. <br>
Risk: Canvas write actions and broadcast-style communication can affect students if misconfigured or executed without review. <br>
Mitigation: Restrict broadcast permissions and require explicit instructor confirmation before announcements or other Canvas write operations. <br>
Risk: Student identity and request content may be logged, reposted to staff channels, or forwarded during support workflows. <br>
Mitigation: Give students clear notice before logging, staff-channel reposting, or forwarding their identity and request content. <br>


## Reference(s): <br>
- [Course TA on ClawHub](https://clawhub.ai/zeron-g/course-ta) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [OpenClaw](https://github.com/nichochar/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Discord replies, Markdown guidance, and inline shell commands or configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update course memory files, configuration, audit logs, and Canvas content when authorized.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
