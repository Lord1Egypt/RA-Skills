## Description: <br>
AI-ready skill to test, register, and publish Markdown articles to WeChat Official Accounts using a local custom CSS theme via Wenyan CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caol64](https://clawhub.ai/user/caol64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agent operators use this skill to preview Markdown with a local Wenyan CSS theme, publish it to a WeChat Official Account draft, and optionally register reusable local themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing uses WeChat account credentials and can create drafts in the target Official Account. <br>
Mitigation: Keep WECHAT_APP_ID and WECHAT_APP_SECRET out of logs and shared files, and require the agent to show the target account context before running the publish command. <br>
Risk: The workflow executes wenyan-cli commands against user-provided Markdown and CSS paths. <br>
Mitigation: Verify the wenyan-cli package source before installing, confirm the Markdown and CSS paths, and run the render test before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caol64/apply-wenyan-custom-theme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Wenyan CLI commands and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Markdown and CSS file paths, WeChat API credentials from environment variables, and optional Wenyan CLI theme or highlighting flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
