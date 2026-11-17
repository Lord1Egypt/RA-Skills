## Description:

Guides agents in creating programmatic videos with React and Remotion, covering project setup, composition structure, animation patterns, and rendering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold or extend Remotion projects, build React video compositions, implement deterministic animations, and produce preview and render commands for final video output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx commands can change behavior as upstream packages change.

Mitigation: Prefer pinned Remotion versions, a project-local locked CLI, and reviewed lockfiles, especially in CI.

Risk: The optional Lambda workflow uses AWS credentials and can create cloud resources.

Mitigation: Use scoped or short-lived AWS credentials, avoid exposing secrets in prompts or logs, and review AWS permissions before running Lambda commands.

## Reference(s):

- [Remotion Project Setup](references/setup.md)
- [Remotion Animation Patterns](references/animations.md)
- [Remotion Rendering Reference](references/rendering.md)
- [Remotion Lambda Rendering](references/lambda.md)
- [Remotion Lambda Documentation](https://www.remotion.dev/docs/lambda)
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-remotion-best-practices)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, markdown]

**Output Format:** [Markdown guidance with TSX code blocks and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project files such as src/Root.tsx and scene components, plus exact preview and render commands.]

## Skill Version(s):

1.0.0 (source: skill frontmatter metadata.version and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
