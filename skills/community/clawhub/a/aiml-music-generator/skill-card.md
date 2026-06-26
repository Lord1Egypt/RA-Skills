## Description: <br>
Generates music and songs through AIMLAPI models such as Suno, Udio, Minimax, and ElevenLabs from prompts, lyrics, and style requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to create instrumental music, songs, or soundtracks with custom prompts, lyrics, model choices, length, and output location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts and lyrics are sent to AIMLAPI for generation. <br>
Mitigation: Avoid submitting confidential prompts, private lyrics, or sensitive project details. <br>
Risk: AIMLAPI usage may consume quota or incur billing through the configured API key. <br>
Mitigation: Use a dedicated AIMLAPI key where possible and monitor API usage and billing. <br>
Risk: Generated audio files are downloaded to a local output directory. <br>
Mitigation: Save outputs to a normal project or downloads directory and review generated files before reuse. <br>


## Reference(s): <br>
- [AIMLAPI audio generation endpoint](https://api.aimlapi.com/v2) <br>
- [ClawHub release page](https://clawhub.ai/aimlapihello/aiml-music-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples; generated MP3 files from the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY and writes generated MP3 files to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
