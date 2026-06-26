## Description: <br>
Professional web automation with headless browser - navigate, scrape, automate, test, and interact with any website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raff-lima](https://clawhub.ai/user/raff-lima) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to control Browserless-backed headless browsers for web navigation, scraping, form automation, screenshots, PDFs, and page interaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad browser-control authority over websites, forms, browser session data, and local output files. <br>
Mitigation: Install only when that authority is intended, and require explicit confirmation before uploads, submissions, cookie or localStorage reads, custom auth headers, screenshots, PDFs of private pages, or arbitrary JavaScript evaluation. <br>
Risk: Browserless credentials and browser sessions can expose sensitive data if shared with an untrusted or overly broad runtime. <br>
Mitigation: Keep BROWSERLESS_TOKEN in secure secret storage, use wss:// for remote services, and prefer a dedicated or self-hosted Browserless instance for sensitive work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raff-lima/browserless-agent) <br>
- [Browserless Documentation](https://docs.browserless.io) <br>
- [Browserless service](https://browserless.io) <br>
- [Playwright Documentation](https://playwright.dev) <br>
- [CSS Selectors Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, configuration] <br>
**Output Format:** [JSON action results, extracted text, and generated screenshot or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BROWSERLESS_URL and may use BROWSERLESS_TOKEN; screenshot and PDF actions write files to requested paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
