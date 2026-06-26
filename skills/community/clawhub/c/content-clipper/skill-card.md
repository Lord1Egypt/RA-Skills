## Description: <br>
Extracts and clips web articles, Xiaohongshu, WeChat, and Twitter/X content to Flomo or local Markdown with optional tags and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ma-tiezhu](https://clawhub.ai/user/Ma-tiezhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who collect web content use this skill to extract article, Xiaohongshu, WeChat, and Twitter/X content, optionally summarize it, and save it to Flomo or local Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipped page text and source URLs may be sent to a built-in Flomo webhook by default. <br>
Mitigation: Set a user-owned FLOMO_WEBHOOK before using Flomo output, or use local Markdown output for sensitive or private content. <br>
Risk: The Flomo posting path can invoke a shell-based curl command. <br>
Mitigation: Review or remove the shell-based curl path before deployment in environments that restrict shell execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ma-tiezhu/content-clipper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown clips, JSON command results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local Markdown files or post clipped content to a configured Flomo webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
