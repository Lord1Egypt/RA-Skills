## Description: <br>
Query Gangtise knowledge base API to search and retrieve financial/market information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmaya](https://clawhub.ai/user/hmaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to configure Gangtise API credentials and query Gangtise knowledge base content for stocks, companies, market concepts, financial reports, and related market information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled or mishandled credentials can expose Gangtise access keys and secret keys. <br>
Mitigation: Remove bundled credentials, configure only scoped user-owned Gangtise keys, and keep credential files restricted. <br>
Risk: Disabled TLS certificate validation can weaken HTTPS protections for authentication and query traffic. <br>
Mitigation: Re-enable normal TLS certificate validation before operational use. <br>
Risk: Passing access tokens on the command line can expose tokens through shell history or process inspection. <br>
Mitigation: Avoid command-line token arguments and use safer credential or token handling. <br>
Risk: Sensitive portfolio or proprietary research queries may be sent to the Gangtise API. <br>
Mitigation: Avoid sending sensitive queries until credential handling and transport security issues are fixed. <br>


## Reference(s): <br>
- [Gangtise Open Platform](https://open.gangtise.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/hmaya/gangtise-kb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return formatted search results or raw JSON from the Gangtise knowledge base API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
