## Description:

Beautify UI helps agents apply design-system inspired UI styling to web projects, including project detection, style recommendations, preview pages, design tokens, and component snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcya01](https://clawhub.ai/user/xcya01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to restyle websites and prototypes across common frontend frameworks, generate preview artifacts, and export design tokens or component snippets for implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite existing project files such as DESIGN.md, theme override CSS, asset CSS, or tailwind.config.js.

Mitigation: Run it in a Git working tree or backup first, inspect dry-run output, and review diffs before keeping generated files.

Risk: Security evidence says the documented preview mode is not actually non-mutating.

Mitigation: Treat preview mode as mutating until fixed; run it only on disposable copies or after backing up the project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xcya01/skills/beautify-ui)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, CSS, HTML, JSON, JavaScript, and shell command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write DESIGN.md, theme override CSS, preview HTML, design tokens, snippets, comparison HTML, and Tailwind configuration in the target project.]

## Skill Version(s):

3.3.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
