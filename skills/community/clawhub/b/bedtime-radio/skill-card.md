## Description: <br>
Generate a complete bedtime story audio program from a keyword, with intro, narration, character voices, and a sleepy outro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, caregivers, and agents serving families use this skill to turn a bedtime-story idea, child age, and length preference into a structured soothing audio program. It guides story writing, SenseAudio synthesis, MP3 file generation, and final assembly instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bedtime-story text is sent to SenseAudio for text-to-audio synthesis. <br>
Mitigation: Avoid including children's real names, addresses, health details, or sensitive family information in prompts or generated story text. <br>
Risk: The skill stores SenseAudio JSON responses and MP3 files locally. <br>
Mitigation: Review generated files before sharing them and delete local story artifacts that contain private family details. <br>
Risk: The workflow depends on a SenseAudio API key and local command-line tools. <br>
Mitigation: Keep SENSEAUDIO_API_KEY out of shared logs and repositories, and install curl, jq, and xxd from trusted package sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/bedtime-radio) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with Bash snippets and generated MP3/JSON file names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces story text, audio segment plans, SenseAudio API calls, local JSON responses, MP3 segment files, durations, and ffmpeg assembly guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
