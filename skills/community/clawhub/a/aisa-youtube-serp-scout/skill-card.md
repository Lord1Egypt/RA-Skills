## Description: <br>
Search YouTube videos, channels, and trends through the AIsa YouTube SERP client for content research, competitor tracking, and trend discovery without managing Google credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content researchers use this skill to search YouTube SERPs, identify top videos, research channels, and monitor trends through the AIsa API using a configured API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIsa API key and sends it with YouTube research requests to AIsa. <br>
Mitigation: Use a dedicated, rotatable API key and avoid exposing it in shared prompts, logs, or shell history. <br>
Risk: YouTube search queries and research context are sent to the AIsa API. <br>
Mitigation: Avoid submitting confidential or sensitive research terms unless the deployment policy permits sharing them with AIsa. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-youtube-serp-scout) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the bundled Python client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the AISA_API_KEY environment variable; search requests are sent to the AIsa API.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
