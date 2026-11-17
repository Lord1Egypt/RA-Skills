## Description:

Browser Agent Pro guides an agent through browser automation workflows including multi-tab browsing, proxy and network configuration, paginated and dynamic scraping, session persistence, UI regression testing, and performance monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, data teams, and operations teams use this skill to direct authorized browser automation tasks such as structured web data collection, login-state workflows, UI regression checks, and page performance monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth scraping, proxy rotation, and fingerprint spoofing guidance may be misused to bypass site controls, rate limits, paywalls, or terms.

Mitigation: Use the skill only on sites and accounts where automation is authorized, and review each proposed scraping or proxy workflow against applicable site rules before execution.

Risk: Saved cookies, sessions, proxy credentials, and alert webhooks can expose account or infrastructure access if mishandled.

Mitigation: Store secrets in environment variables or encrypted session storage, keep session files out of version control, restrict file permissions, scope credentials per site, and delete stale sessions.

Risk: Generated browser actions, shell commands, and test configurations may be incorrect for the target site or environment.

Mitigation: Review commands and configuration before running them, start with limited-scope tests, and keep human approval in workflows that affect accounts, payments, deployments, or production data.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-agent-pro-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose browser actions, configuration snippets, scraping outputs, test reports, and operational guidance for the invoking agent to review before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
