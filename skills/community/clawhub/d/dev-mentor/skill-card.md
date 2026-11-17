## Description:

Guides experienced developers through learning an unfamiliar technical field by building a project from start to finish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a conversational mentor when they want to learn an unfamiliar development area through a hands-on project. It currently guides learning in backend development, databases, server deployment, and Rust.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database migration guidance could affect existing data if applied without safeguards.

Mitigation: Back up the database, review the migration and rollback plan, and test it in a staging environment before applying it to production data.

Risk: SSH hardening steps could lock the operator out of a server.

Mitigation: Keep the current SSH session open, confirm alternate console access, and test a new SSH connection before closing the existing session.

## Reference(s):

- [Dev Mentor on ClawHub](https://clawhub.ai/z-zihan/skills/dev-mentor)
- [Project homepage](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Conversational Markdown with explanations, code examples, and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts explanations to the learner's experience and pauses between project steps for feedback.]

## Skill Version(s):

2.1.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
