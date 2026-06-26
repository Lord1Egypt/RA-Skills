## Description: <br>
Create, schedule, queue, and manage social media posts and drafts across Buffer-connected profiles using terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmadabugosh](https://clawhub.ai/user/ahmadabugosh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media operators, developers, and agent users use this skill to let an assistant list Buffer profiles, create posts, queue or schedule content, save drafts, and inspect upcoming posts from a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, queue, schedule, or save social content through a Buffer API key without a built-in confirmation step. <br>
Mitigation: Require the assistant to show the final post text, target profile ID, and timing before executing posting commands; prefer draft or queue workflows for content that needs review. <br>
Risk: Using the all-profiles option may send content to more Buffer-connected profiles than intended. <br>
Mitigation: Use explicit profile IDs for routine posting and reserve --all for cases where every connected profile is intentionally targeted. <br>
Risk: The Buffer API key grants account access if exposed in repositories, logs, screenshots, or shared environments. <br>
Mitigation: Store BUFFER_API_KEY only in local secret management or environment configuration and avoid echoing it in assistant-visible output. <br>


## Reference(s): <br>
- [Buffer Developer Docs](https://developers.buffer.com/) <br>
- [Buffer API Key Settings](https://publish.buffer.com/settings/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/ahmadabugosh/buffer-social) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented text with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate Buffer API calls that create, queue, schedule, or draft social media content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
