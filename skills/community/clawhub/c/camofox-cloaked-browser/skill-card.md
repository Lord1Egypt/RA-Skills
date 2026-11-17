## Description:

Use Camofox/Camoufox as an opt-in anti-detection browser server for agent workflows that need cloaked browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when ordinary browser automation is likely to be blocked and an opt-in Camofox/Camoufox browser workflow is warranted. It guides local server startup, OpenClaw plugin use, REST commands, session and tab handling, environment variables, and cleanup checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned npm browser package that downloads a large executable at install time.

Mitigation: Pin `@askjo/camofox-browser` to a reviewed version and prefer a verified local Camoufox bundle via `CAMOUFOX_EXECUTABLE`.

Risk: A cloaked browser service exposed beyond loopback can create browser-control risk if access controls are not set.

Mitigation: Keep the server on loopback for local use and set `CAMOFOX_ACCESS_KEY` before any non-local exposure.

Risk: Crash or hang telemetry may be undesirable for privacy-sensitive browsing.

Mitigation: Set `CAMOFOX_CRASH_REPORT_ENABLED=false` when privacy matters, or use a self-hosted crash-report endpoint if telemetry is required.

## Reference(s):

- [Camofox Browser upstream project](https://github.com/jo-inc/camofox-browser)
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/camofox-cloaked-browser)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to macOS and Linux environments with Node.js, npm, and curl available.]

## Skill Version(s):

1.3.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
