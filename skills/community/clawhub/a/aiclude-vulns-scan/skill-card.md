## Description: <br>
Search security vulnerability scan results for MCP Servers and AI Agent Skills from the AICLUDE scan database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mastergear4824](https://clawhub.ai/user/mastergear4824) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to look up vulnerability reports for MCP servers and agent skills, or to register a target for server-side scanning when no report exists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or internal target names, target types, and scan results may be sent to and retained by AICLUDE. <br>
Mitigation: Use the skill on private or internal targets only after confirming that AICLUDE handling and retention are acceptable for the data. <br>
Risk: The referenced npm package is a separate installable dependency from the skill artifact. <br>
Mitigation: Review the npm package and its dependencies separately before installing it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mastergear4824/aiclude-vulns-scan) <br>
- [AICLUDE Scan Dashboard](https://vs.aiclude.com) <br>
- [AICLUDE Security Skill npm Package](https://www.npmjs.com/package/@aiclude/security-skill) <br>
- [AICLUDE Security MCP npm Package](https://www.npmjs.com/package/@aiclude/security-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown vulnerability report or plain text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include risk level, vulnerability details, risk assessment, and remediation recommendations.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package-lock.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
