## Description:

Archive public Instagram media through InstaCognito with bounded archive/sync runs, section-aware outcomes, durable receipts, and optional local ZIP export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saju01](https://clawhub.ai/user/saju01)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use FrameFerry to run bounded, permissioned archives or syncs of public Instagram media through InstaCognito, then review status, receipts, and optional ZIP exports. It is intended for personal or explicitly authorized public-profile archiving, not login-based, private, commercial-scale, or anti-bot scraping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archiving public Instagram media through InstaCognito can exceed user rights, provider terms, or privacy expectations if used on unauthorized profiles or at commercial scraping scale.

Mitigation: Use the skill only for public profiles the user has rights or permission to archive, respect InstaCognito terms, and avoid commercial-scale or private-access workflows.

Risk: Browser, network, and file access can expose local data if run in shared folders or with credentials, cookies, tokens, signed URLs, or unrelated browser sessions.

Mitigation: Use a dedicated output folder, keep secrets and session data out of prompts, arguments, logs, and receipts, and review any scheduler, CDP attachment, or sub-agent delegation before enabling it.

## Reference(s):

- [FrameFerry ClawHub page](https://clawhub.ai/saju01/skills/frameferry)
- [FrameFerry source repository](https://github.com/saju01/frameferry)
- [InstaCognito public profile viewer](https://instacognito.com/en/photo)
- [Model-tiered orchestration guide](references/orchestration.md)
- [OpenClaw sub-agents](https://docs.openclaw.ai/tools/subagents)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands; CLI-generated JSON status, receipts, media files, and optional ZIP exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node >=20, npm, and Playwright Chromium for archive runs; ZIP export is bounded to ZIP32-safe limits.]

## Skill Version(s):

0.2.1 (source: CHANGELOG, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
