## Description:

Cross-platform browser opening skill that supports launching URLs with the default browser or Chrome, Firefox, Edge, and Safari.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent provide command-line and Python usage for opening trusted URLs in a selected local browser across Windows, macOS, or Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README instructs users to run pip install for Python standard-library module names, which creates avoidable supply-chain risk.

Mitigation: Do not run that installation command; use the skill with the Python standard library modules already available.

Risk: Using the skill can launch local browser tabs or windows and make network connections to supplied URLs.

Mitigation: Run it in a normal user context and open only URLs you trust.

## Reference(s):

- [Browser Support Details](references/browser_support.md)
- [ClawHub Skill Page](https://clawhub.ai/panchenbo/skills/browser-opener-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may launch local browser tabs or windows and make network connections when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
