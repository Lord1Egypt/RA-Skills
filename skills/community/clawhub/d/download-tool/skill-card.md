## Description: <br>
Downloads videos from supported platforms such as YouTube, TikTok, Xiaohongshu, and Douyin by using a configured external download service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SeanFeng1234](https://clawhub.ai/user/SeanFeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a video URL, create a download task through a configured backend, poll status, and receive a temporary download link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted video URLs and the API key are sent to an external or configured backend. <br>
Mitigation: Use only datamass.cn or a trusted self-hosted backend, and avoid private or access-controlled videos. <br>
Risk: Downloads consume account credits and may create storage or billing impact. <br>
Mitigation: Check account balance and monitor credit usage before and after download tasks. <br>
Risk: Temporary download links point to backend-managed storage and are documented as expiring after 24 hours. <br>
Mitigation: Treat returned links as time-limited outputs and avoid using the skill for sensitive content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SeanFeng1234/download-tool) <br>
- [Datamass Service](https://www.datamass.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Links] <br>
**Output Format:** [Markdown or console text with status messages, task IDs, quota details, and temporary download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires download_tool_api_key in ~/.openclaw/config.json and may use download_tool_base_url for a trusted self-hosted backend.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
