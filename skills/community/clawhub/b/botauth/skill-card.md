## Description:

Use the botauth CLI to list, search, and retrieve secrets from the user's unlocked botauth vault with per-request approval in the desktop app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyhn](https://clawhub.ai/user/eyhn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve API keys, tokens, and passwords from an unlocked local botauth vault while keeping the user in the approval loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install of the botauth CLI may install an unpinned or unreviewed CLI version.

Mitigation: Install only a trusted, reviewed botauth CLI version and avoid running npm with elevated privileges.

Risk: Agents using this skill can request vault metadata and sensitive fields from the local botauth vault.

Mitigation: Rely on the botauth desktop approval flow, request only the fields needed for the current task, and discard short-lived access keys after use.

## Reference(s):

- [botauth ClawHub Skill Page](https://clawhub.ai/eyhn/skills/botauth)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive values are retrieved only through approved botauth CLI requests and short-lived access keys.]

## Skill Version(s):

0.1.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
