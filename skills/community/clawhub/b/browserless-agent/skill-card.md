## Description:

Professional web automation with headless browser - navigate, scrape, automate, test, and interact with any website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raff-lima](https://clawhub.ai/user/raff-lima)

### License/Terms of Use:

MIT License

## Use Case:

Developers and external users use Browserless Agent to automate web browsing tasks such as scraping, form interaction, testing, screenshots, PDF generation, and browser state inspection through a configured Browserless service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and return cookies, localStorage, form values, headers, screenshots, PDFs, uploaded file paths, and extracted page content that may contain sensitive data.

Mitigation: Use a disposable browser or container, a dedicated output/upload directory, and avoid authenticated or sensitive sites unless those data flows are acceptable.

Risk: Browserless credentials and browser sessions may be exposed if endpoints or tokens are configured too broadly.

Mitigation: Use wss:// endpoints, least-privilege Browserless tokens, secure environment storage, separate tokens per environment, and regular token rotation.

Risk: Automations can interact with untrusted websites, submit forms, set headers, upload files, and execute page JavaScript.

Mitigation: Restrict network egress and target domains, validate URLs and action arguments before execution, and review high-impact actions before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raff-lima/skills/browserless-agent)
- [Browserless documentation](https://docs.browserless.io)
- [Playwright documentation](https://playwright.dev)
- [MDN CSS selectors reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files, guidance]

**Output Format:** [JSON action results with optional generated screenshot or PDF files and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can navigate websites, extract page content, return browser state data, and write screenshots or PDFs to caller-selected paths.]

## Skill Version(s):

0.1.0 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
