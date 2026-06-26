## Description: <br>
All-in-one content generation, social media publishing, video creation, and image template design via the GenerateBot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osaket](https://clawhub.ai/user/osaket) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and developers use this skill to search topics or URLs, generate articles, social posts, scripts, images, and videos, manage generated content, and publish through GenerateBot-connected CMS or social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GenerateBot API key and may access connected GenerateBot, CMS, and social accounts. <br>
Mitigation: Install only when the user trusts GenerateBot and intends to let an agent operate those connected accounts. <br>
Risk: The skill can publish, delete, bulk-clear, update, or otherwise change account content. <br>
Mitigation: Before any destructive or publishing action, require the agent to show the exact target account, content, destination, and requested change, then get explicit confirmation. <br>
Risk: Paid generation actions can consume GenerateBot credits. <br>
Mitigation: Before any paid generation, require the agent to show the credit cost and receive explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/osaket/content-generator-from-url) <br>
- [GenerateBot Homepage](https://generatebot.com) <br>
- [GenerateBot API Base URL](https://generatebot.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GENERATEBOT_API_KEY; some operations consume credits and can publish, update, or delete connected account content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
