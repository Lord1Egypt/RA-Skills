## Description:

Generates PowerPoint outlines and downloadable PPT files from user themes, questions, optional resource URLs, and selected Baidu Qianfan templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-owo](https://clawhub.ai/user/lulu-owo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to help end users build presentation outlines and request generated PPT download URLs through Baidu Qianfan's AI PPT APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation prompts, outlines, resource links, template links, and BAIDU_API_KEY are sent to Baidu's Qianfan service.

Mitigation: Install and use only where Baidu processing is approved for the intended presentation content and credentials.

Risk: Private internal document URLs or regulated data may be exposed if provided as presentation resources.

Mitigation: Avoid private or regulated resources unless the organization has approved Baidu processing for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lulu-owo/skills/ai-ppt-generate-skip2)
- [Baidu Qianfan PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)
- [Baidu Qianfan PPT outline endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_outline)
- [Baidu Qianfan PPT generation endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/generate_ppt_by_outline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts return JSON or streamed events and a downloadable PPT URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BAIDU_API_KEY; optional resource and template URLs may be sent to Baidu Qianfan.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
