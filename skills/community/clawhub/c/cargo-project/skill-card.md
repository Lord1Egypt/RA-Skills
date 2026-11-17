## Description:

Manages a Cargo workspace as code by defining resources in TypeScript, previewing changes, and deploying them repeatably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to define multi-resource Cargo projects in TypeScript, review planned changes, and deploy repeatable workspace configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a destructive all-resources command outside the skill's declared purpose.

Mitigation: Review the command and target carefully before execution, and inspect the project plan before deploying changes.

Risk: The security assessment reports unpinned package and skill installers.

Mitigation: Review installer sources and pin versions to releases that have been checked before installing.

Risk: The security assessment calls out contact data flows and automatic deployment behavior for review.

Mitigation: Check which contact data the project handles and when deployments run before connecting a workspace or enabling automatic deployment.

Risk: One referenced guide was only partially analyzed by the security scan.

Mitigation: Read the relevant guide and review the skill before relying on its instructions.

## Reference(s):

- [Project homepage](https://github.com/getcargohq/cargo-skills)
- [Cargo Project on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-project)
- [Command reference](artifact/references/commands.md)
- [Resource reference](artifact/references/resources.md)
- [Deploy and state guide](artifact/guides/deploy-and-state.md)
- [Cookbook examples](https://github.com/getcargohq/gtm-skills)

## Skill Output:

**Output Type(s):** [Guidance, TypeScript code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with TypeScript examples, configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repeatable project files and deployment plans based on the requested workspace changes.]

## Skill Version(s):

5.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
