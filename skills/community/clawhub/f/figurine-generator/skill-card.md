## Description:

Figurine Generator helps agents create toy design drafts, multi-view reference sheets, 3D generation tasks, and task-polling requests through Craftsman Agent toy generation APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to draft toy concepts, create 3D toy generation jobs from prompts or images, and poll for generated model and preview outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, task identifiers, and generated-asset links are sent to OneKey and Craftsman external services.

Mitigation: Use only data approved for those services, and avoid confidential images, internal URLs, regulated data, or secrets.

Risk: The skill includes unpinned npx command examples that could execute changing third-party code while an API key is present.

Mitigation: Prefer the documented REST curl flow, or pin and review any CLI package before running it with DEEPNLP_ONEKEY_ROUTER_ACCESS.

Risk: Returned share_url links and generated asset URLs may provide access to task results.

Mitigation: Treat share_url values and generated-asset links as sensitive and share them only with intended recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/figurine-generator)
- [OneKey Agent Gateway endpoint](https://agent.deepnlp.org/agent_router)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [Craftsman Agent website](https://craftsman-agent.aiagenta2z.com)
- [OneKey access keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with curl and npx command examples plus JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API outputs can include task IDs, share URLs, image URLs, model file URLs, previews, progress values, and provider metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
