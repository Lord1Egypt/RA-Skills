## Description: <br>
Byted Data Search helps agents query and analyze public business, company, industry-chain, and A-share market datasets through Volcengine datasource tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, developers, and business users can use this skill to look up company registrations, listed-company details, industry-chain participants, regional metrics, and grouped statistics from supported public datasets. It guides the agent to inspect datasource metadata before building precise filters, aggregations, sorting, and pagination queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Volcengine credentials and query contents are sent to a remote Volcengine gateway. <br>
Mitigation: Install only if the publisher and endpoint are trusted, use least-privilege Volcengine keys, and prefer environment variables over command-line secrets. <br>
Risk: Overriding the gateway URL could send credentials or business queries to an untrusted host. <br>
Mitigation: Use the default trusted endpoint unless there is a reviewed operational reason to change it. <br>
Risk: Business investigations may include confidential or sensitive context. <br>
Mitigation: Avoid sending confidential investigations through the skill unless the data handling path has been approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-data-search) <br>
- [Volcengine high-quality dataset console](https://console.volcengine.com/high-quality-dataset) <br>
- [Volcengine Access Key documentation](https://www.volcengine.com/docs/6291/65568?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcengine credentials; remote query results depend on selected datasource, filters, and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
