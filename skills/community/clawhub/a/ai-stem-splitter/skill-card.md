## Description: <br>
Use when the user wants to split a song or audio file into vocals, drums, bass, guitar, piano, and other stems; remove vocals for karaoke; extract acapellas or instrumentals; process YouTube, SoundCloud, Bandcamp, direct audio URLs, MP3, WAV, or other audio through the AI Stem Splitter API, SDKs, or web app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeugar](https://clawhub.ai/user/codeugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to route audio files or source URLs through the hosted AI Stem Splitter service and return separated stems for karaoke, acapella extraction, remix preparation, practice loops, or stem-level analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files, source URLs, and job metadata are sent to a third-party hosted processing service. <br>
Mitigation: Confirm each file or URL before submission and avoid private or internal URLs unless the user explicitly intends to process them with AI Stem Splitter. <br>
Risk: The skill requires an API key for the AI Stem Splitter service. <br>
Mitigation: Use AISTEMSPLITTER_API_KEY from the environment, never print or store the key, and keep API calls server-side. <br>
Risk: Optional SDK installation adds package supply-chain exposure. <br>
Mitigation: Verify the Node or Python SDK package before installing it and use raw REST calls when the user prefers not to add dependencies. <br>
Risk: Generated stems may be misused if the user lacks rights to the source audio. <br>
Mitigation: State that users must have rights to process and use the source audio, and do not promise copyright clearance. <br>


## Reference(s): <br>
- [AI Stem Splitter API Reference](references/api.md) <br>
- [AI Stem Splitter ClawHub Release](https://clawhub.ai/codeugar/ai-stem-splitter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with API workflow guidance, shell commands, code-oriented integration details, and stem result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include returned stem names, job status, source filename or URL, download URLs, and local file paths when downloads are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
