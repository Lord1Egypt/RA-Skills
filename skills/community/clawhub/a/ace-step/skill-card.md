## Description: <br>
Generate, inpaint, and outpaint music with ACE Step on RunComfy via the runcomfy CLI, using tag-driven composition, multilingual lyrics with section markers, and 5-second to 4-minute stereo output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate new music, repair a time range in an existing track, or extend audio through RunComfy-hosted ACE Step endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid external RunComfy service and a RunComfy token, so runs can consume credits and expose submitted prompts, lyrics, or audio to that service. <br>
Mitigation: Install only if RunComfy and the @runcomfy/cli package are trusted, review endpoint and duration choices before execution, and avoid submitting confidential lyrics, unreleased audio, or private client material unless RunComfy processing is acceptable. <br>
Risk: Generated music may include user-supplied lyrics or source audio whose rights are unclear. <br>
Mitigation: Confirm the operator has rights to supplied lyrics and audio before generation, inpainting, or outpainting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/ace-step) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step) <br>
- [ACE Step text-to-audio](https://www.runcomfy.com/models/acestep-ai/ace-step/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step) <br>
- [ACE Step 1.5 text-to-audio](https://www.runcomfy.com/models/acestep-ai/ace-step-1.5/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step) <br>
- [ACE Step audio-inpaint](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-inpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step) <br>
- [ACE Step audio-outpaint](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-outpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated audio files downloaded by the RunComfy CLI into the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
