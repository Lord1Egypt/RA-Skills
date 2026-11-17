## Description:

Check Markdown files and websites for broken links. Use when asked to find dead links, validate URLs in docs, check if links still work, audit a README, or run a link health check. Zero dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to check Markdown files, documentation folders, and websites for broken local or external links before publishing or in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External URL checks and website crawl mode can make outbound requests from the execution environment.

Mitigation: Use explicit paths, shallow crawl depth, reasonable timeouts, and network controls when running against untrusted documents or from sensitive internal networks.

## Reference(s):

- [README](README.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional plain-text or JSON link-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes; optional external URL checks and crawl mode may make outbound HTTP requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
