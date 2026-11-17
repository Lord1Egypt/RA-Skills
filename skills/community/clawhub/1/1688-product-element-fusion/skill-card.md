## Description:

Extracts creative elements from inspiration images or video frames, searches 1688 for real products in a user-specified category, researches feasibility factors, and generates product concept image variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product designers, sourcing teams, and marketplace operators use this skill to turn visual inspiration into practical product concepts by extracting style elements, matching real 1688 products, and producing grounded concept image variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled executable code includes unrelated template behavior.

Mitigation: Review the package before installation and prefer a revised release that removes DingTalk/template remnants not needed for product element fusion.

Risk: Executable code can report signed gateway telemetry.

Mitigation: Install only where telemetry is acceptable, or use a revised release that disables telemetry by default or clearly discloses it.

Risk: Credential behavior includes fallback to another 1688 skill configuration.

Mitigation: Use only credentials explicitly scoped to this skill and avoid shared or inherited credentials unless reviewed by the deployment owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-product-element-fusion)
- [Publisher profile](https://clawhub.ai/user/1688aiinfra)
- [Creative element model](references/element-model.md)
- [Fusion prompt template and variant strategy](references/fusion-prompt.md)
- [Element fusion examples](references/examples.md)
- [1688 skills gateway endpoint](https://skills-gateway.1688.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Images]

**Output Format:** [Markdown with structured JSON snippets, product research summaries, image-generation prompts, and generated concept image outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. The final workflow can include an element card, candidate product links, a fusion plan, concept image variants, the applied prompt, and a legal notice.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
