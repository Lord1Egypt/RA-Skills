## Description: <br>
Evaluates whether an agent has enough information, permission, tools, evidence, and safe boundaries before starting a workflow or high-impact action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a pre-workflow readiness gate before tool use, file changes, external actions, purchases, research tasks, customer actions, code changes, or high-impact decisions. It helps the agent decide whether to start, ask for clarification, retrieve evidence, request approval, route to review, narrow scope, or refuse unsafe work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agents to pause more often for clarification, approval, evidence, or review before acting. <br>
Mitigation: Use it when readiness checks are desired for workflows or high-impact actions, and treat additional pauses as part of the approval and evidence-gathering process. <br>
Risk: Readiness review payloads could expose private data if an external checker is connected carelessly. <br>
Mitigation: Use only approved checker integrations and send minimal, redacted payloads without secrets, credentials, full private records, full logs, or unrelated private data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-workflow-readiness-check) <br>
- [README](artifact/README.md) <br>
- [Workflow readiness payload schema](artifact/schemas/workflow-readiness-check.schema.json) <br>
- [Redacted readiness check example](artifact/examples/redacted-workflow-readiness-check.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, JSON] <br>
**Output Format:** [Agent-facing instructions with an optional text readiness check and redacted JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
