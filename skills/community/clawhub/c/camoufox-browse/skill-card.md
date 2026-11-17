## Description:

Anti-detection browsing with a real Firefox (Camoufox) when Cloudflare, Datadome, or fingerprinting blocks the built-in browser tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenaufa](https://clawhub.ai/user/zenaufa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive authorized browsing sessions against sites where standard automation is blocked by bot detection or browser fingerprinting. It provides Node and Python guidance for Camoufox setup, session persistence, proxy configuration, form interaction, page reading, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anti-detection browsing can be misapplied to sites where automation is not authorized.

Mitigation: Use the skill only for sites where automated access is permitted by the site's terms and applicable law.

Risk: Saved browser sessions, cookies, proxy credentials, or account data may be exposed if reused or stored in shared locations.

Mitigation: Use disposable profiles and accounts, keep secrets in environment or proxy configuration, and avoid storing session-state files in shared or source-controlled paths.

Risk: Browser automation may submit forms, download files, run bulk actions, or delete data in ways that are difficult to undo.

Mitigation: Require explicit human approval before form submissions, bulk actions, downloads, deletion, or other irreversible steps.

Risk: Camoufox and Playwright dependency changes can break browsing workflows.

Mitigation: Pin or lock Camoufox and Playwright dependencies, including the documented Playwright 1.60.0 constraint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zenaufa/skills/camoufox-browse)
- [Camoufox Homepage](https://camoufox.com)
- [Camoufox PyPI Package](https://pypi.org/project/camoufox/)
- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup commands, browser automation snippets, troubleshooting guidance, and operational safety constraints for authorized Camoufox usage.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
