## Description:

Creates guidance and shell commands for setting up an educational subagent that records and tracks class lesson progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2070super](https://clawhub.ai/user/2070super)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, teaching coordinators, and agent developers use this skill to create a course-progress tracking subagent that records class coverage, answers progress queries, and maintains lesson-outline status. It also provides troubleshooting guidance for OpenClaw runtime selection and permission approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an approval command that can grant broad OpenClaw admin, approval, pairing, write, and secrets-related permissions.

Mitigation: Inspect the exact pending OpenClaw request before approval, grant only privileges that are necessary for the course-progress subagent, and avoid running the approval script by default.

Risk: A course-progress tracking subagent may not require broad administrative or secrets-related scopes.

Mitigation: Use the least-privilege OpenClaw scopes available for subagent creation and course-progress recording.

## Reference(s):

- [Create Educational Subagent on ClawHub](https://clawhub.ai/2070super/skills/create-educational-subagent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and companion shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw permission approval and subagent creation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
