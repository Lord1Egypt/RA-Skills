## Description: <br>
Browser automation security audit pack that validates Playwright and Puppeteer headless configuration for dangerous arguments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Playwright and Puppeteer browser automation configurations for risky Chrome or Chromium launch arguments before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required mcp-openclaw-extensions dependency could introduce supply-chain risk if installed from an untrusted source. <br>
Mitigation: Confirm the dependency source and version before installation. <br>
Risk: Browser automation configuration files may contain sensitive operational settings. <br>
Mitigation: Audit only configuration files that are intended to be reviewed by the agent. <br>
Risk: The audit is scoped to known dangerous Playwright and Puppeteer browser launch arguments. <br>
Mitigation: Use the findings as a focused configuration check and review broader browser security controls separately. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/romainsantoli-web/firm-browser-audit-pack) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, guidance] <br>
**Output Format:** [Markdown or text audit findings with severity classifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings focus on dangerous Playwright and Puppeteer browser launch arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
