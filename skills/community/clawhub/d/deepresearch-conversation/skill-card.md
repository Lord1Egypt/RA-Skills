## Description: <br>
Qianfan DeepResearch automates Baidu Qianfan DeepResearch report generation, including conversation creation, research execution, clarification skipping, outline confirmation, and Markdown and HTML report link retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and research analysts use this skill to run Qianfan DeepResearch workflows for structured long-form research reports, such as market research, competitive analysis, technical overviews, policy interpretation, and decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends research topics, generated outlines, and API key-authorized usage to Baidu Qianfan. <br>
Mitigation: Use QIANFAN_API_KEY from a secure environment, avoid pasting keys into chat or command history, and run only when sending the research topic to Qianfan is acceptable. <br>
Risk: The workflow automatically skips clarification and confirms the generated outline, so vague or incorrect queries can produce low-quality or unintended reports. <br>
Mitigation: Review and refine the query and depth selection before execution, and ask for clarification when the research topic is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/deepresearch-conversation) <br>
- [DeepResearch API reference](references/api.md) <br>
- [DeepResearch workflow reference](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with report outline text and Markdown and HTML download links from stdout JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Qianfan API key and may run for 10 to 30 minutes.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
