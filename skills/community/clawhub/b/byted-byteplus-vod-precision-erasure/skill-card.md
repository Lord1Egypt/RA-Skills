## Description: <br>
Uploads local or URL media to BytePlus VOD, returns Vid and playback references, and submits automatic OCR precision-erasure jobs for subtitles or all detected on-screen text with optional segment filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and media operations teams use this skill to ingest video or audio into BytePlus VOD and run automated subtitle or on-screen text erasure jobs. It is suited for workflows that need Vid references, playback URLs, erasure job polling, and optional region-level erasure metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses BytePlus VOD credentials to upload media, submit erasure jobs, and generate playback or download URLs. <br>
Mitigation: Install and run it only in environments where those credentials are intended for this media workflow, and keep credentials in environment variables or an approved secret store. <br>
Risk: Endpoint and playback-domain overrides can redirect VOD API calls or generated media URLs away from the expected BytePlus configuration. <br>
Mitigation: Review VOD_HOST and VOD_PLAY_DOMAIN before use and restrict changes to approved BytePlus VOD endpoints and domains. <br>
Risk: Local upload commands can send user-provided media files to BytePlus VOD. <br>
Mitigation: Upload only media files deliberately selected for this workflow and keep any allowed upload directories narrowly scoped. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-byteplus-vod-precision-erasure) <br>
- [Precision erasure reference](references/precise_erase.md) <br>
- [BytePlus VOD Python SDK](https://docs.byteplus.com/en/docs/byteplus-vod/docs-python-sdk) <br>
- [BytePlus VOD precision subtitle erasure](https://docs.byteplus.com/en/docs/byteplus-vod/docs-precision-subtitle-erasure) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON objects on stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Vid references, playback or download URLs when available, polling status, timeout resume commands, and optional erasure metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, pyproject.toml, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
