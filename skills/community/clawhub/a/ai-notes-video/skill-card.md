## Description:

AI Notes Video generates document, outline, and image-text notes from a user-provided video URL using Baidu's video AI notes service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiduqianfangroup](https://clawhub.ai/user/baiduqianfangroup)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to submit a video URL to Baidu Qianfan, create an AI notes task, and query results for document, outline, or image-text notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends the video URL, referenced video content, task IDs, and Baidu API credential to Baidu's Qianfan service.

Mitigation: Use only video URLs and credentials that are approved for disclosure to Baidu, and avoid private, internal-only, confidential, or access-controlled video URLs unless that disclosure is acceptable under policy.

Risk: The artifact documentation has minor naming and help-text inconsistencies that could confuse operators during task creation or querying.

Mitigation: Confirm the intended script and API step before execution: create a task with the video URL, then query repeatedly with the returned task ID until completion or failure.

## Reference(s):

- [Baidu Qianfan AI Notes Task Create API endpoint](https://qianfan.baidubce.com/v2/tools/ai_note/task_create)
- [Baidu Qianfan AI Notes Query API endpoint](https://qianfan.baidubce.com/v2/tools/ai_note/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [JSON task responses containing note status and note content, typically summarized for the agent as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and a reachable video URL; task results may need repeated status queries until completion.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
