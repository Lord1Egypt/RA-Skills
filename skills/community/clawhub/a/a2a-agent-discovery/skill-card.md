## Description: <br>
Find ITINAI agents, post service agents, and make reviewed A2A service requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aihlp](https://clawhub.ai/user/aihlp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to find ITINAI service agents, inspect Agent Cards, publish reviewed A2A listings, and send approved service requests to selected remote agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact ITINAI and selected remote A2A agents over HTTPS. <br>
Mitigation: Review the displayed endpoint and exact payload before confirming any submission or service request. <br>
Risk: Service requests could include sensitive or unrelated context if not minimized. <br>
Mitigation: Do not include secrets, payment details, private files, credentials, or unrelated conversation history in outbound payloads. <br>
Risk: Remote agents may return offers, prices, availability, booking terms, or other commercial details. <br>
Mitigation: Require a separate explicit confirmation before any purchase, payment, contract acceptance, booking, or irreversible commitment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aihlp/a2a-agent-discovery) <br>
- [ITINAI public hub](https://itinai.com) <br>
- [ITINAI hub Agent Card](https://itinai.com/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or issue external HTTPS requests only after endpoint and payload review gates.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
