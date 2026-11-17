## Description:

CLI-first form builder with BYOK philosophy that generates HTML forms from JSON schemas, handles submissions through a user-provided SMTP server, and stores responses locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenix2479](https://clawhub.ai/user/phoenix2479)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create self-hosted contact, feedback, registration, survey, and lead-generation forms from JSON schemas while keeping email delivery and response storage under the user's control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned global npm CLI.

Mitigation: Pin or locally install the gatecrash-forms package and inspect the npm package source before use.

Risk: SMTP credentials may be exposed if real passwords are placed directly in shell commands or shared logs.

Mitigation: Use a secret manager, environment-specific configuration, or temporary app passwords rather than entering long-lived credentials directly in command history.

Risk: Generated response files may contain personal data from contact, feedback, registration, or survey submissions.

Mitigation: Store response files in access-controlled locations, apply retention limits, and review files before sharing or committing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phoenix2479/skills/gatecrash-forms)
- [npm Package](https://www.npmjs.com/package/gatecrash-forms)
- [Project Repository](https://github.com/Phoenix2479/gatecrash-forms)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON schemas and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HTML form files, local response files, and SMTP configuration guidance through the gatecrash-forms CLI.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
