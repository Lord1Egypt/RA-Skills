## Description:

Frontman helps users edit frontend UI visually in the browser by selecting rendered elements, describing changes in plain English, and applying source file edits with hot reload for Next.js, Astro, and Vite projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluehotdog](https://clawhub.ai/user/bluehotdog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to set up and operate browser-based visual editing for frontend applications. It supports UI changes such as spacing, colors, layout, copy, and design-system fixes in running Next.js, Astro, and Vite projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup commands install packages and modify a development project.

Mitigation: Run the skill only in a development project under version control, review dependency and source diffs after setup, and prefer pinned package versions when available.

Risk: The visual editing workflow can write changes to source files.

Mitigation: Review generated source changes before keeping or committing them, and avoid running the installer in CI or environments containing production secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluehotdog/skills/frontman-dev)
- [Frontman documentation](https://frontman.sh/docs/)
- [Frontman GitHub repository](https://github.com/frontman-ai/frontman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and framework-specific configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide source-file edits through a dev-only visual editing workflow; users should review generated changes in version control.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
