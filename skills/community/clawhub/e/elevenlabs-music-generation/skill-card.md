## Description: <br>
Generate full songs and instrumental tracks with ElevenLabs Music on RunComfy via the runcomfy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to draft and generate vocal songs, instrumental beds, jingles, podcast intros, game loops, and other music tracks through RunComfy's ElevenLabs Music endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music generation uses an external paid model API, so long generations can create unexpected cost. <br>
Mitigation: Review music_length_ms before execution and draft shorter clips before generating full-length tracks. <br>
Risk: RunComfy credentials and generated prompts may expose sensitive account or creative information if mishandled. <br>
Mitigation: Keep RUNCOMFY_TOKEN private, avoid logging tokens, and do not submit confidential lyrics, brand material, or unreleased creative work unless the operator accepts sending it to RunComfy and ElevenLabs. <br>
Risk: User-supplied lyrics or brand material may have rights or licensing constraints. <br>
Mitigation: Confirm the operator has the rights to any provided lyrics or creative material before using it for generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalvinrv/elevenlabs-music-generation) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [ElevenLabs Music model on RunComfy](https://www.runcomfy.com/models/elevenlabs/elevenlabs/music-generation?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation) <br>
- [RunComfy CLI docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; generated music is downloaded as audio files by the RunComfy CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI and RunComfy authentication; music length is controlled from 5 seconds to 5 minutes per generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
