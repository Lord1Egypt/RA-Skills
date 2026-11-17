## Description:

Browser Session Pro helps agents operate recurring and persistent browser automation sessions with webhook notifications, batch management, monitoring alerts, Cloudflare handling, and debugging support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, operations teams, and data teams use this skill to configure and manage browser sessions for recurring site checks, authenticated crawling, batch automation, webhook alerts, and session health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist logged-in browser sessions and write reusable configuration and script files.

Mitigation: Use only dedicated sessions for sites you control or have permission to automate, avoid storing secrets in saved config or generated scripts, and periodically review ~/.bsession/workspace for retained files.

Risk: The skill can run Docker browser-session commands, automatic restarts, recurring monitors, and batch jobs.

Mitigation: Restrict execution to authorized containers and sites, set conservative intervals and concurrency limits, and enable recurring monitors or automatic restarts only when explicitly needed.

Risk: Webhook notifications can send session or page-derived data to external endpoints.

Mitigation: Use dedicated webhook endpoints, redact sensitive data before sending notifications, and verify each destination URL before deployment.

Risk: The release evidence flags broad browser-session automation claims, including Cloudflare avoidance.

Mitigation: Limit use to permitted automation workflows and review site terms, access controls, and operational impact before running against third-party services.

## Reference(s):

- [Detailed bsession-tool-pro Reference](artifact/references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bsession-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, configuration snippets, and JSON-style status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Docker bsession commands, webhook configuration, generated session scripts, monitoring loops, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
