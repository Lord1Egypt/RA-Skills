## Description:

Helps developers, AI application teams, content platforms, and enterprise technical owners turn AI model API gateway needs into executable AI-HIVE workflows, commands, integration plans, task tracking, and cost-control guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI application teams, content platforms, and enterprise technical owners use this skill to design AI-HIVE API gateway integrations for model access, authentication, routing, asynchronous jobs, retries, audit records, and cost controls. It also helps produce production briefs, runnable commands, code examples, and review checklists for authorized image and video generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys may be persisted or exposed if users initialize local config or paste credentials into commands, logs, or shared files.

Mitigation: Prefer environment-variable credentials, keep config files permission-restricted, use placeholders in examples, and review logs and generated files before sharing.

Risk: Generation workflows can upload media and submit billable AI-HIVE jobs without an enforced in-script approval gate.

Mitigation: Review prompts, routing mode, budget, model parameters, and authorized media before execution; run a small sample before batch jobs and keep task IDs for audit.

Risk: A custom base URL could redirect credentials or media to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the replacement endpoint is fully trusted and approved.

Risk: Downloaded outputs and local processing files may be written into sensitive directories.

Mitigation: Use a non-sensitive output directory, preserve source files, and review generated media before publication or redistribution.

Risk: Commercial content workflows can produce misleading claims, unauthorized likeness or brand use, or overly similar recreations of protected material.

Mitigation: Confirm rights to all inputs, avoid false product claims and fabricated testimonials, keep reference use at an abstract structural level when rights are unclear, and require human review before publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/ai-model-api-gateway-ai-hive)
- [AI-HIVE web console](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON files, bash commands, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task records, price snapshots, task IDs, status, and local file locations when generation commands are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
