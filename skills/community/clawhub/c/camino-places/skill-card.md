## Description: <br>
Places helps agents geocode addresses and find named places through Camino's API, returning coordinates, addresses, and optional street-level imagery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up landmarks, points of interest, postal codes, or structured addresses and receive geocoded place results for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place, address, home, workplace, or other private location queries are sent to Camino's API using the configured Camino API key. <br>
Mitigation: Use a Camino API key intended for this integration and avoid submitting sensitive private location queries unless Camino processing is acceptable. <br>
Risk: Installing the broader Camino skill suite can add behavior outside this Places skill. <br>
Mitigation: Install only camino-places unless the wider Camino skill suite has been reviewed for the target environment. <br>


## Reference(s): <br>
- [ClawHub Places skill page](https://clawhub.ai/james-southendsolutions/camino-places) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino search API endpoint](https://api.getcamino.ai/search) <br>
- [x402 payment protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON place-search results returned by a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; accepts a free-form query or structured address JSON.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
