## Description:

Works as a software developer day to day, turning a ticket into merged, shipped, supported code inside an existing codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to navigate unfamiliar codebases, scope and implement changes, diagnose bugs, improve tests, review work, plan migrations and releases, and handle on-call incidents with explicit verification and rollback thinking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable local work notes, project records, and contact records may retain sensitive work context on the machine.

Mitigation: Install only when persistent local developer memory is desired, and periodically review or clear the relevant ~/Clawic/data/ files.

Risk: Credentials or customer data could be retained if a user asks the agent to save raw sensitive content as a note.

Mitigation: Store pointers to secrets instead of values, strip customer data from saved notes, and use the skill's declared no-credential storage rule when writing memory.

## Reference(s):

- [ClawHub Developer skill page](https://clawhub.ai/ivangdavila/skills/developer)
- [Clawic Developer skill homepage](https://clawic.com/skills/developer)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, code snippets, shell commands, and local configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local developer notes under ~/Clawic/data/ when the skill is installed and used.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
