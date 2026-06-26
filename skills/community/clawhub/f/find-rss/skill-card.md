## Description: <br>
Discover RSS and Atom feeds for websites so users can subscribe to updates or monitor content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and content-monitoring users use this skill to locate RSS or Atom feed URLs for public websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes web requests to the user-supplied URL and common feed paths. <br>
Mitigation: Use it only with public websites you intend to query, and avoid localhost, private network hosts, internal services, or sensitive URLs. <br>
Risk: Some websites may block automated requests, omit feed links from static HTML, or rate limit repeated checks. <br>
Mitigation: Treat a not-found result as inconclusive and verify manually through the website footer, documentation, or a trusted feed reader. <br>


## Reference(s): <br>
- [Find RSS on ClawHub](https://clawhub.ai/yangzhe1991/find-rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with discovered feed URLs and short guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a bash script against the user-supplied website URL and common feed paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
