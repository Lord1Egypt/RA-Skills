## Description: <br>
Domain threat scores, content categories, and deep intelligence using alphaMountain.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skibum3d](https://clawhub.ai/user/skibum3d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, developers, and incident responders use this skill to query alphaMountain.ai for domain-level threat scores, content categories, popularity, DGA probability, WHOIS, DNS, geolocation, passive DNS, impersonation, and related-host intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried hostnames or URL-derived hostnames are sent to alphaMountain.ai. <br>
Mitigation: Avoid submitting confidential internal domains unless approved. <br>
Risk: The skill requires an alphaMountain API key for lookups. <br>
Mitigation: Use a dedicated or limited API key where possible and avoid exposing it in conversation or logs. <br>


## Reference(s): <br>
- [AlphaMountain API skill on ClawHub](https://clawhub.ai/skibum3d/alphamountain) <br>
- [alphaMountain Threat Intelligence Feeds API](https://www.alphamountain.ai/threat-intelligence-feeds-api/) <br>
- [alphaMountain hostname intelligence endpoint](https://api.alphamountain.ai/intelligence/hostname) <br>
- [alphaMountain license info endpoint](https://api.alphamountain.ai/license/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables derived from alphaMountain API JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALPHAMOUNTAIN_API_KEY; queried hostnames are sent to alphaMountain.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
