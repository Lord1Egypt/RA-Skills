## Description: <br>
Secure browser automation with Chrome profile support, vault integration, approval gates, and comprehensive audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverho](https://clawhub.ai/user/riverho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use Browser Secure to automate Chrome sessions for authenticated or gated web content while preserving approval gates, vault-backed credential access, isolated browser profiles, and audit records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials and authenticated page content. <br>
Mitigation: Install only on a trusted, single-user machine; use a dedicated automation Chrome profile; and scope vault items narrowly to the sites being automated. <br>
Risk: Approval bypass options can reduce human review for sensitive sites. <br>
Mitigation: Avoid auto-approval flags such as --yes or --skip-approval for sensitive sessions and keep approval gates enabled for login, extraction, and recording. <br>
Risk: Captured screenshots, raw HTML, full text, logs, cache, and daemon state can retain sensitive content. <br>
Mitigation: Disable raw HTML and full-text capture unless needed, and regularly clear ~/.browser-secure scrapbook, logs, cache, and daemon state. <br>


## Reference(s): <br>
- [Browser Secure on ClawHub](https://clawhub.ai/riverho/browser-secure) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Default Configuration](artifact/config/default.yaml) <br>
- [Package Manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated configuration, capture, and audit artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshots, YAML or JSON scrapbook records, audit logs, and browser session state during use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
