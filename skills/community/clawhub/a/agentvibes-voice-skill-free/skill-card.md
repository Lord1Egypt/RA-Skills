## Description: <br>
Agentvibes Voice Skill Free helps agents use Piper TTS for basic text-to-speech voice selection, listing, preview, sampling, and speed control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI-agent operators use this skill to add basic voice output workflows through Piper TTS, including voice switching, previewing, sampling, and speech-rate adjustment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawHub security summary says the skill requests broader execution, file, API, and credential-related authority than a Piper-only voice skill clearly needs. <br>
Mitigation: Restrict use to Piper text-to-speech tasks, run it in a constrained agent environment, and avoid granting file, execution, API, or credential access that is not needed for the specific voice workflow. <br>
Risk: The ClawHub security guidance warns users not to provide API keys unless the publisher explains why they are needed. <br>
Mitigation: Do not configure API keys for routine Piper TTS use; if a key is required, verify the publisher's explanation and keep credentials in scoped environment variables outside version control. <br>
Risk: The ClawHub security guidance notes that first-time voice use may download files from HuggingFace. <br>
Mitigation: Review and approve first-use network downloads, cache voice files from trusted sources, and avoid using downloaded voice assets in sensitive environments until they have been inspected. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/thcjp/skills/agentvibes-voice-skill-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with slash-command examples and JSON-shaped status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local Piper voice selection and first-use voice file downloads; normal outputs include command guidance, status summaries, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
