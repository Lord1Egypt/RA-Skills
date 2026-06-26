## Description: <br>
Audits and scans OpenClaw skills for security risks by uploading a target skill directory or archive to a Volcengine scanning service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to submit OpenClaw skill directories or archives for Volcengine security scanning and receive JSON results that can be summarized for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected skill or archive contents may be uploaded to Volcengine or another configured scan endpoint. <br>
Mitigation: Review the target directory for secrets or proprietary data before scanning and use only approved scan endpoints. <br>
Risk: Cloud scan credentials are used to sign API requests. <br>
Mitigation: Use dedicated least-privilege Volcengine credentials and configure them through the approved OpenClaw configuration or environment mechanism. <br>
Risk: Small upload bodies may be echoed in terminal or CI logs. <br>
Mitigation: Avoid scanning sensitive small archives in shared terminals or CI, and review logs for accidental disclosure. <br>
Risk: Untrusted archives are unpacked and repackaged before upload. <br>
Mitigation: Inspect archives before scanning and avoid running the script on untrusted archive inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-security-skillsscanner) <br>
- [Volcengine Access Key Guide](https://www.volcengine.com/docs/6291/65568?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON array from the scan script and Markdown security report text for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target skill name, an absolute skill or archive path, and Volcengine credentials or a configured scan endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
