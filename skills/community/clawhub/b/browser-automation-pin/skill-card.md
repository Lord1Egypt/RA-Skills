## Description:

Browser automation for AI agents using PinchTab to control Chrome programmatically for testing, scraping, interaction, text extraction, multi-instance orchestration, headless or headed browsing, and MCP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to guide agents through browser navigation, interaction, web data extraction, form workflows, visual checks, and Chrome-based validation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a remote curl-to-bash installer pattern.

Mitigation: Review the installer before use and prefer a pinned, verifiable npm or container release, especially in privileged or secret-rich environments.

Risk: Persistent browser profiles can retain cookies, local storage, and authenticated sessions.

Mitigation: Treat profiles and cookies as credentials, use test accounts where possible, and isolate or remove profiles after sensitive automation.

Risk: Browser outputs such as screenshots, PDFs, cookies, and extracted page text may contain sensitive information.

Mitigation: Avoid exposing these outputs from sensitive sites to untrusted agents, logs, or shared storage.

Risk: Automated browser interaction can perform actions on live sites or authenticated accounts.

Mitigation: Run against test environments and accounts where possible, review target URLs and actions before execution, and clean up browser instances after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huamu668/skills/browser-automation-pin)
- [Publisher profile](https://clawhub.ai/user/huamu668)
- [PinchTab documentation](https://pinchtab.com/docs)
- [PinchTab GitHub](https://github.com/pinchtab/pinchtab)
- [Agent Optimization Guide](https://pinchtab.com/docs/guides/agent-optimization)
- [Common Patterns](https://pinchtab.com/docs/guides/common-patterns)
- [SMCP Plugin](https://github.com/pinchtab/pinchtab/tree/main/plugins)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash commands, curl examples, API patterns, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may produce browser actions, screenshots, PDFs, extracted page text, cookies, or JavaScript evaluation commands when used with PinchTab.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
