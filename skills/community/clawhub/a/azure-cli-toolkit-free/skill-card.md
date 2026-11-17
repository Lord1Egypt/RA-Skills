## Description: <br>
Azure CLI Toolkit Free helps an agent guide Azure command-line management for subscriptions, resource groups, virtual machines, storage, networking, output formatting, and JMESPath queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to get Azure CLI commands and guidance for common Azure resource management tasks, including login, subscription selection, resource groups, virtual machines, storage accounts, and formatted queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live Azure create, update, or delete operations that may affect resources or costs. <br>
Mitigation: Use a sandbox subscription or least-privilege account, require explicit confirmation before create or delete actions, and check billing and dependent resources before running examples. <br>
Risk: Azure service-principal credentials may be exposed through shell history, logs, or agent transcripts. <br>
Mitigation: Avoid pasting secrets into prompts, shell history, or logs; prefer managed secret storage and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/azure-cli-toolkit-free) <br>
- [Azure CLI Linux installer](https://aka.ms/InstallAzureCliLinux) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure CLI command output interpretation and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
