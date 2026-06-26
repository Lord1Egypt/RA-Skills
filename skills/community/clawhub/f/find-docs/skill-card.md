## Description: <br>
Retrieves authoritative, up-to-date technical documentation, API references, configuration details, and code examples for developer technologies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kritsanan1](https://clawhub.ai/user/kritsanan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to resolve a technology to a Context7 library ID and retrieve current documentation, API references, configuration details, and code examples before answering technical questions or writing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation queries are sent to the external Context7 service. <br>
Mitigation: Use sanitized documentation-style queries only, and exclude API keys, passwords, private source code, customer data, and confidential architecture details. <br>
Risk: The skill asks the agent to run the Context7 npm CLI. <br>
Mitigation: Install and run it only in environments where use of the Context7 CLI is approved, and authenticate with Context7 only when higher rate limits are needed. <br>


## Reference(s): <br>
- [ClawHub listing for Find Docs](https://clawhub.ai/kritsanan1/find-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Context7 CLI command examples and documentation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include library-selection rationale, version-specific documentation IDs, quota handling guidance, and reminders to keep sensitive information out of documentation queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
