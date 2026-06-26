## Description: <br>
Create explainer videos with narration and AI-generated visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create narrated explainer or tutorial videos from a topic, source text, or concept. It guides collection of language, style, speaker, and output choices before generating a script or full video through ListenHub/Marswave. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends explainer topics or source text to an external ListenHub/Marswave service. <br>
Mitigation: Avoid private or confidential material unless the provider's data handling is acceptable for the intended use. <br>
Risk: The skill requires a ListenHub API key and uses it in API requests. <br>
Mitigation: Provide the key only in the expected environment variable, limit access to trusted workspaces, and rotate it if exposure is suspected. <br>
Risk: Generated preferences and outputs may be stored locally under .listenhub/explainer/. <br>
Mitigation: Review local output files before sharing the workspace or committing generated content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/0xFANGO/explainer-video) <br>
- [Video Guide](references/video-guide.md) <br>
- [ListenHub explainer app](https://listenhub.ai/app/explainer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and curl commands, local configuration files, generated script text, and generated media links or downloaded audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LISTENHUB_API_KEY and may write preferences and generated outputs under .listenhub/explainer/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
