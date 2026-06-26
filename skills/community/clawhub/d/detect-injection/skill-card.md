## Description: <br>
Provides two-layer content safety for agent input and output using prompt-injection detection and optional content moderation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZSkyX](https://clawhub.ai/user/ZSkyX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to check untrusted user input for prompt-injection attempts and to screen generated output or sensitive-topic exchanges before an agent acts or responds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moderated input or draft output may be sent to Hugging Face and, when configured, OpenAI. <br>
Mitigation: Use dedicated scoped API keys and avoid submitting secrets, regulated data, or other sensitive content. <br>
Risk: Missing tokens or API errors can make a moderation check unavailable. <br>
Mitigation: Treat unavailable checks as inconclusive rather than proof that content is safe. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ZSkyX/detect-injection) <br>
- [Hugging Face inference endpoint used by the skill](https://router.huggingface.co/hf-inference/models/$MODEL) <br>
- [OpenAI moderations endpoint used by the skill](https://api.openai.com/v1/moderations) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Structured JSON verdicts with optional action text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HF_TOKEN for prompt-injection checks; OPENAI_API_KEY enables optional content moderation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
