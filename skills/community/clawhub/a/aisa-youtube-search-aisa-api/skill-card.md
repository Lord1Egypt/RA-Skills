## Description: <br>
Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover YouTube videos, channels, and playlists through the AIsa relay without configuring Google API credentials. It supports query, locale, language, and pagination-style narrowing through endpoint parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the sensitive AISA_API_KEY credential. <br>
Mitigation: Store the key in the environment or a secret manager, keep access least-privileged, and avoid exposing it in logs, prompts, or command output. <br>
Risk: YouTube search requests are sent to the external AIsa relay at api.aisa.one. <br>
Mitigation: Use the skill only when external relay requests are acceptable, and avoid sending private or regulated query text unless approved for that environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-youtube-search-aisa-api) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and structured API response handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for calling a hosted YouTube search relay; responses may include videos or grouped sections from the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
