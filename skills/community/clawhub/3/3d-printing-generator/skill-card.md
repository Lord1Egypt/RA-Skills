## Description:

Generates toy design drafts, multi-view reference sheets, and 3D model generation workflows through Craftsman Agent APIs served by the OneKey Agent Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to call Craftsman Agent toy-generation APIs that turn prompts or reference images into toy design sheets, create 3D generation tasks, and poll for generated model and preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a OneKey access key for external API calls.

Mitigation: Use a short-lived, least-privilege key where possible and avoid exposing it in logs, shell history, or shared examples.

Risk: Prompts, private image URLs, and returned share URLs may expose sensitive project data.

Mitigation: Avoid confidential prompts or private image URLs, and treat returned share URLs like secrets.

Risk: The artifact includes unpinned npx CLI examples.

Mitigation: Prefer the REST API examples or review and pin the CLI package before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/3d-printing-generator)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [OneKey Agent Gateway endpoint](https://agent.deepnlp.org/agent_router)
- [OneKey access keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with REST API examples, CLI examples, and JSON response structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce share URLs, generated image URLs, task IDs, GLB model URLs, preview URLs, and credit usage from external services.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
