## Description:

Monitor and clean invalid Codex auth files from CPA (Codex Provider Agent), including quota checks, disabling 401 files, and double-verifying files before deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekjair](https://clawhub.ai/user/geekjair)

### License/Terms of Use:


## Use Case:

Developers and operators who manage CPA-backed Codex authentication files use this skill to inspect file status, disable files that return 401 responses, and delete disabled files after repeated verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a high-privilege CPA admin key.

Mitigation: Prefer CPA_KEY from an environment variable or secret store, restrict config.json permissions, and avoid exposing the key in shared workspaces.

Risk: The clean, delete, and monitor commands can permanently remove Codex auth records.

Mitigation: Run status and check first, review affected files, and use destructive commands only when you operate the CPA server.

Risk: CPA traffic sent to insecure or untrusted endpoints could expose administrative access.

Mitigation: Use HTTPS CPA URLs and avoid untrusted CPA endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geekjair/skills/codex-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown and terminal text reports, JSON summaries, and command-line configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CPA URL and admin key configuration from CLI arguments, environment variables, or config.json.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
