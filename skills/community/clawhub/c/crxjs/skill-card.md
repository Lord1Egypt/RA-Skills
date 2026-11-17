## Description:

CRXJS guides agents through Chrome extension development with Vite, including HMR setup, manifest-driven builds, content script configuration, framework-specific Vite configuration, and production packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, configure, troubleshoot, and package CRXJS-based Chrome extension projects. It is most useful when an agent needs to generate Vite configuration, Manifest V3 examples, content script setup, shell commands, or workflow guidance for CRXJS projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill requests broad GitHub CLI authority that its instructions do not clearly need.

Mitigation: Review tool permissions before installation and avoid or narrow GitHub CLI access unless the workflow specifically requires it.

Risk: The security guidance calls out dependency handling risk when using npm in sensitive repositories.

Mitigation: Prefer pinned npm package versions or a lockfile before applying generated dependency changes.

Risk: The skill can propose shell commands and project configuration changes for extension builds.

Mitigation: Review proposed commands and file diffs before execution, especially in repositories with release or browser-store publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/crxjs)
- [Skill library homepage](https://github.com/samber/cc-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose npm, git, and GitHub CLI commands; users should review commands before execution.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
