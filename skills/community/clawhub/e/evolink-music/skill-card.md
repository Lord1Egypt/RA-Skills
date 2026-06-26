## Description: <br>
AI music generation with Suno v4, v4.5, v5. Text-to-music, custom lyrics, instrumental, vocal control. 5 models, one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, developers, and agents use this skill to generate songs or instrumental music, configure Suno model parameters, upload source audio for continuation or remix workflows, and retrieve generated audio links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, audio files, base64 audio, or referenced URLs may be sent to Evolink for generation and file handling. <br>
Mitigation: Use only content the user intends to send to Evolink, and avoid private, unreleased, licensed, or internal audio unless the user accepts that exposure. <br>
Risk: Uploaded audio can be exposed through temporary public links. <br>
Mitigation: Tell users that uploaded files expire after 72 hours, generated result URLs expire after 24 hours, and sensitive links should be saved or deleted deliberately. <br>
Risk: Deleting the wrong hosted file could remove audio the user still needs. <br>
Mitigation: Confirm file IDs before calling delete operations. <br>


## Reference(s): <br>
- [Evolink Music API Parameter Reference](references/music-api-params.md) <br>
- [Evolink File Hosting API](references/file-api.md) <br>
- [Evolink Homepage](https://evolink.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/EvoLinkAI/evolink-music) <br>
- [Evolink Media MCP Package](https://www.npmjs.com/package/@evolinkai/evolink-media) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline commands, configuration snippets, task IDs, status updates, and generated audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference temporary hosted files and generated result URLs that expire.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
