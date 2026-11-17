## Description:

Cookie Use helps agents capture, store, list, switch, share, and apply logged-in website sessions across Chrome profiles, isolated browsers, and connected browser sessions on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation agents use this skill to manage multiple website account sessions, switch identities in browser workflows, and replay authorized sessions for testing or operational tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture, replay, share, and inject live account sessions, which may expose or misuse authenticated access if used on accounts the user does not own or administer.

Mitigation: Use it only with explicit authorization, avoid personal, production, financial, or third-party accounts, and confirm the intended target before session injection.

Risk: Documented workflows include confirmation bypasses such as --no-confirm and COOKIE_USE_YES=1.

Mitigation: Keep confirmation enabled for interactive use and reserve bypasses for tightly controlled automation where account scope and target browser are pre-approved.

Risk: The install instructions use curl-to-shell commands for cookie-use and chrome-use.

Mitigation: Review and verify installers manually before execution, and install only when the publisher and source provenance are trusted.

Risk: Session sharing and production-to-localhost replay can move authenticated state outside its original context.

Mitigation: Avoid session sharing and cross-origin replay unless the workflow is authorized, scoped to non-sensitive accounts, and reviewed for downstream access impact.

## Reference(s):

- [Server-resolved source provenance](https://github.com/leeguooooo/cookie-use/tree/main/skills/cookie-use)
- [Cookie Use repository](https://github.com/leeguooooo/cookie-use)
- [chrome-use dependency repository](https://github.com/leeguooooo/chrome-use)
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/cookie-use)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install or run cookie-use and chrome-use, manage encrypted local session vaults, and inject sessions into browser targets.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
