## Description: <br>
Track flights in real-time with detailed status, gate info, delays, and live position. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[copey02](https://clawhub.ai/user/copey02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up flight status by IATA flight number and present departure, arrival, gate, delay, aircraft, and live-position details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free AviationStack setup sends the API key and flight lookup over plain HTTP. <br>
Mitigation: Use a dedicated low-value API key, rotate it if exposed, avoid sensitive travel lookups on untrusted networks, and prefer an HTTPS-capable paid plan or another provider for production or private use. <br>


## Reference(s): <br>
- [AviationStack API Setup](references/api-setup.md) <br>
- [AviationStack Free API Signup](https://aviationstack.com/signup/free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown-style terminal text or raw JSON from the flight tracking script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AviationStack API key in AVIATIONSTACK_API_KEY and the Python requests dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
