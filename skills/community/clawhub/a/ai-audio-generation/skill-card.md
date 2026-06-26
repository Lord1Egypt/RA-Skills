## Description: <br>
AI audio generation for agents through Image Skill's zero-setup hosted creative runtime for music, sound, ambience, effects, and durable hosted audio output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgwilson](https://clawhub.ai/user/danielgwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn prompts into AI-generated audio such as music, sound design, ambience, and effects through Image Skill's hosted runtime. It is intended for workflows that need durable hosted audio URLs, recoverable jobs, cost receipts, stable JSON, payments, and feedback without managing provider credentials or local model infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated audio jobs are sent to Image Skill's hosted service. <br>
Mitigation: Review prompt content before use and avoid sending confidential or sensitive material unless the hosted service is approved for that data. <br>
Risk: The skill can use an Image Skill token and payment workflow for generation. <br>
Mitigation: Review token handling and spending controls before running generation commands; start with the no-spend guide path when media spend is not approved. <br>
Risk: Examples invoke the latest npm CLI package and hosted media URLs. <br>
Mitigation: Inspect commands before execution and pin or approve CLI versions according to local release policy when reproducibility is required. <br>


## Reference(s): <br>
- [Image Skill Homepage](https://image-skill.com) <br>
- [Image Skill LLM Contract](https://image-skill.com/llms.txt) <br>
- [Canonical Skill Contract](https://image-skill.com/skill.md) <br>
- [CLI Contract](https://image-skill.com/cli.md) <br>
- [Hosted API](https://api.image-skill.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/danielgwilson/ai-audio-generation) <br>
- [Publisher Profile](https://clawhub.ai/user/danielgwilson) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON-oriented runtime guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Image Skill's hosted runtime and may return durable hosted media URLs, recoverable job data, cost receipts, and stable JSON results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
