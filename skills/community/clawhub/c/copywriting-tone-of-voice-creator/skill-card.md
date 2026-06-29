## Description: <br>
Builds or adapts a machine-readable TONE.md brand voice guide through discovery, voice definition, lexicon and mechanics decisions, and channel-specific tone modulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand, marketing, content, and developer teams use this skill to create a structured TONE.md guide for downstream copywriting agents and human writers. It supports new tone-of-voice guide creation and channel adaptation for an existing guide. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tone guidance can be inappropriate for regulated, political, financial, crypto, healthcare, or adult-content contexts if accepted without review. <br>
Mitigation: Review the generated TONE.md before using it in high-stakes or regulated contexts, and verify any research-derived category norms and claims. <br>
Risk: The skill may read local brand documents supplied by the user or present in the working directory. <br>
Mitigation: Provide only documents intended for brand voice analysis and review the final markdown before sharing it downstream. <br>
Risk: Platform limits and social-channel norms can change after the guide is generated. <br>
Mitigation: Verify channel-specific constraints against current platform documentation before committing specific limits to TONE.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/copywriting-tone-of-voice-creator) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Project homepage](https://github.com/samber/cc-skills) <br>
- [TONE.md template](assets/TONE-template.md) <br>
- [Discovery questionnaire](references/discovery-questionnaire.md) <br>
- [Category adaptations](references/category-adaptations.md) <br>
- [Channel adaptations](references/channel-adaptations.md) <br>
- [Voice attributes](references/voice-attributes.md) <br>
- [Lexicon and mechanics](references/lexicon-mechanics.md) <br>
- [Reference brands](references/reference-brands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file, typically TONE.md or TONE-<channel>.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plain markdown with stable sections for downstream copywriting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
