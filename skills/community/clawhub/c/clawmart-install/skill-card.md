## Description:

Search and install an OpenClaw configuration pack from ClawMart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxdaozhang](https://clawhub.ai/user/rxdaozhang)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to search ClawMart, choose a configuration pack, download it with an API token, and install pack files into an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote pack contents can overwrite local OpenClaw workspace files or add skill files.

Mitigation: Install only trusted packs, inspect exact file names, contents, and destinations before writing, and keep backups for rollback.

Risk: The ClawMart API token may be stored locally in plaintext.

Mitigation: Use scoped or short-lived tokens when available, avoid pasting long-lived tokens, and remove the saved token when it is no longer needed.

Risk: Downloaded file paths may be unsafe if remote content is not validated.

Mitigation: Sanitize every remote file path and block writes outside the intended OpenClaw workspace and skills directories.

Risk: Pack authenticity may be unclear before installation.

Mitigation: Validate pack signatures or other trust signals and install only from publishers the user trusts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/rxdaozhang/skills/clawmart-install)
- [ClawMart service](https://clawmart-gray.vercel.app)
- [ClawMart token dashboard](https://clawmart-gray.vercel.app/dashboard/tokens)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Files, Configuration]

**Output Format:** [Markdown guidance with API request details, JSON snippets, and installation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OpenClaw configuration files, workspace files, skill files, backups, and a local ClawMart token configuration.]

## Skill Version(s):

1.2.3 (source: server release evidence; artifact frontmatter lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
