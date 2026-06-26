## Description: <br>
French vocab automation that formats Excel vocabulary into a Google Sheet, generates ElevenLabs audio, and uploads MP3 files to Google Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clairproqc-star](https://clawhub.ai/user/clairproqc-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and language-learning content maintainers use this skill to turn French vocabulary rows into translated study materials and batched pronunciation audio. It reads configured Google Sheets, uses Gemini for translations and examples, uses ElevenLabs for audio, and uploads generated MP3 files to Google Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clear and replace the configured target Google Sheet range A1:F1000. <br>
Mitigation: Review or change the hard-coded Sheet IDs before running, confirm the target range, and keep a backup of any sheet data that should be preserved. <br>
Risk: Configured spreadsheet content and generated French sentences are sent to Gemini, ElevenLabs, and Google Drive. <br>
Mitigation: Avoid using sensitive, personal, or proprietary spreadsheet content unless those external service uses are acceptable. <br>
Risk: Generated MP3 files are uploaded to the configured Google Drive folder without a separate confirmation step. <br>
Mitigation: Review or change the Drive folder ID before audio generation and verify that the destination folder is appropriate for the generated files. <br>


## Reference(s): <br>
- [French Learning Skill Configuration](artifact/references/config.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clairproqc-star/french-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with script paths, JSON command output, Google Sheet rows, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes vocabulary in batches of 20 and writes generated content to configured Google Sheet and Drive locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
