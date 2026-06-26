## Description: <br>
Generate or discover a CLI + AgentSkill for any REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find existing REST API CLIs, generate new CLI scaffolds, implement resources, build and link tools, and prepare generated CLIs or skills for publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through installing developer tools, linking executables and skills, and modifying local files. <br>
Mitigation: Require explicit user approval before installs, symlinks, deletions, or other environment-changing commands. <br>
Risk: Publishing workflows may expose code, generated skills, package metadata, or credentials if files are not reviewed first. <br>
Mitigation: Inspect generated files for secrets and confirm authentication state before any GitHub, npm, ClawHub, Sundial Hub, or registry publish step. <br>
Risk: The scanner summary says the skill gives broad install, linking, publishing, and deletion authority without enough confirmation gates. <br>
Mitigation: Treat install, remove, force-push, repository creation, npm publish, and registry publish actions as approval-gated operations. <br>


## Reference(s): <br>
- [api2cli Commands Reference](references/commands.md) <br>
- [Create a CLI Scaffold](references/create.md) <br>
- [Resource File Patterns](references/resource-patterns.md) <br>
- [Finalize Skill and README](references/skill-generation.md) <br>
- [Using api2cli with OpenClaw](references/openclaw.md) <br>
- [Publish to GitHub](references/publish-to-github.md) <br>
- [Publish to npm](references/publish-to-npm.md) <br>
- [Publish a CLI](references/publish.md) <br>
- [package.json Checklist for npm Publishing](references/package-checklist.md) <br>
- [api2cli Registry](https://api2cli.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated CLI commands should use --json when called programmatically.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
