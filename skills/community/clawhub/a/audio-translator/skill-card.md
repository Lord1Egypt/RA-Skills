## Description: <br>
Translates local or URL-based audio into a requested target language, then produces translated text and synthesized speech output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okgptai](https://clawhub.ai/user/okgptai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to translate audio from local files or URLs into another language and receive both text and generated speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs unpinned Python packages and system dependencies during setup or use. <br>
Mitigation: Review scripts before installation, prefer an isolated virtual environment, and pin dependencies before using the skill in trusted workflows. <br>
Risk: Speech-derived text may be sent to third-party translation and text-to-speech services. <br>
Mitigation: Avoid sensitive audio unless users accept that transcription text may be shared with external services. <br>
Risk: URL inputs cause the skill to download remote audio before processing. <br>
Mitigation: Use trusted URLs only and review downloaded content handling before processing untrusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okgptai/audio-translator) <br>
- [Publisher profile](https://clawhub.ai/user/okgptai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated audio/text file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create translated MP3 and TXT files; network access is used for URL downloads, translation, and text-to-speech.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
