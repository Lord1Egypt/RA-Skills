## Description:

Recognizes Chinese calligraphy font styles from uploaded images or image URLs, including kaishu, xingshu, caoshu, zhuanshu, lishu, and weibei.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfxia](https://clawhub.ai/user/jfxia)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, learners, and cultural heritage reviewers use this skill to identify the likely script style in Chinese calligraphy images and receive confidence-ranked alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads supplied images to external services, including an undisclosed third-party mirror.

Mitigation: Use only non-sensitive images, disclose all upload destinations before use, and make the mirror endpoint opt-in or remove it.

Risk: URL input can fetch arbitrary remote content before forwarding it externally.

Mitigation: Restrict URL fetching with network egress controls and validate target hosts, content types, and response sizes.

Risk: Hugging Face token use is supported but not fully documented for operators.

Mitigation: Document HF_TOKEN handling and avoid exposing tokens in logs, prompts, or shared outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfxia/skills/chinese-calligraphy-recognition)
- [Hugging Face Space: jfxia/shufa](https://huggingface.co/spaces/jfxia/shufa)
- [Hugging Face inference model: xiajingfeng/shufa](https://api-inference.huggingface.co/models/xiajingfeng/shufa)
- [Hugging Face Space endpoint](https://jfxia-shufa.hf.space/run/predict)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON recognition results with confidence scores and alternative candidates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw API responses when verbose mode is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
