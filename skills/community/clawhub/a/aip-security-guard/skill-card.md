## Description: <br>
Verify skill authorship, enforce declared permissions, and audit tool usage to secure OpenClaw environments using Agent Identity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunilp](https://clawhub.ai/user/sunilp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to install and operate AIP Security Guard for checking OpenClaw skill signatures, capability manifests, audit logs, and trusted author keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could install the wrong or impersonated global npm package. <br>
Mitigation: Verify the npm package name, publisher, repository, and version before installation. <br>
Risk: Unverified author keys could allow misplaced trust in skill signatures. <br>
Mitigation: Only add author keys whose fingerprints have been confirmed through a trusted channel. <br>
Risk: Audit logs and trust-list data may be stored somewhere inappropriate for the user's environment. <br>
Mitigation: Review where the tool stores audit logs and trust-list data before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunilp/aip-security-guard) <br>
- [AIP Protocol](https://sunilprakash.com/aip/) <br>
- [AIP Paper](https://arxiv.org/abs/2603.24775) <br>
- [aip-openclaw GitHub Repository](https://github.com/sunilp/aip-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for verification, audit review, security status, and trust-list updates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
