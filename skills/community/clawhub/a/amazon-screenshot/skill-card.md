## Description: <br>
Captures Amazon ASIN detail pages as PNG screenshots, packages them into a ZIP file, and emails the archive to a user-provided campsnail.com address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[328786889](https://clawhub.ai/user/328786889) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators use this skill to collect screenshots of Amazon product pages for supplied ASINs and receive the captured images as a ZIP attachment by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports stealth browser automation, stored browser sessions, and an embedded SMTP password. <br>
Mitigation: Install only in an environment where the publisher and shared accounts are trusted; rotate or remove the embedded SMTP password before use. <br>
Risk: Screenshots may expose Amazon account, address, or product context from the persisted browser profile. <br>
Mitigation: Use a dedicated low-privilege Amazon browser profile and review screenshots before distribution. <br>
Risk: Automated verification and stealth behavior may be inappropriate without authorization for the target sites. <br>
Mitigation: Confirm that the automation behavior is authorized for the Amazon accounts and pages being accessed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/328786889/amazon-screenshot) <br>
- [Publisher profile](https://clawhub.ai/user/328786889) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Console status text plus PNG screenshots packaged as a ZIP email attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASIN inputs and a campsnail.com recipient email; generated screenshots and ZIP files are temporary and are deleted after successful email delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
