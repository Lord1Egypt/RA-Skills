## Description:

Helps agents use the 百炼®标书 service to interpret tender files, generate bid documents, review bid submissions for compliance risks, and compare bid files for duplicate or similarity signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement teams use this skill to analyze tender files, produce bid documents, review bid submissions for compliance risks, and compare bid files for duplicate or similarity signals before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tender and bid documents are uploaded to the 百炼®标书 service and may contain commercial, pricing, or personal information.

Mitigation: Use the skill only when the user is comfortable with that upload and the service's handling of task outputs.

Risk: Paid workflows charge against the account associated with the API key.

Mitigation: Keep the API key in the skill-local config file, avoid sharing it in chat, and monitor account word balance before and after paid tasks.

Risk: The security review notes persistent local storage, writable paths, and possible ~/.zcm/projects.json creation.

Mitigation: Prefer the generated-files directory for outputs, avoid custom output paths unless intentional, and review local project storage when operating in sensitive environments.

Risk: The security review notes fixed promotional platform URLs in setup guidance.

Mitigation: Review account, registration, and recharge links before following them, especially in managed enterprise environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-audit)
- [百炼®标书 Service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API Overview](references/api.md)
- [Authentication, Jobs, and Billing](references/api-auth.md)
- [Bid Workflow API](references/api-bid-workflow.md)
- [Compliance Review API](references/api-compliance.md)
- [Duplicate Review API](references/api-duplicate.md)
- [Usage Guide](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Plain text and Markdown guidance with command-backed workflows; generated artifacts may include JSON, HTML reports, Word reports, and .docx bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local tender or bid files and a skill-local API key; paid workflows consume the API-key account's available word balance.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
