## Description:

Ai Maker helps e-commerce image teams turn creative briefs into Jimeng or LiblibAI image-generation result records with tool selection, model parameters, and output paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhihai123](https://clawhub.ai/user/duzhihai123)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce creative operators and agent builders use this skill to route product briefs to Jimeng or LiblibAI-style image workflows, choose parameters, and preserve generation records for review and iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the inspected code claims image generation while returning placeholder success results.

Mitigation: Review runtime behavior before relying on generated output, and verify that real Jimeng or LiblibAI integrations are implemented and tested before production use.

Risk: The security guidance says prompt snippets may be retained in plaintext generation history.

Mitigation: Avoid confidential prompts unless history storage is hardened, access-controlled, or disabled for sensitive runs.

Risk: The security guidance calls for runtime quantity validation.

Mitigation: Validate requested image counts at runtime against the documented 1-4 image limit before invoking or simulating generation.

## Reference(s):

- [Ai Maker ClawHub Listing](https://clawhub.ai/duzhihai123/skills/ai-maker)
- [Jimeng](https://jimeng.jianying.com/)
- [LiblibAI](https://www.liblib.art/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON result objects with image path metadata and Markdown generation-history entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records selected tool, model, prompt-derived parameters, quantity, and output paths; current inspected code returns placeholder image paths rather than invoking live image generation.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
