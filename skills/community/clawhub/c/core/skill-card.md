## Description:

Core provides plain-text devtools reference documentation for core concepts, workflows, debugging, performance, security, migration, and quick-reference use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Core to ask an agent for concise reference guidance about devtools fundamentals, setup, patterns, troubleshooting, performance, security, migration, and quick commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference text mentions credentials as a general prerequisite topic, which could be mistaken for a request to provide secrets.

Mitigation: Treat credential mentions as general documentation only; do not paste secrets into prompts, scripts, or shell commands.

Risk: The skill provides generic devtools reference guidance that may not match a specific production environment.

Mitigation: Review the output against project documentation, security policy, and environment-specific requirements before applying it.

## Reference(s):

- [BytesAgain Homepage](https://bytesagain.com)
- [Core on ClawHub](https://clawhub.ai/xueyetianya/skills/core)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Plain text reference documentation with Markdown-style headings, lists, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static reference output; no external API calls, credential handling, persistence, or network access observed in the inspected artifact evidence.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
