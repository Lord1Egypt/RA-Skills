## Description:

Guides agents in using Remotion to create React and TypeScript video projects, preview them locally, render MP4/WebM/GIF outputs, and configure Lambda or Cloud Run rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to build data-driven or personalized videos with Remotion, including component authoring, local preview, media rendering, captions, and cloud rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unpinned npx and npm installation commands.

Mitigation: Review commands before execution, pin package versions, use a lockfile, and isolate installs in a project workspace.

Risk: The skill includes AWS Lambda and Cloud Run rendering workflows that can use credentials and create cloud cost exposure.

Mitigation: Require explicit approval before cloud deployment, use least-privilege short-lived credentials, and verify cost limits and cleanup steps.

Risk: Troubleshooting guidance includes destructive local cleanup and process termination commands.

Mitigation: Confirm target paths and process IDs manually before running rm or kill commands.

## Reference(s):

- [Remotion homepage](https://remotion.dev)
- [Remotion documentation](https://remotion.dev/docs)
- [Remotion API reference](https://remotion.dev/api)
- [Remotion GitHub repository](https://github.com/remotion-dev/remotion)
- [Remotion Lambda guide](https://remotion.dev/docs/lambda)
- [Remotion captions documentation](https://remotion.dev/docs/captions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose npm, npx, local rendering, and cloud rendering commands that require user review before execution.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
