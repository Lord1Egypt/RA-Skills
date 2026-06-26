## Description: <br>
Guides a Chinese two-step option flow for adult female portrait generation, produces two matched realistic portraits, and can optionally create a video-ready character reference sheet from the first image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pddsa](https://clawhub.ai/user/pddsa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn short or fuzzy Chinese beauty-photo requests into guided adult-female portrait outputs with consistent styling. It also supports an optional reference-sheet follow-up for video or motion-design preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because the skill uses a local quota lockout and may direct users to an external WeChat or social-promotion unlock path after quota exhaustion. <br>
Mitigation: Review before installing, monitor generated user-facing messages, and avoid following off-platform payment, contact, or promotional instructions unless the publisher is trusted. <br>
Risk: The skill is designed for adult female portrait generation, which can create misuse risk if users request underage, school-age, explicit, or sexualized-youth framing. <br>
Mitigation: Keep the documented refusal behavior active and limit vague sexy requests to tasteful, non-explicit fashion portrait language. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pddsa/beauty-photo-generator) <br>
- [Conversation Flows](references/conversation_flows.md) <br>
- [Option Catalog](references/option_catalog.md) <br>
- [Reference Sheet Prompt](references/reference_sheet_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Chinese conversational guidance with generated-image instructions and inline shell commands for quota checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces two matched portrait-generation requests by default and one optional character-reference-sheet request when the user asks for it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
