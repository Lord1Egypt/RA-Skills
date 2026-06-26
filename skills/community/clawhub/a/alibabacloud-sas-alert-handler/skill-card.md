## Description: <br>
Alibaba Cloud Security Center (SAS) CWPP host security alert handling skill for querying, analyzing, and handling alerts from Cloud Security Center. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators and cloud engineers use this skill to inspect Alibaba Cloud Security Center host alerts, review available handling operations, execute approved remediation or suppression actions, and verify handling status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Alibaba Cloud Security Center actions such as blocking, quarantining, ignoring, or whitelisting alerts. <br>
Mitigation: Use a dedicated least-privilege RAM identity, start with read-only permissions when possible, and manually review any block, quarantine, kill, ignore, or whitelist action before approval. <br>
Risk: The skill requires Alibaba Cloud credentials and operates in a cloud security account context. <br>
Mitigation: Check credential status without exposing secrets, avoid pasting long-lived AccessKeys into prompts, commands, or logs, and use scoped credentials appropriate to the intended alert workflow. <br>


## Reference(s): <br>
- [Workflow Details](references/workflow-details.md) <br>
- [Operation Codes](references/operation-codes.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud SAS alert summaries, recommended handling actions, command examples, polling results, and final remediation status summaries.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
