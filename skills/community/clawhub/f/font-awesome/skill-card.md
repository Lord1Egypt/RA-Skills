## Description:

Add Font Awesome icons to web projects with CDN, npm, React, and SVG sprite methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and web project maintainers use this skill to select Font Awesome icons, choose an installation method, and generate framework-appropriate icon markup or package commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes non-transparent wording that tells the agent not to mention its setup file.

Mitigation: Prefer a version that removes that wording and allows the agent to be transparent about setup behavior when relevant.

Risk: The skill may store icon preferences in workspace memory when a user expresses recurring preferences.

Mitigation: Ask before storing preferences and keep saved preferences limited to icon style, package method, or Font Awesome version.

Risk: Using the CDN method sends an HTTP request to Font Awesome infrastructure.

Mitigation: Use npm packages, framework packages, or SVG sprites when a project requires local-only assets or avoids external CDNs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/font-awesome)
- [Skill homepage](https://clawic.com/skills/font-awesome)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline HTML, JSX, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include accessibility labels, free versus Pro icon availability notes, installation guidance, and optional memory preference guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
