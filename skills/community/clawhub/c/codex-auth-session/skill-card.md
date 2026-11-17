## Description:

Refreshes Codex CLI auth.json from a local ChatGPT web session for users whose normal OAuth flow is blocked by firewalls, WSL, containers, or remote desktops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcz-user](https://clawhub.ai/user/zcz-user)

### License/Terms of Use:

MIT-0

## Use Case:

Developers who use Codex CLI on Windows use this skill to refresh auth.json from an existing ChatGPT browser session when browser-based OAuth is unreliable in proxied, containerized, WSL, or remote desktop environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live ChatGPT and Codex credentials and writes authentication data to the local filesystem.

Mitigation: Use it only on trusted machines, keep browser profiles and auth backups private, and delete stored session artifacts when they are no longer needed.

Risk: Browser profiles, logs, and backups may retain sensitive session metadata or historical authentication state.

Mitigation: Protect and periodically remove browser-profile, logs, and backups directories according to the bundled security guidance.

Risk: Automatic refresh through a scheduled task can extend the lifetime of local credential material.

Mitigation: Enable scheduled refresh only when ongoing automatic credential refresh is necessary and review the task configuration before use.

Risk: Install-time scripts from a mutable remote repository may change after this release evidence was captured.

Mitigation: Review the scripts before execution and prefer a pinned release or commit when installing outside ClawHub.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zcz-user/skills/codex-auth-session)
- [README](references/README.md)
- [Security Policy](references/SECURITY.md)
- [Codex CLI](https://github.com/openai/codex)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline Bash and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused workflow requiring Node.js 18+, Chrome or Microsoft Edge, and Playwright Core.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
