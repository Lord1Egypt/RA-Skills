## Description: <br>
Baidu Wenku AI Picture Book helps agents create static or dynamic picture-book video tasks from story text and retrieve generated video URLs from Baidu's service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn story or educational text into static or dynamic AI picture-book video outputs through Baidu Wenku. Agents can create a generation task, poll task status, and return the resulting video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story prompts and task data are sent to Baidu's external service using BAIDU_API_KEY. <br>
Mitigation: Do not submit secrets, private personal data, unpublished confidential material, or regulated content unless the user's data-sharing requirements allow it. <br>
Risk: Generated video URLs are returned as external links. <br>
Mitigation: Treat returned URLs as external content and review them before sharing or embedding. <br>
Risk: Generation can time out or remain in progress while the task continues server-side. <br>
Mitigation: Use bounded polling intervals and query the task again later with the returned task ID when generation does not complete promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/ai-picture-book) <br>
- [Baidu Qianfan API base](https://qianfan.baidubce.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text, External links] <br>
**Output Format:** [Command output and JSON responses containing task IDs, status values, and generated video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and Python 3; dynamic and static picture-book modes are selected with method values 10 and 9.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence; artifact _meta.json lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
