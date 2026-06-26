## Description: <br>
Transforms casual, voice-transcribed, mixed-language, vague, or ambiguous user requests into structured AI-optimized prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesxu81](https://clawhub.ai/user/jamesxu81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other agent users use this skill to convert informal requests into clear prompts with task, context, requirements, references, and output expectations. It is most useful for voice transcription, mixed-language input, ambiguous requests, and complex multi-step work that needs clarification before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account-related examples can encourage users to include private identifiers or message content in prompts. <br>
Mitigation: Replace personal identifiers with placeholders, avoid unnecessary private content, and confirm before posting, sending, or acting externally. <br>
Risk: A refined prompt may make an ambiguous or destructive request appear ready to execute. <br>
Mitigation: For destructive or high-impact actions, summarize the intended action and obtain confirmation before execution. <br>


## Reference(s): <br>
- [Prompt Refiner release page](https://clawhub.ai/jamesxu81/covert-native-language-to-ai-firendly-prompt) <br>
- [Prompt Refiner package listing](https://clawhub.com/skills/prompt-refiner) <br>
- [Worked examples](references/examples.md) <br>
- [Prompt engineering techniques](references/techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Structured prompt text or Markdown; the bundled CLI can also emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a focused clarification question before producing the refined prompt when critical context is missing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
