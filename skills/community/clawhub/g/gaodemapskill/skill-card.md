## Description: <br>
A skill to interact with Gaode Map (AMap) for location search and route planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search places, geocode addresses, and plan driving, walking, bicycling, or transit routes through the Gaode Map API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, coordinates, and route details are sent to Gaode/AMap under the user's API key. <br>
Mitigation: Use the skill only for data acceptable to share with Gaode/AMap and review provider terms before sensitive or regulated use. <br>
Risk: Passing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Set AMAP_API_KEY in the environment or agent configuration instead of using the --key argument. <br>
Risk: The requests dependency is unpinned. <br>
Mitigation: Pin and review dependencies before production or sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/279458179/gaodemapskill) <br>
- [AMap Console](https://console.amap.com/) <br>
- [AMap REST API endpoint](https://restapi.amap.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from a Python command-line tool, with markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY and the Python requests package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
