## Description: <br>
This release is published as a flight-status checker, but the submitted artifact describes and implements a hotel aggregation assistant for searching, comparing, and formatting hotel results across multiple travel platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents would use the artifact for hotel search aggregation, price comparison, and formatted hotel-result summaries. It should not be treated as a flight-status checker unless the publisher replaces or clarifies the submitted implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public identity advertises a flight-status checker while the submitted artifact implements hotel aggregation behavior. <br>
Mitigation: Review the package before installing and use it only if the intended task is hotel search or aggregation. <br>
Risk: The skill claims real-time hotel data and booking capabilities, while the visible provider search methods are placeholders. <br>
Mitigation: Verify working provider integrations and data-source authorization before relying on search results, prices, availability, or booking flows. <br>
Risk: Hotel searches and booking flows may involve location, travel dates, and other user-provided travel details sent to external services. <br>
Mitigation: Confirm privacy terms, user consent, and data handling requirements before enabling external searches or bookings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/flight-status-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API calls] <br>
**Output Format:** [JSON responses and Markdown-style tabular summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; visible provider integrations are placeholders and should be verified before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
