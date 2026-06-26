## Description: <br>
A hotel aggregation skill that helps an agent search hotels, compare room prices, and format booking-oriented results across Fenbeitong, Ctrip, Meituan, Tongcheng, Huazhu, and Jinjiang. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel assistants use this skill to aggregate hotel search results, compare room and price options, and present booking-oriented summaries from multiple travel providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release name says flight ticket helper, while the artifact implements hotel aggregation. <br>
Mitigation: Confirm the intended domain before installation and treat this release as a hotel aggregation assistant until the publisher fixes the mismatch. <br>
Risk: The security evidence says the skill overclaims live booking and search behavior, and the artifact contains placeholder provider integrations. <br>
Mitigation: Do not rely on prices, availability, room details, or booking claims until the publisher implements and validates the advertised provider integrations. <br>
Risk: Travel search details may be shared with several outside providers without clear data-sharing documentation. <br>
Mitigation: Avoid sending sensitive travel or personal data until provider data flows, dependencies, and privacy expectations are documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/air-ticket-helper) <br>
- [Publisher profile](https://clawhub.ai/user/ryan-zry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, guidance] <br>
**Output Format:** [Markdown tables, JSON-style function results, and Python adapter code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. The skill instructs the agent to use real provider API data, preserve source attribution, and avoid inventing hotel prices, inventory, or room details.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
