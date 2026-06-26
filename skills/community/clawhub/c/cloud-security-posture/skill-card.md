## Description: <br>
Cross-cloud security posture assessment covering IAM analysis, encryption audit, and public exposure detection across AWS, Azure, and GCP using provider-specific inline command labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud security engineers, auditors, and incident responders use this skill to assess IAM posture, encryption coverage, and public exposure across multi-cloud AWS, Azure, and GCP environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad cloud visibility across AWS, Azure, and GCP and may handle sensitive IAM, credential-report, and exposure data. <br>
Mitigation: Use narrowly scoped read-only cloud credentials, restrict assessment scope to approved accounts or projects, and treat collected security data as confidential. <br>
Risk: The security evidence notes that the skill overstates read-only safety while requesting GCP Storage Admin for bucket IAM inspection. <br>
Mitigation: Avoid granting GCP Storage Admin unless it is truly required for the assessment, and prefer the least-privileged role set that supports the requested checks. <br>


## Reference(s): <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Security Controls Reference](references/security-controls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown assessment procedure with CLI command blocks and a report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces findings, provider comparison, and prioritized remediation guidance without modifying cloud resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
