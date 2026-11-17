## Description:

Build, inspect, update, and call hosted personal apps with the Charming CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charming](https://clawhub.ai/user/charming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, inspect, update, call, and manage hosted personal apps on Charming. It is most useful when building small interactive apps that need a backend manifest, routes, persistent storage, a browser UI, and CLI-driven deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through create, update, delete, and public-sharing actions that change hosted apps.

Mitigation: Review dry-run output before mutations and require explicit user approval before passing confirmation flags such as --yes.

Risk: Installing or running the Charming CLI depends on trusting the Charming service and the usecharming npm package source.

Mitigation: Install only from a trusted package source and prefer a pinned or otherwise verified CLI version where possible.

Risk: Credentials and API secrets may be exposed if copied into app source, logs, URLs, or agent-visible output.

Mitigation: Do not print tokens or device codes, show only login user codes when needed, and prefer header-based secret placeholders over query-string secrets unless an API requires query parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charming/skills/charming)
- [Charming website](https://usecharming.com)
- [Charming app manifest schema](https://charm.ing/schema/app-manifest/2026-07-31.json)
- [Contract reference](artifact/resources/contract.md)
- [Patterns reference](artifact/resources/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI workflow guidance, dry-run checks, app contract constraints, sandbox rules, and hosted app implementation patterns.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
