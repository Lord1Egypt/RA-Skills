## Description:

The intelligent PPT generation tool is provided by Baidu and generates PPT files from user themes, questions, selected themes, templates, custom templates, and optional resource files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiduqianfangroup](https://clawhub.ai/user/baiduqianfangroup)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Baidu PPT themes, generate a presentation outline, optionally edit the outline in markdown, and request a downloadable PPT file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, outlines, document URLs, and template URLs are sent to Baidu Qianfan PPT APIs.

Mitigation: Do not submit confidential content unless your organization permits sending that content to Baidu.

Risk: The skill requires a BAIDU_API_KEY for API access.

Mitigation: Provide the API key through a managed environment secret and avoid placing it in prompts, command history, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiduqianfangroup/skills/ai-ppt-generate)
- [Baidu Qianfan PPT theme API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)
- [Baidu Qianfan PPT outline API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_outline)
- [Baidu Qianfan PPT generation API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_ppt_by_outline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown outline guidance, JSON API responses, and a PPT download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and network access to Baidu Qianfan PPT APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
