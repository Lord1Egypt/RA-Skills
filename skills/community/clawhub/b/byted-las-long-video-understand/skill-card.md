## Description: <br>
Extracts audio tracks from supported video files and splits long audio into fixed-duration segments using Volcengine LAS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare local or TOS-hosted video and audio for Volcengine LAS processing, estimate cost, upload inputs when needed, run audio extraction or splitting, and present output segment paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can automatically fetch and install remote SDK code without a clear consent or integrity check. <br>
Mitigation: Review artifact/scripts/env_init.sh before installation, run it only in an isolated environment, and approve the remote Volcengine-hosted SDK source before proceeding. <br>
Risk: The skill requires sensitive LAS and optional TOS credentials and may send selected media to Volcengine services. <br>
Mitigation: Use least-privilege, short-lived credentials, avoid pasting long-lived secrets into chat, and confirm that the selected input media can be uploaded to Volcengine. <br>
Risk: Audio upload and processing can incur cloud charges. <br>
Mitigation: Estimate pricing before upload or processing and require explicit user confirmation before executing LAS jobs. <br>


## Reference(s): <br>
- [las_audio_extract_and_split API Reference](artifact/references/api.md) <br>
- [Volcengine LAS Pricing Reference](artifact/references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include pricing estimates, environment checks, LAS command guidance, generated result summaries, and TOS output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
