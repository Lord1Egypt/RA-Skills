## Description: <br>
Converts Mandarin or Cantonese text into natural Cantonese phrasing and generates Cantonese MP3 speech with selectable tone and voice options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpenn](https://clawhub.ai/user/jimpenn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to convert Chinese text into Cantonese phrasing and generate spoken Cantonese MP3 files for localized audio assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is synthesized through the edge-tts dependency, so text may be handled by an external TTS service. <br>
Mitigation: Use only text appropriate for that service and review dependency and service terms before processing sensitive content. <br>
Risk: The script writes timestamped MP3 files to the current working directory. <br>
Mitigation: Run it from the intended output directory and review generated files before sharing or committing them. <br>
Risk: Automatic Cantonese phrasing may change meaning, register, or tone. <br>
Mitigation: Have a Cantonese speaker review important or customer-facing audio before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimpenn/cantonese-tts) <br>
- [Publisher profile](https://clawhub.ai/user/jimpenn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or terminal text with generated MP3 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates timestamped MP3 files in the current working directory; tone options are normal, slow, fast, and angry; voice options are hiuMaan, hiuGaai, and wanLung.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
