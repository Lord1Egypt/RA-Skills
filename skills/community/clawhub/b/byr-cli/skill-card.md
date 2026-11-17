## Description:

Use BYR CLI for auth, search, detail inspection, and safe torrent download planning with JSON envelopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1morebuild](https://clawhub.ai/user/1morebuild)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to operate the BYR CLI for authentication checks, torrent search, browsing, detail inspection, metadata lookup, diagnostics, and planned downloads with JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and trusting the external byr-pt-cli package.

Mitigation: Review the package source and install path before use, and use the skill only when the package source is trusted.

Risk: Authentication workflows may expose cookies, tokens, or browser session material to command lines or logs.

Mitigation: Avoid pasting real cookies or tokens into visible command lines or logs, and use browser-profile import only when the CLI and local environment are trusted.

Risk: Non-dry-run downloads write files to user-selected paths.

Mitigation: Use explicit output paths, run the documented dry-run first, inspect sourceUrl and fileName, and confirm intent before write operations.

## Reference(s):

- [BYR CLI Skill on ClawHub](https://clawhub.ai/1morebuild/skills/byr-cli)
- [Publisher profile: 1morebuild](https://clawhub.ai/user/1morebuild)
- [ClawHub homepage](https://clawhub.ai)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers byr --json output, short result summaries, explicit IDs and paths for downloads, and dry-run review before write operations.]

## Skill Version(s):

0.1.2 (source: publish.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
