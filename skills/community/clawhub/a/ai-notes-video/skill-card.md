## Description: <br>
Generate detailed AI notes, including document, outline, and image-text formats, from a user-provided video URL using Baidu's video AI notes tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiduQianfanGroup](https://clawhub.ai/user/baiduQianfanGroup) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit a video URL to Baidu's AI notes API, poll task status, and retrieve generated document, outline, or image-text notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, internal, signed, token-bearing, or confidential video URLs may be sent to Baidu's service for processing. <br>
Mitigation: Use only authorized media URLs and review Baidu's retention, logging, and processing terms before submitting sensitive content. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/baiduQianfanGroup/ai-notes-video) <br>
- [Baidu AI Notes Task Create API](https://qianfan.baidubce.com/v2/tools/ai_note/task_create) <br>
- [Baidu AI Notes Task Query API](https://qianfan.baidubce.com/v2/tools/ai_note/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands] <br>
**Output Format:** [JSON responses containing task metadata and generated note content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and a reachable video URL; querying may need repeated polling until the task completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
