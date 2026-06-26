## Description: <br>
Api Billing helps agents query account balances, subscription usage, and historical billing for Volcengine, Alibaba Cloud, DeepSeek, MiniMax, and OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check API account balances, subscription usage, and billing history across supported cloud and model API providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive cloud and API billing credentials, and the security review notes weak storage guidance around Base64-encoded credential files. <br>
Mitigation: Use least-privilege billing or read-only keys, store secrets with a managed secret mechanism when possible, keep credential files out of source control with strict permissions, and do not treat Base64 as encryption. <br>
Risk: The skill contacts named third-party provider billing APIs and may print account balance, usage, or billing details. <br>
Mitigation: Run it only in trusted environments, review the configured provider endpoints before use, and avoid sharing logs or terminal output that contain billing or account data. <br>


## Reference(s): <br>
- [API billing interface reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/yifeiwang1981/api-billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured provider credentials and network access to the named billing APIs; command output may include account balance, usage, and billing amounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
