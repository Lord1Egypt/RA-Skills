## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shendingyi](https://clawhub.ai/user/shendingyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable patterns as structured learning notes. It helps agents review prior learnings, promote durable knowledge into shared memory files, and optionally configure hooks that remind agents to log useful discoveries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes could capture secrets, private transcripts, sensitive command output, or customer data. <br>
Mitigation: Keep .learnings local unless team sharing is intentional, and redact API keys, tokens, passwords, customer data, private transcripts, and sensitive command output before saving entries. <br>
Risk: Promoted learnings may place incorrect, stale, or overly broad guidance into shared memory or agent instruction files. <br>
Mitigation: Review each promoted learning for accuracy, scope, and sensitivity before adding it to shared memory or agent instruction files. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Skill Release Page](https://clawhub.ai/shendingyi/alex-self-improving-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/shendingyi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and structured log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local markdown learning files and optional agent hook configuration when the user chooses to install or enable those workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
