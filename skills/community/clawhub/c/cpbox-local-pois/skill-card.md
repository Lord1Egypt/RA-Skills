## Description: <br>
Gets local business and point-of-interest details from cpbox.io for POI IDs returned by a prior web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve full local business details, including hours, address, contact information, ratings, categories, price range, and optional distance for POIs found by a prior location-filtered web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests use x402 pay-per-use payment tooling and may incur charges. <br>
Mitigation: Install only after completing the x402-payment setup and confirm payment expectations before sending requests. <br>
Risk: Optional latitude and longitude headers can disclose precise user location. <br>
Mitigation: Omit exact coordinates unless distance results are needed, and use the least precise location that supports the task. <br>
Risk: POI IDs expire after about 8 hours and cannot be refreshed. <br>
Mitigation: Fetch fresh POI IDs with web-search result_filter=locations and avoid caching IDs beyond their stated TTL. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sprintmint/cpbox-local-pois) <br>
- [x402 payment setup prerequisites](https://github.com/springmint/cpbox-skills#prerequisites) <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [Local POIs API endpoint](https://www.cpbox.io/api/x402/local-pois) <br>
- [CP Pay facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown with HTTP and bash examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 1-20 POI IDs from prior web-search location results; optional location headers enable distance calculations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
