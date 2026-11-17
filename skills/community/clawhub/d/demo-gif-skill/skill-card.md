## Description:

Record, render, optimize, and embed a demo GIF in a repo's README.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT

## Use Case:

Developers and documentation maintainers use this skill to add reproducible README demo GIFs for CLI tools, TUIs, web apps, and libraries. It helps an agent choose an appropriate recording method, generate scripts, render and optimize the result, and embed it with useful alt text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation commands can add package repositories or install recording tools that are not needed for a specific project.

Mitigation: Install only the recording tools required for the chosen demo path, prefer pinned versions or project lockfiles, and review any sudo APT repository changes before running them.

Risk: Recorded demo flows can accidentally capture secrets, real user data, or misleading application state.

Mitigation: Use demo credentials and sanitized fixture data for recorded flows, then preview generated GIFs before committing them.

Risk: Generated recording scripts and README edits can introduce incorrect or stale documentation.

Mitigation: Review and scan the skill output before deployment, and keep committed recording scripts with the rendered GIF so demos can be regenerated when the project changes.

## Reference(s):

- [Tape Cookbook](references/tape-cookbook.md)
- [Web App Capture](references/web-capture.md)
- [VHS](https://github.com/charmbracelet/vhs)
- [Playwright](https://playwright.dev/)
- [ffmpeg](https://ffmpeg.org/)
- [gifsicle](https://www.lcdf.org/gifsicle/)
- [asciinema](https://asciinema.org/)
- [agg](https://github.com/asciinema/agg)
- [gifski](https://gif.ski/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Markdown, Files]

**Output Format:** [Markdown guidance with inline code blocks, recording scripts, shell commands, and README image embed snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update .tape files, Playwright scripts, GIF/video assets, and README markdown.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
