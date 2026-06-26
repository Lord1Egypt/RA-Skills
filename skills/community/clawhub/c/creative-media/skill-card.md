## Description: <br>
Creative media for agents over one zero-setup Image Skill runtime: image generation, image editing, video, audio, and image-to-3D assets with no provider API key, OAuth, local runtime, or per-provider billing account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgwilson](https://clawhub.ai/user/danielgwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to request generated images, edits, video, audio, and image-to-3D assets through the hosted Image Skill runtime. The skill is intended for workflows that need durable hosted URLs, recoverable jobs, stable JSON, cost receipts, payments, and feedback through one agent-facing interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded media, generated outputs, and job state flow through an external hosted Image Skill service. <br>
Mitigation: Use the skill only after approving that external processing and storage; avoid confidential, regulated, personal, or unreleased assets unless that use is explicitly allowed. <br>
Risk: Agent use can involve wallet/payment flows and paid media generation. <br>
Mitigation: Start with no-spend inspection commands and allow paid generation only when spend is intentionally approved. <br>
Risk: Agents may run the Image Skill npm CLI as part of the workflow. <br>
Mitigation: Install only when the workspace permits agents to run this hosted-service CLI, and review generated commands before execution in sensitive environments. <br>


## Reference(s): <br>
- [Creative Media on ClawHub](https://clawhub.ai/danielgwilson/creative-media) <br>
- [Image Skill Homepage](https://image-skill.com) <br>
- [Image Skill LLM Contract](https://image-skill.com/llms.txt) <br>
- [Canonical Image Skill Contract](https://image-skill.com/skill.md) <br>
- [Image Skill CLI Contract](https://image-skill.com/cli.md) <br>
- [Hosted Image Skill API](https://api.image-skill.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for hosted creative-media generation, including commands that can return stable JSON, durable media URLs, job recovery details, and cost receipts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
