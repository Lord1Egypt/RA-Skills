## Description: <br>
Generate and edit AI music through the RunComfy CLI by routing user requests to ElevenLabs Music, ACE Step, ACE Step 1.5, ACE Step audio-inpaint, or ACE Step audio-outpaint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to choose the right RunComfy music model for text-to-music generation, multilingual vocal tracks, lower-cost background music, or time-bounded edits to existing audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external paid RunComfy CLI service and may generate costs for longer or premium music runs. <br>
Mitigation: Confirm the selected model, duration, and cost before running longer generations or premium ElevenLabs Music requests. <br>
Risk: RunComfy authentication is required, so token exposure could grant access to the user's RunComfy account. <br>
Mitigation: Use a limited RunComfy token where possible and avoid echoing, logging, or committing RUNCOMFY_TOKEN or files under ~/.config/runcomfy. <br>
Risk: Prompts, lyrics, and source audio are sent to RunComfy, which may be inappropriate for confidential lyrics or unreleased audio. <br>
Mitigation: Submit confidential lyrics or unreleased audio only when RunComfy's terms are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/ai-music-runcomfy) <br>
- [RunComfy homepage](https://www.runcomfy.com) <br>
- [RunComfy audio model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [ElevenLabs Music Generation model](https://www.runcomfy.com/models/elevenlabs/elevenlabs/music-generation?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [ACE Step text-to-audio model](https://www.runcomfy.com/models/acestep-ai/ace-step/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [ACE Step 1.5 text-to-audio model](https://www.runcomfy.com/models/acestep-ai/ace-step-1.5/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [ACE Step audio-inpaint model](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-inpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>
- [ACE Step audio-outpaint model](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-outpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI plus RunComfy authentication via RUNCOMFY_TOKEN or ~/.config/runcomfy.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
