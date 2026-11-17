## Description:

Automates browser navigation, screenshots, form interactions, clicking, data extraction, and web testing for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyunrei2025](https://clawhub.ai/user/baiyunrei2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent builders use this skill to drive browser-based workflows such as navigation, screenshots, form filling, element clicks, page text extraction, and web application testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted URLs, selectors, output paths, option names, or form data may be passed into local shell execution.

Mitigation: Use the skill only with trusted inputs in controlled environments, review browser commands before execution, and prefer an implementation that invokes processes with argument arrays.

Risk: Raw command logging can expose URLs, form data, selectors, or other sensitive browsing inputs.

Mitigation: Avoid sensitive data in automation inputs, use test accounts or sanitized values, and disable or scrub command logs before broader use.

Risk: Browser automation can violate website terms, robots.txt expectations, or rate limits when used aggressively.

Mitigation: Automate only appropriate public sites, respect site terms and robots.txt, and use delays or rate limits for repeated actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baiyunrei2025/skills/agent-browser-skill)
- [OpenClaw Browser Documentation](https://docs.openclaw.ai/tools/browser)
- [Playwright Automation Guide](https://playwright.dev/docs/automation)
- [Web Scraping Best Practices](https://docs.openclaw.ai/automation/web-scraping)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash examples; helper script output may include text responses and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an enabled OpenClaw browser tool, Chrome or Chromium, and network access for web browsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
