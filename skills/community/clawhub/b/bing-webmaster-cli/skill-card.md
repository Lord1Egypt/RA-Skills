## Description:

Use this skill when working with this repository's `bwm` CLI, including Bing Webmaster API key setup, CLI authentication, site listing, traffic stats, URL index checks with explanation, URL submission, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmadeleidev](https://clawhub.ai/user/nmadeleidev)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to install and operate the `bwm` CLI for Bing Webmaster authentication, site and URL statistics, index checks with explanations, URL submission, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run a local CLI package, so users could install an unintended or changed package source.

Mitigation: Verify the package identity before installation and pin a known version when appropriate.

Risk: The skill handles a Bing Webmaster API key that could be exposed through shell history, logs, or persisted local credential files.

Mitigation: Use a least-privileged API key, prefer an interactive prompt or secret manager over command-line key arguments, and clear stored credentials when no longer needed.

## Reference(s):

- [Bing Webmaster Tools](https://www.bing.com/webmasters/)
- [Bing Webmaster API access documentation](https://learn.microsoft.com/en-us/bingwebmaster/getting-access)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require a local Python installation, the `bwm` CLI, and a Bing Webmaster API key.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
