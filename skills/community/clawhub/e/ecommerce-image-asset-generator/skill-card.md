## Description: <br>
Plan and generate ecommerce image assets that actually support conversion. Use when teams need to decide which product, PDP, marketplace, promo, or ad images to create first, turn product context into clear visual briefs, or route asset generation/editing through an available image provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, marketers, marketplace teams, and developers use this skill to prioritize product image assets, turn business goals into visual briefs, and prepare provider-ready prompts or edit plans for conversion-focused ecommerce visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider-backed generation can expose API keys or tokens if credentials are pasted into chat. <br>
Mitigation: Use preconfigured environment variables or a trusted secret mechanism before running provider-backed image generation. <br>
Risk: External image providers may receive confidential product images or sensitive campaign context. <br>
Mitigation: Send confidential product images only when the selected provider's privacy and retention terms are acceptable. <br>
Risk: Generated ecommerce visuals can include misleading claims, non-compliant copy, or edits that drift from the original product or brand requirements. <br>
Mitigation: Review asset briefs, on-image text, compliance boundaries, and edited outputs before publishing or using them in listings, ads, or campaigns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/ecommerce-image-asset-generator) <br>
- [Output Template](artifact/references/output-template.md) <br>
- [Provider Notes - Seedream 5.0 (ARK API)](artifact/references/provider-seedream-5.md) <br>
- [Provider Notes - Nano Banana Pro / Nano Banana 2](artifact/references/provider-nano-banana.md) <br>
- [Provider Notes - Jimeng 4.0](artifact/references/provider-jimeng-v4.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown asset plans, briefs, provider-ready prompts, payload guidance, and optional file paths or URLs when execution runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stop at planning and prompt output when provider authentication, endpoints, runtime details, or source images are unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
