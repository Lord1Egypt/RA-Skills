## Description: <br>
Browser Collector provides a Playwright-based browser automation and data collection framework with adapters for structured document, API, social, and finance-site extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjl1004](https://clawhub.ai/user/wjl1004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to collect and structure web content from authorized sites through browser automation, site-specific adapters, batch jobs, OCR, proxy handling, and command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines browser scraping, stealth behavior, CAPTCHA solving, proxy rotation, batch collection, and persistent cookies. <br>
Mitigation: Install only for authorized collection workflows; use strict domain allowlists and disable stealth, CAPTCHA solving, public proxies, and cookie persistence unless explicitly approved. <br>
Risk: Persistent cookies, OAuth tokens, and other sensitive credentials can expose personal or work sessions. <br>
Mitigation: Run in an isolated environment with throwaway accounts, avoid personal browser sessions, and disable cookie export or persistence when not required. <br>
Risk: Batch collection and public proxy use can create high-volume or hard-to-attribute traffic. <br>
Mitigation: Use conservative worker limits, rate limits, and vetted network paths; avoid public proxies for business or sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub Browser Collector Page](https://clawhub.ai/wjl1004/browser-collector) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Integration Plan](artifact/INTEGRATION_PLAN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Structured extraction results, Markdown or JSON content, Python API examples, and CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Playwright browser installation, OCR dependencies, OAuth tokens or other sensitive credentials, and target-site authorization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
