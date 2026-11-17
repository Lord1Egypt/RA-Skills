## Description:

Andrew Google Tasks helps an agent manage Google Tasks task lists and tasks through OAuth 2.0, including listing, creating, updating, completing, and deleting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibluewind](https://clawhub.ai/user/ibluewind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users who want an agent to operate Google Tasks can use this skill to list task lists, create tasks with notes and due dates, update or complete tasks, and delete tasks after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests full Google Tasks access and can create, update, complete, or delete tasks.

Mitigation: Grant access only to an appropriate Google account and review task deletion or update actions before invoking them.

Risk: The OAuth token is stored and reloaded through a local Python pickle file, which could execute local code if the file is tampered with.

Mitigation: Replace pickle token storage with Google's JSON credential serialization where possible, keep credential and token files private, and regenerate the token if tampering is suspected.

Risk: The skill runs local Python code and depends on Google API packages installed in the local environment.

Mitigation: Install dependencies in a virtual environment with pinned versions and review the script before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibluewind/skills/andrew-google-tasks)
- [Google Tasks OAuth scope](https://www.googleapis.com/auth/tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Tasks OAuth credentials and local Python dependencies.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
