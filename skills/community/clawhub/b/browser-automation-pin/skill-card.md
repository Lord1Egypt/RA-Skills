## Description: <br>
Browser Automation enables AI agents to control Chrome through PinchTab for navigation, interaction, testing, scraping, extraction, screenshots, PDFs, and multi-instance browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to have agents drive real Chrome sessions for web testing, scraping, form interaction, visual checks, and browser-based data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser profiles, cookies, local storage, screenshots, PDFs, and extracted page content may contain sensitive data. <br>
Mitigation: Use dedicated or disposable browser profiles for sensitive sites and delete screenshots, PDFs, and extracted data when they are no longer needed. <br>
Risk: Agent-driven browser control can submit forms, click controls, run JavaScript, or interact with authenticated sessions in unintended ways. <br>
Mitigation: Review planned actions before execution, avoid hardcoding real credentials, and use least-privileged test accounts where possible. <br>
Risk: A local browser automation service exposed beyond trusted access could allow unauthorized browser control. <br>
Mitigation: Keep the PinchTab service bound to trusted local access and restrict network exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huamu668/browser-automation-pin) <br>
- [PinchTab Documentation](https://pinchtab.com/docs) <br>
- [PinchTab GitHub](https://github.com/pinchtab/pinchtab) <br>
- [Agent Optimization Guide](https://pinchtab.com/docs/guides/agent-optimization) <br>
- [Common Patterns](https://pinchtab.com/docs/guides/common-patterns) <br>
- [SMCP Plugin](https://github.com/pinchtab/pinchtab/tree/main/plugins) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown with bash and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to create browser artifacts such as extracted text, screenshots, PDFs, and JavaScript evaluation results through PinchTab.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
