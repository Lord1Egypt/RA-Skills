## Description: <br>
Download and query your Amazon order history via an unofficial Python API and CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfernandez98](https://clawhub.ai/user/pfernandez98) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technically comfortable users use this skill to install and operate the unofficial amazon-orders package for Amazon.com order-history lookup, filtering, and export. <br>

### Deployment Geography for Use: <br>
Global; the skill evidence states that only the English Amazon.com site is officially supported. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Amazon sign-in credentials and may use an MFA secret for automated login. <br>
Mitigation: Use an isolated environment, avoid persistent shell exports or dotfile storage, and store automation secrets in a secret manager. <br>
Risk: Exported order-history files may contain private purchase data. <br>
Mitigation: Protect generated files as sensitive data and limit sharing, retention, and access. <br>
Risk: The underlying amazon-orders package is an unofficial scraper-based tool that may break when Amazon changes its website. <br>
Mitigation: Pin and review the package version before automation, and validate output before relying on it. <br>


## Reference(s): <br>
- [ClawHub Amazon Orders Skill](https://clawhub.ai/pfernandez98/amazon-orders) <br>
- [amazon-orders Project Homepage](https://github.com/alexdlaird/amazon-orders) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance references Amazon account credentials, MFA secret handling, and optional JSON order-history export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
