## Description:

Guides agents through researching a topic, planning a long-form manual, writing modular HTML fragments, and building a book-length PDF with Node.js and Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renbigcheng](https://clawhub.ai/user/renbigcheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agent users use this skill to turn a topic into a structured PDF manual or ebook through research, outline planning, parallel HTML-fragment writing, build automation, and version updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shell and Node.js scripts use user-provided project titles, paths, metadata, and update messages while creating files and running builds.

Mitigation: Run the workflow in a dedicated project directory and avoid untrusted titles, metadata, paths, and update messages.

Risk: The workflow depends on mutable external packages and browser assets for Playwright-based PDF rendering.

Mitigation: Pin Playwright and related dependencies with a lockfile before use.

Risk: PDF rendering may load remote fonts from the generated HTML/CSS.

Mitigation: Remove remote font imports or block network access during PDF rendering when reproducibility or network isolation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renbigcheng/skills/book-pdf)
- [Design system reference](artifact/references/design-system.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTML/CSS/JavaScript templates, and project configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local project skeleton, modular HTML fragments, build scripts, changelog/version metadata, rendered HTML, and PDF outputs when the generated workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
