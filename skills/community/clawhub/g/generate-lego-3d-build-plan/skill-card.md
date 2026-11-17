## Description:

Call Craftsman Agent API OneKey Router to generate a LEGO 3D step-by-step instruction build plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to call the Craftsman Agent API through OneKey Router and generate LEGO build plans from a text prompt and optional reference image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional image URLs, and the OneKey API key are sent to the external Craftsman/DeepNLP service.

Mitigation: Use only approved data, avoid confidential prompts and private image links, and confirm the external service is authorized for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/generate-lego-3d-build-plan)
- [DeepNLP Workspace Keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and sends prompts plus optional image URLs to the Craftsman/DeepNLP service.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
