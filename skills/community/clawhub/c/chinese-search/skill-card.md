## Description:

Chinese Search helps agents construct Chinese-language web searches and curl commands for Bing China and Sogou WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, content teams, and external users use this skill to prepare Chinese web searches for market research, content discovery, self-media research, and technical lookup. Users should review outbound search terms and parse returned HTML before relying on results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to third-party search providers.

Mitigation: Review the provider list before use and avoid entering secrets, credentials, private customer data, or sensitive project names as search terms.

Risk: Install examples use an unpinned ClawHub CLI version.

Mitigation: Use a reviewed and pinned ClawHub CLI version instead of @latest when installing in controlled environments.

Risk: The artifact includes an unrelated wttr.in example that may mislead users or send data to an unexpected endpoint.

Mitigation: Treat the wttr.in example as unsafe or remove it before relying on the skill.

Risk: Provider responses are raw HTML and may be incomplete, rate-limited, blocked, or difficult to parse reliably.

Mitigation: Add request throttling, review provider terms, and validate parsed results before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/chinese-search)
- [Bing China search endpoint](https://cn.bing.com/search)
- [Sogou WeChat search endpoint](https://weixin.sogou.com/weixin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests require curl and may return provider HTML that needs separate parsing.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
