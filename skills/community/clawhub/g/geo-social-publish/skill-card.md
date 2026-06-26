## Description: <br>
Deprecated Geo Social Publish documents a legacy GEO content export and local social publishing workflow, while directing users to the newer SaaS download and Rongmeibao batch-publishing process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this deprecated skill as historical reference for exporting generated GEO content, using local publishing tools, and reporting publish status back to the SaaS. New tasks should prefer the replacement SaaS download and Rongmeibao workflow described by the release evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated but still contains actionable steps for authenticated publishing. <br>
Mitigation: Use it only as historical reference, prefer the supported replacement workflow, and supervise any authenticated API call or publish command. <br>
Risk: The workflow references local API keys, OAuth sessions, and publishing cookies. <br>
Mitigation: Treat local credentials as sensitive, confirm content before upload, and keep credential storage local and access-controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/geo-social-publish) <br>
- [GEO SaaS base URL](https://ai.gaobobo.cn) <br>
- [Social Auto Upload download](https://ai.gaobobo.cn/downloads/social-auto-upload.zip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deprecated; requires supervised handling of local credentials, OAuth sessions, and authenticated publishing commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
