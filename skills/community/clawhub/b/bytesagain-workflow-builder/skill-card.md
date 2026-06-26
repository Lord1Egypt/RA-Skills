## Description: <br>
Create and run multi-step shell-command workflows with status tracking for local automation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define, run, inspect, list, and export repeatable shell-command workflows such as local CI, build, and deployment sequences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs arbitrary shell commands from workflow steps. <br>
Mitigation: Review each workflow and command before running it, and avoid workflows from untrusted sources. <br>
Risk: Commands that print secrets may leave short output snippets in the workflow store. <br>
Mitigation: Avoid commands that emit credentials, tokens, or other sensitive values, and clear stored workflow outputs when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/loutai0307-prog/bytesagain-workflow-builder) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON workflow definitions or exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow execution can save short command-output snippets in the local workflow store.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
