## Description: <br>
Generate structured wedding-photo prompt packages for couples using either predefined wedding-style templates or custom user ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garkinchu](https://clawhub.ai/user/garkinchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to plan AI wedding-photo or couple-portrait outputs, either by generating images directly when the runtime supports it or by producing cohesive multi-shot prompt packages for another image tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference-photo workflows can involve sensitive likenesses or non-consensual identity-based wedding imagery. <br>
Mitigation: Use only authorized photos of the actual couple and avoid presenting generated wedding imagery as real documentary evidence. <br>
Risk: Some bundled templates include Chinese ethnicity or facial descriptors that may not fit every couple. <br>
Mitigation: Review and change or remove demographic descriptors before generating prompts for other couples. <br>
Risk: Prompt packages and generated images may still drift on identity, hands, wardrobe, or anatomy. <br>
Mitigation: Review prompts and generated candidates before use, test a small set first, and select or retouch outputs that preserve likeness and wedding-photo realism. <br>


## Reference(s): <br>
- [AI Wedding Studio on ClawHub](https://clawhub.ai/garkinchu/ai-wedding-studio) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Package Schema](artifact/references/package-schema.md) <br>
- [Quality Rules](artifact/references/quality-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, images] <br>
**Output Format:** [Markdown prompt package with base prompt, negative prompt, 8-shot prompt set, usage notes, and optional generated image results when supported by the runtime] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese, English, and bilingual workflows; template packages can be adapted with user-specified wedding style, location, wardrobe, mood, lighting, and camera language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
