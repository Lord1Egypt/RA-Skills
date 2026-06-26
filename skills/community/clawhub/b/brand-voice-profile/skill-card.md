## Description: <br>
Define and store a brand voice profile for consistent content generation across tone, vocabulary, writing patterns, audience rules, and platform preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DimitriPantzos](https://clawhub.ai/user/DimitriPantzos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketers, founders, and agents use this skill to interview a user, create a reusable brand voice profile, and apply that profile when drafting or checking content for different platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to store brand voice data and writing samples on disk. <br>
Mitigation: Use only writing samples and profiles the user is authorized to analyze, avoid sensitive client material unless needed, and store profiles in expected local paths. <br>
Risk: User-provided profile names could be used as unsafe file paths if handled carelessly by an agent. <br>
Mitigation: Use simple profile names without path characters and review the target file path before creating or updating profile JSON. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DimitriPantzos/brand-voice-profile) <br>
- [Publisher profile](https://clawhub.ai/user/DimitriPantzos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON profile examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local brand voice profile JSON files when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
