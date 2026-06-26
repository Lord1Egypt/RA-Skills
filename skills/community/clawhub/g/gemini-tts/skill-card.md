## Description: <br>
Custom TTS using Gemini 2.5 Flash for high-quality, persona-driven voice output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate spoken audio files from supplied text through Gemini 2.5 Flash TTS. It is useful when an agent workflow needs command-line text-to-speech output and can provide a GEMINI_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to Google Gemini, which can expose secrets, private prompts, or regulated data. <br>
Mitigation: Use only appropriate text for the target environment and avoid sending secrets, private prompts, or regulated data. <br>
Risk: The skill requires a Gemini API key for cloud API access. <br>
Mitigation: Provide GEMINI_API_KEY through the environment and manage it as a secret outside prompts, source files, and generated artifacts. <br>
Risk: The --voice/persona option is accepted by the script but the security guidance says it is not actually honored. <br>
Mitigation: Do not rely on custom voice or persona selection until the script is updated and retested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangzhe1991/gemini-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [Audio file plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output_voice.<mime extension>; requires GEMINI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
