## Description: <br>
Formats and beautifies WeChat public account and Xiaohongshu articles with Markdown rendering, 30 preset styles, style selection, and image workflow guidance; it does not publish content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superxs777](https://clawhub.ai/user/superxs777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to normalize WeChat and Xiaohongshu article drafts, render Markdown into styled HTML, list available styles, and get image workflow guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the formatter executes third-party Python code and dependencies. <br>
Mitigation: Verify the linked project and requirements, pin a release tag, and run it in an isolated Python environment or container without root privileges. <br>
Risk: Optional image workflows may require OpenAI, Google, or DashScope API keys. <br>
Mitigation: Configure only the keys needed for those workflows, keep them out of chat and version control, and avoid commands that print environment files. <br>
Risk: Shell execution could be misused if expanded beyond the documented formatter script. <br>
Mitigation: Use only the documented ffformat_cli.py JSON commands and prefer content files for longer input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superxs777/fastfish-format) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/superxs777) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command examples and formatter responses that can include Markdown or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python CLI commands; optional image workflows may require separately configured API keys.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
