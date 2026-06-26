## Description: <br>
Verify skill authorship, enforce capability manifests, and audit tool usage to secure and control OpenClaw skills with identity and access management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunilp](https://clawhub.ai/user/sunilp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to verify installed skill signatures, inspect capability manifests, review audit logs, and manage trusted author keys in an OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external npm package aip-openclaw for installation and operation. <br>
Mitigation: Confirm that aip-openclaw is the intended package, prefer a pinned version, and review where it stores trusted author keys and audit logs before installing. <br>
Risk: Adding a trusted author key can affect future skill trust decisions. <br>
Mitigation: Only trust author keys from verified sources and review trust-list changes as part of normal skill governance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunilp/aip-agent-guard) <br>
- [AIP Protocol](https://sunilprakash.com/aip/) <br>
- [AIP Paper](https://arxiv.org/abs/2603.24775) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands for installing aip-openclaw, checking skill status, viewing audit logs, and managing trusted author keys.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
