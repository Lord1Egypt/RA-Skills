## Description: <br>
Turn websites into CLI commands across 36 platforms and 103 commands using OpenClaw's browser directly, without an extra extension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yan5xu](https://clawhub.ai/user/yan5xu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to discover and run bb-browser site adapters that extract structured data from web pages through OpenClaw's browser session. It is useful for command-line access to social, developer, news, finance, video, and knowledge sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use logged-in browser sessions across many sites, which may expose authenticated account data to adapter commands. <br>
Mitigation: Use a separate or low-privilege browser profile where practical, and only run commands against accounts and pages intended for automation. <br>
Risk: The skill relies on bb-browser adapters and includes update capability for community adapters. <br>
Mitigation: Install only if you trust bb-browser and the adapter source, and review the specific site command before allowing it to access authenticated pages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yan5xu/bb-browser-sites) <br>
- [Publisher profile](https://clawhub.ai/user/yan5xu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return JSON and jq-filtered structured data through bb-browser site adapters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
