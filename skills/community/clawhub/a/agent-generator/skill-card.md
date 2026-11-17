## Description:

Agent Generator helps with dynamic agent generation, template systems, code generation, prompt engineering, domain-specific language design, and agent capability composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, template, generate, validate, and document specialized AI agents from requirements, reusable patterns, and capability definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requirements or examples may be shared with a remote model during agent-generation workflows.

Mitigation: Redact sensitive requirements before using remote model examples or integrations.

Risk: Generated prompts and tool declarations may be influenced by model output without sufficient safeguards.

Mitigation: Use schema validation, a server-controlled tool allowlist, and human approval before activating generated agents.

Risk: Automatically granting generated agents requested tools can expand their effective permissions.

Mitigation: Review each generated agent before deployment and grant only the minimum tools required for the intended task.

## Reference(s):

- [Agent Generator examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/agent-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with code examples and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated agent prompts, template patterns, DSL examples, validation guidance, testing recommendations, and benchmark suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
