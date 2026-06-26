## Description: <br>
Routes uncertain, high-impact, irreversible, low-evidence, or sensitive actions to user approval, human review, professional review, admin review, or refusal before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this instruction-only skill to decide when sensitive, uncertain, irreversible, or high-impact work should proceed, ask the user, require explicit approval, route to a qualified reviewer, route to an administrator, or be refused. It is especially relevant for financial, legal, medical, production, publishing, deletion, permission, private-data, or other consequential workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review packets may expose sensitive task context if shared through untrusted review channels. <br>
Mitigation: Use only trusted review channels and share compact, redacted summaries without secrets, credentials, full private records, full logs, full transcripts, or unrelated private data. <br>
Risk: Approval and review gates add friction to financial, legal, medical, production, deletion, publishing, and other high-impact tasks. <br>
Mitigation: Apply the routing gates where the additional review is appropriate, and continue only after the required user approval, human review, professional review, or admin review is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-human-review-router) <br>
- [Human review route schema](artifact/schemas/human-review-route.schema.json) <br>
- [Redacted human review route example](artifact/examples/redacted-human-review-route.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with optional redacted JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; it does not install dependencies, execute commands, call services, write files, persist memory, or approve high-impact actions by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
