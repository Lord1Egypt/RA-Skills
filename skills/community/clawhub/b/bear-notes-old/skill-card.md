## Description:

Create, search, and manage Bear notes via grizzly CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, read, search, update, and manage Bear notes on macOS through the grizzly CLI. It is useful for agents that need to propose or execute note-management commands while respecting Bear and grizzly configuration requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party grizzly CLI that can read or modify Bear notes when invoked.

Mitigation: Review and pin the grizzly CLI version before installation where possible, and confirm commands before running them against important notes.

Risk: Bear API tokens can be exposed if typed directly into shell commands or stored with broad permissions.

Mitigation: Store the token in ~/.config/grizzly/token with owner-only permissions and pass it through --token-file rather than placing the token directly in command history.

## Reference(s):

- [Bear](https://bear.app)
- [Grizzly Go module](https://pkg.go.dev/github.com/tylerwince/grizzly/cmd/grizzly)
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/skills/bear-notes-old)
- [Publisher profile](https://clawhub.ai/user/huangfeng1995)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and TOML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS with Bear installed and the grizzly CLI available; some operations require a Bear API token.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
