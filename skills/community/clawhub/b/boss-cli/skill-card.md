## Description:

Boss Cli helps agents guide users through BOSS Zhipin job search, application management, job detail review, exports, and HR greeting workflows using the boss command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and developers use this skill to install and operate the boss CLI for searching BOSS Zhipin jobs, filtering results, exporting listings, reviewing applications and interviews, and contacting recruiters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unaudited third-party CLI package.

Mitigation: Install only from a trusted source or pinned version and review the package before use.

Risk: Authentication can involve browser-cookie detection, which may expose account credentials if mishandled.

Mitigation: Prefer QR-code login over browser-cookie detection when possible.

Risk: Greeting and batch-greeting commands can send account-linked messages to recruiters.

Mitigation: Require explicit confirmation before recruiter-contact commands and use dry-run previews for batch actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/skills/boss-cli)
- [Publisher profile](https://clawhub.ai/user/aitowerofbabel-lang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can emit structured JSON with schema_version 1 when commands are run with --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
