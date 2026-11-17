## Description:

Plan and generate ecommerce image assets that actually support conversion. Use when teams need to decide which product, PDP, marketplace, promo, or ad images to create first, turn product context into clear visual briefs, or route asset generation/editing through an available image provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, marketers, designers, and agent operators use this skill to prioritize conversion-focused product, PDP, marketplace, promotional, and ad image assets before generating or editing them through an available provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation or editing workflows may send prompts or source images to a selected provider.

Mitigation: Confirm the provider and approval status before uploading confidential product, listing, or campaign assets.

Risk: Credentials can be exposed if raw API keys or tokens are pasted into chat.

Mitigation: Use environment variables or a secret manager, and confirm required provider access without sharing secrets.

Risk: Generated ecommerce visuals or copy may imply unsupported product claims.

Mitigation: Capture compliance boundaries in the asset brief and review outputs for misleading or prohibited claims before use.

## Reference(s):

- [Output Template](references/output-template.md)
- [Provider Notes - Seedream 5.0](references/provider-seedream-5.md)
- [Provider Notes - Nano Banana Pro / Nano Banana 2](references/provider-nano-banana.md)
- [Provider Notes - Jimeng 4.0](references/provider-jimeng-v4.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown asset plans, commercial briefs, provider-ready prompts or edit plans, and optional generated file paths or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stop at planning and prompt guidance when provider credentials, endpoints, source images, or runtime details are unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
