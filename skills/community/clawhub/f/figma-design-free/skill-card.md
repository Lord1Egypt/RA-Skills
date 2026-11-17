## Description:

Automates Figma API workflows for browsing design files, reading design structure, exporting images, managing comments, viewing version history, and retrieving design variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and automation-focused agents use this skill to inspect and operate on Figma files, components, comments, exports, version history, and design variables through Figma API tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command-execution authority beyond its stated Figma integration purpose.

Mitigation: Install and run it only in an agent environment where file access and command execution are constrained to explicit Figma tasks.

Risk: Figma credentials and design data may be exposed or misused if granted too broadly.

Mitigation: Use a known Figma credential with least-privilege access, avoid sharing unnecessary files, and review outputs for sensitive data before reuse.

Risk: The artifact includes generic sandbox and whitelist claims that may not match the host environment.

Mitigation: Rely on host-enforced sandboxing, permission prompts, and allowlists rather than the artifact's own generic control language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/figma-design-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-oriented responses with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return file metadata, export links, status messages, or troubleshooting guidance depending on the Figma task.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
