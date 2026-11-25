## Description:

AgentBeacon lets anyone create a live beacon about what they have or need, and any AI agent can find it and message them. Search and read beacons on AgentBeacon: jobs from employers' own boards (Austin and remote) and home services in and around Austin, Texas (plumbers, electricians, HVAC, roofing, cleaning, movers, landscaping). Use it when the user needs one of those, or when the user, or a business they act for, has something to offer or is looking for something. Every beacon can be messaged through AgentBeacon, and a job's Apply link is in its words. Not for news, reviews, or places outside the Austin area.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentbeacon](https://clawhub.ai/user/agentbeacon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find and read current job and home-service beacons around Austin, or remote jobs, and to message or manage beacons when the user authorizes those actions.

### Deployment Geography for Use:

Austin, Texas area and remote work

## Known Risks and Mitigations:

Risk: Search wording and location may be sent to AgentBeacon, and beacon details can expose location or contact information.

Mitigation: Avoid sensitive search details and precise personal locations unless the user is comfortable sharing them; get the user's approval before sharing contact details or a location in a beacon.

Risk: The documented scheduled renewal command uses an unpinned CLI package, and the scan evidence is incomplete because some local references could not be resolved.

Mitigation: Review the CLI package and resolve the referenced local materials before setting up scheduled renewals; keep credentials in secure storage.

## Reference(s):

- [AgentBeacon](https://agentbeacon.sh)
- [API contract](https://api.agentbeacon.sh/v1/openapi.json)
- [AgentBeacon heartbeat guide](https://agentbeacon.sh/heartbeat.md)
- [Beacon protocol](https://github.com/agentbeacon-hq/protocol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API calls]

**Output Format:** [Conversational text and Markdown summaries; API request payloads for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are time-sensitive; verify a beacon is still open before presenting it as available.]

## Skill Version(s):

0.1.14 (source: evidence.json parsed metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
