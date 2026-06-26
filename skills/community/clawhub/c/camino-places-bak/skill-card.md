## Description: <br>
Locate places using flexible query formats - free-form search or structured address components. Returns coordinates, addresses, and optional street-level photos. Use for geocoding addresses or finding specific named places. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Valvoc](https://clawhub.ai/user/Valvoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to geocode addresses, find named places, and retrieve coordinates, formatted addresses, and optional street-level imagery through Camino's place lookup API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place searches, addresses, postal codes, and optional photo lookup parameters are sent to Camino's external API. <br>
Mitigation: Avoid submitting sensitive home, customer, or operational locations unless Camino's privacy and retention terms meet the user's requirements. <br>
Risk: The skill depends on an external API key and network API behavior for place lookup results. <br>
Mitigation: Configure CAMINO_API_KEY only in trusted environments and review returned place data before using it in customer-facing or operational decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Valvoc/camino-places-bak) <br>
- [Camino skill activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino search API endpoint](https://api.getcamino.ai/search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; place queries, addresses, postal codes, and optional photo lookup parameters are sent to Camino's external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
