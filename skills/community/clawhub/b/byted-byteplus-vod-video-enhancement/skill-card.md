## Description: <br>
Upload video/audio media to BytePlus VOD storage, returning Vid and playback references, and run AI-based comprehensive quality restoration on already-uploaded videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and media operations teams use this skill to upload local or URL-hosted media into BytePlus VOD, obtain reusable media references, and submit selected videos for quality restoration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs credentialed BytePlus VOD API calls and can upload selected local or URL-hosted media. <br>
Mitigation: Use only scoped BytePlus credentials, confirm the selected media before execution, and verify the target VOD space before uploading. <br>
Risk: Returned playback or signed URLs may expose media access depending on VOD space and domain settings. <br>
Mitigation: Treat returned URLs as sensitive and confirm publication, authentication, and access-control settings before processing private, regulated, or unreleased media. <br>
Risk: Overriding the VOD host could direct credentialed requests to an unintended endpoint. <br>
Mitigation: Set VOD_HOST only after verifying the official endpoint for the intended BytePlus environment. <br>


## Reference(s): <br>
- [BytePlus VOD Python SDK](https://docs.byteplus.com/en/docs/byteplus-vod/docs-python-sdk) <br>
- [Quality restoration parameter reference](references/quality-enhance.md) <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-byteplus-vod-video-enhancement) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts print JSON lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BytePlus credentials and a VOD space; outputs may include media IDs, playback URLs, direct URLs, signed URLs, or timeout resume commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
