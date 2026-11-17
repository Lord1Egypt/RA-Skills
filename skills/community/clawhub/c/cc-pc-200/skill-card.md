## Description:

PC 200 helps run a ClawHub publishing probe that uses many tiny synthetic files to locate a multipart file-count threshold associated with 413 errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autogame-17](https://clawhub.ai/user/autogame-17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to probe ClawHub publishing behavior with synthetic files and identify file-count limits that may trigger 413 responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing threshold tests may fail or encounter rate limits while probing 413 behavior.

Mitigation: Run the probe only when testing ClawHub publishing limits and plan for publish failures or rate-limit effects.

Risk: Using real project files could expose sensitive content during a publishing probe.

Mitigation: Use only synthetic, non-sensitive test files.

## Reference(s):

- [PC 200 on ClawHub](https://clawhub.ai/autogame-17/skills/cc-pc-200)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publishing-probe guidance for synthetic test files; no hidden code or persistence was found in the security evidence.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
