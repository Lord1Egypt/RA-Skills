## Description: <br>
Firecrawl Local Search guides agents to use a disclosed local Firecrawl HTTP service for webpage scraping, data extraction, and site search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobowg163](https://clawhub.ai/user/bobowg163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a trusted local Firecrawl service for scraping website content and returning structured results. It is most useful when the local network service at 192.168.1.2:3002 is controlled or explicitly trusted by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to a local-network HTTP Firecrawl service. <br>
Mitigation: Install and use only when 192.168.1.2:3002 is a Firecrawl service you control or trust. <br>
Risk: Submitted URLs or page content may expose sensitive internal resources to that service. <br>
Mitigation: Avoid submitting sensitive internal URLs, tokens in query strings, or private content unless the service and network are appropriate for that data. <br>
Risk: The documentation mentions map and search helper scripts that are not included in this package. <br>
Mitigation: Rely on the included scrape helper or verify any missing helper scripts before using those workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from the local Firecrawl API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a disclosed local-network HTTP endpoint and a Python standard-library helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
