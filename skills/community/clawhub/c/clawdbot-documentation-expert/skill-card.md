## Description: <br>
Expert guidance on navigating, understanding, configuring, troubleshooting, and automating Clawdbot using official documentation and config snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janhcla](https://clawhub.ai/user/janhcla) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to find Clawdbot documentation, retrieve relevant pages, summarize documentation categories, and apply configuration snippets for setup, troubleshooting, automation, and deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts may contact docs.clawd.bot and store a local documentation cache under ~/.cache/clawddocs. <br>
Mitigation: Run the scripts only where documentation network access and local caching are acceptable; review or clear the cache according to local policy. <br>
Risk: Configuration snippets include placeholder token and key fields that could be mistaken for places to share real secrets. <br>
Mitigation: Keep real secrets out of shared examples and replace placeholders only in private configuration files managed by the user. <br>


## Reference(s): <br>
- [Clawdbot documentation](https://docs.clawd.bot) <br>
- [Common Clawdbot Configuration Snippets](snippets/common-configs.md) <br>
- [ClawHub skill page](https://clawhub.ai/janhcla/clawdbot-documentation-expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, links, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference helper scripts that search, fetch, cache, index, and compare Clawdbot documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
