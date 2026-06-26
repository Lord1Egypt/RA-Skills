## Description: <br>
Create short URLs and submit feature requests using 1p.io. Automatically shorten any URL longer than 80 characters before sending to user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanpmt](https://clawhub.ai/user/tuanpmt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, teams, and external users use this skill to register a 1p.io agent, create and manage short links, and submit or vote on organization-scoped feature requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send arbitrary long URLs to an external 1p.io service, including URLs that contain private documents, tokens, signed downloads, reset links, internal hosts, or personal data. <br>
Mitigation: Ask for user confirmation before shortening links and avoid sending sensitive, internal, credential-bearing, or personal-data URLs to the service. <br>
Risk: The skill includes organization link deletion and feature-status editing actions that can alter shared organizational resources. <br>
Mitigation: Grant delete or edit permissions only when needed and require explicit confirmation before destructive or organization-wide changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanpmt/1p-shortlink) <br>
- [1p.io API register endpoint](https://1p.io/api/register) <br>
- [1p.io API shorten endpoint](https://1p.io/api/shorten) <br>
- [1p.io API feature requests endpoint](https://1p.io/api/features) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration, text] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce 1p.io short URLs, API registration guidance, link-management requests, and feature-request operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
