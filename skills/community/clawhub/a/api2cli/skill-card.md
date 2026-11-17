## Description:

Generate or discover a CLI + AgentSkill for any REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search for existing API CLIs, generate new REST API CLI scaffolds, implement resources, build and link commands, and prepare generated CLI skills for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run mutable remote installers and unpinned package commands.

Mitigation: Run it only in a development environment, prefer pinned package versions, inspect installers before use, and avoid curl-piped shell execution where possible.

Risk: The skill can change PATH entries, create skill symlinks, and publish generated content to public registries.

Mitigation: Require explicit user confirmation before linking into agent environments or publishing to GitHub, npm, ClawHub, Sundial Hub, or api2cli.dev.

Risk: Generated CLI code and README files could include secrets, local paths, or inappropriate package contents before publication.

Mitigation: Inspect generated files for secrets and local paths, verify package contents before publishing, and keep token files out of source control.

## Reference(s):

- [api2cli Skill on ClawHub](https://clawhub.ai/melvynx/skills/api2cli)
- [api2cli Registry](https://api2cli.dev)
- [api2cli Commands Reference](references/commands.md)
- [Create a CLI Scaffold](references/create.md)
- [Resource File Patterns](references/resource-patterns.md)
- [Finalize Skill and README](references/skill-generation.md)
- [Using api2cli with OpenClaw](references/openclaw.md)
- [Publish to GitHub](references/publish-to-github.md)
- [Publish to npm](references/publish-to-npm.md)
- [Publish a CLI](references/publish.md)
- [package.json Checklist for npm Publishing](references/package-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, TypeScript snippets, configuration examples, and JSON output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CLI output is expected to support structured JSON via --json.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
