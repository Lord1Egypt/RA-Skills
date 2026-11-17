## Description:

Enterprise natural-language browser automation skill for remote browser clusters, stealth mode, proxy and CAPTCHA handling, batch task orchestration, monitoring, and alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation teams, and business operators use this skill to drive browser workflows for data collection, competitive monitoring, content publishing, and multi-account operational tasks. It is intended for authorized browser automation where remote browsers, proxies, CAPTCHA handling, batching, and monitoring are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes stealth mode, proxy rotation, CAPTCHA solving, scraping, and bulk publishing workflows that may be misused or violate site policies.

Mitigation: Use only for legitimate authorized automation on systems, sites, accounts, and data you are permitted to access; review these workflows before execution.

Risk: Remote browser, proxy, CAPTCHA, webhook, and account workflows can expose credentials or sensitive collected data.

Mitigation: Store secrets in environment variables or a secret manager, avoid hardcoded-key examples, limit account permissions, and redact sensitive data from logs, screenshots, and exports.

Risk: Batch automation can create unintended high-volume actions or publishing mistakes.

Mitigation: Constrain concurrency, require human review for publishing or account actions, keep audit logs, and test against low-impact targets before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-automation-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose browser commands, configuration snippets, extracted data formats, screenshots, metrics, logs, and webhook alert payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
