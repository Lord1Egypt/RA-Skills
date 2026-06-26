## Description: <br>
OpenClaw browser hosting and automation capabilities for web interaction, scraping, and UI testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frisky1985](https://clawhub.ai/user/frisky1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to control isolated or remote browsers for web interaction, scraping, UI testing, content extraction, and repeatable browser workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to control live or remote browsers. <br>
Mitigation: Install only when browser-control authority is intended, prefer isolated managed profiles, and review browser actions before submission, purchase, posting, account-setting, or authenticated-data workflows. <br>
Risk: Using an existing Chrome profile can expose logged-in sessions and personal browsing state. <br>
Mitigation: Prefer the isolated openclaw profile and use the chrome profile only when the agent is explicitly permitted to operate in the logged-in browser context. <br>
Risk: Remote CDP and Browserless endpoints can expose browser sessions, network traffic, and tokens if misconfigured. <br>
Mitigation: Use only trusted endpoints with TLS, short-lived tokens, and redacted logs and configuration. <br>
Risk: Configuration may require sensitive credentials such as Browserless tokens. <br>
Mitigation: Store secrets in environment variables or a secrets manager, avoid committing tokens, and rotate credentials if exposure is suspected. <br>
Risk: File upload and content extraction workflows can move local files or authenticated data to websites. <br>
Mitigation: Review target sites, selected files, extracted data, and destination forms before allowing upload or extraction actions. <br>


## Reference(s): <br>
- [Browser Configuration Guide](references/configuration.md) <br>
- [Browser Profiles Reference](references/profiles.md) <br>
- [Browser Snapshot System](references/snapshot-system.md) <br>
- [Browser Automation Workflow Example](assets/example-workflow.md) <br>
- [ClawHub release page](https://clawhub.ai/frisky1985/browser-hosting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser snapshots, screenshots, PDFs, network observations, and generated command sequences depending on the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
