## Description: <br>
Generate songs from prompts or lyrics through an ACE-Step-compatible API backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twocode](https://clawhub.ai/user/twocode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit text-to-music or lyrics-to-song jobs to an ACE-Step-compatible backend, save generated audio files, and optionally hand the saved files to Clawatch playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured backend can influence output file locations and remote fetches. <br>
Mitigation: Use only a local or trusted HTTPS ACE-Step-compatible backend and inspect generated output paths before sharing or playback. <br>
Risk: Prompts, lyrics, and API keys may be sent to the configured backend. <br>
Mitigation: Avoid private lyrics or sensitive prompts with unknown services and use a scoped API key when authentication is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twocode/gen-music) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands plus saved audio files and a JSON manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is saved to a stable output directory; the skill requires a separate ACE-Step-compatible backend and Python 3.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
