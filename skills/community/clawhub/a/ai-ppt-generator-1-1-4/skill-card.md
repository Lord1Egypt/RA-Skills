## Description:

Generates PowerPoint presentations with Baidu AI and selects templates based on the requested topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zou-cc](https://clawhub.ai/user/zou-cc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate PowerPoint presentations from a topic, optionally choosing a Baidu AI PPT template style or letting the scripts select one automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPT topics, outline content, and optional web_content may be sent to Baidu's AI PPT service.

Mitigation: Avoid confidential business, personal, or regulated content unless policy and data handling requirements allow use of the Baidu service.

Risk: The skill depends on a BAIDU_API_KEY and external Baidu API availability.

Mitigation: Provide the API key only through the environment and confirm service availability before relying on the generated presentation workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zou-cc/skills/ai-ppt-generator-1-1-4)
- [Baidu AI PPT API](https://qianfan.baidubce.com/v2/tools/ai_ppt/)
- [Baidu AI PPT Theme Endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output, ending with a PowerPoint URL when generation completes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; PPT generation may take several minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
