## Description: <br>
Provides a paid x402 web-search proxy that returns ranked web, news, video, discussion, FAQ, infobox, and location results with snippets, URLs, thumbnails, freshness filters, SafeSearch, Goggles, and pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI agents use this skill to run paid, structured web searches for search interfaces, data extraction, custom ranking, and retrieval-augmented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid searches can trigger external requests and automatic x402 payment signing without clear spend controls. <br>
Mitigation: Use a dedicated low-balance wallet, require confirmation or a fixed budget for paid searches, and verify the external payment helper package before use. <br>
Risk: Location-aware searches can send precise location headers to the service. <br>
Mitigation: Send location headers only when the user explicitly needs location-aware results, and omit precise coordinates when they are not required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sprintmint/cpbox-web-search) <br>
- [x402 payment setup steps](https://github.com/springmint/cpbox-skills#prerequisites) <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [CPPay facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON search response with ranked result objects, snippets, URLs, thumbnails, and optional rich callback metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a query string and supports optional country, language, count, offset, SafeSearch, freshness, result filters, Goggles, rich callbacks, and location headers.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
