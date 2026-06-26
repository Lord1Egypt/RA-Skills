## Description: <br>
Business API Recorder helps developers record browser API traffic from authorized web workflows and generate API logs and reconstruction-oriented implementation documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sihan2017](https://clawhub.ai/user/sihan2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, business analysts, and authorized system reviewers use this skill to capture fetch and XMLHttpRequest activity for a web business process, then turn the observed traffic into API inventories, data dictionaries, workflow notes, and implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture complete authenticated browser traffic, including cookies, authorization headers, tokens, personal data, and business secrets. <br>
Mitigation: Use it only on systems you are explicitly authorized to inspect, prefer isolated browser profiles or test accounts, and redact sensitive values before saving or sharing logs or generated documents. <br>
Risk: Captured production or regulated data could be retained in generated JSON logs or Markdown implementation documents. <br>
Mitigation: Avoid production and regulated data where possible, clear logs after use, and review generated artifacts for sensitive data before distribution. <br>


## Reference(s): <br>
- [Business API Recorder ClawHub Release](https://clawhub.ai/sihan2017/business-api-recorder) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Chrome Extension Documentation](https://docs.openclaw.ai/tools/chrome-extension) <br>
- [DOCUMENT_TEMPLATE.md](DOCUMENT_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, injected JavaScript, JSON API logs, and generated implementation documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include complete authenticated request and response data, including sensitive headers, tokens, personal data, or business secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
