## Description: <br>
Generates audiobooks, podcasts, and educational audio by drafting scripts and converting approved text into MP3 narration with ElevenLabs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn a requested topic, story, lesson, or podcast idea into an AI-written script and then an MP3 narration after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved script text is sent to Anthropic and ElevenLabs, which can expose sensitive, proprietary, or regulated content to external providers. <br>
Mitigation: Use only content that is acceptable under those providers' data handling terms, and avoid sensitive, proprietary, or regulated inputs unless those terms have been reviewed and approved. <br>
Risk: Audio generation can incur Anthropic and ElevenLabs provider costs. <br>
Mitigation: Review the generated script before text-to-speech conversion and confirm provider credits, quotas, and cost expectations before generating longer audio. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown script preview, shell command guidance, and MEDIA path for an MP3 audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANTHROPIC_API_KEY and ELEVENLABS_API_KEY; creates audio only after user approval of the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
