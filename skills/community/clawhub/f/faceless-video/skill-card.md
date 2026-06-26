## Description: <br>
Scenario-focused Sparki skill for faceless or no-camera-presence outputs while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn existing footage or ideas into faceless videos, no-camera explainers, narration-led edits, and related short-form outputs through Sparki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local video files and prompts may be uploaded to Sparki for processing. <br>
Mitigation: Use only files intended for remote processing, confirm rights and privacy expectations before upload, and avoid sensitive media unless Sparki use is approved. <br>
Risk: A Sparki API key may be stored on disk or read from the environment. <br>
Mitigation: Protect SPARKI_API_KEY as a credential, restrict access to local configuration files, and rotate the key if it may have been exposed. <br>
Risk: A custom base URL can route credentials and uploads outside the declared Sparki endpoint. <br>
Mitigation: Do not use --base-url unless the endpoint is fully trusted, and confirm the agent is routing requests to Sparki when that is the intended tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/faceless-video) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload) <br>
- [Sparki API endpoint](https://agent-api.sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON and may download MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SPARKI_API_KEY for authentication, can store configuration under $HOME/.openclaw/config, and can write video outputs under $HOME/.openclaw/workspace/sparki/videos.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
