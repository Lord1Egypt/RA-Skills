## Description: <br>
DinzeeAgent helps agents discover and call Dinzee gateway e-commerce data tools for ASIN, keyword, traffic, and ad research for Amazon sellers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yefeng311](https://clawhub.ai/user/yefeng311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research Amazon marketplace products and campaigns by discovering available Dinzee providers, invoking selected data tools, and summarizing the returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user integration token and routes requests through a paid third-party data gateway. <br>
Mitigation: Use an environment variable for the token when possible, keep it revocable, and confirm pricing before paid tool calls. <br>
Risk: The skill can install or update local agent skills from gateway-delivered packages. <br>
Mitigation: Use install and update commands only when the Dinzee gateway is trusted as a software delivery channel, and review delivered files before relying on them. <br>


## Reference(s): <br>
- [Dinzee Gateway](https://gateway.dinzee.ai/) <br>
- [ClawHub Skill Page](https://clawhub.ai/yefeng311/dinzee-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/yefeng311) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke paid gateway calls and may write installed skill files when users request skill installation or updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
