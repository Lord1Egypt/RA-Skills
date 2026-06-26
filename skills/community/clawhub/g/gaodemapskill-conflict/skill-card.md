## Description: <br>
A skill to interact with Gaode Map (AMap) for location search and route planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Beelkic](https://clawhub.ai/user/Beelkic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Gaode Map places, geocode addresses, and plan driving, walking, bicycling, or transit routes through a Python command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, addresses, coordinates, route details, and the AMap API key are sent to Gaode/AMap. <br>
Mitigation: Avoid highly sensitive locations unless needed, use the AMAP_API_KEY environment variable, and review the data sharing implications before installation. <br>
Risk: Passing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Store AMAP_API_KEY in the environment or agent configuration instead of using the --key argument. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Beelkic/gaodemapskill-conflict) <br>
- [Beelkic publisher profile](https://clawhub.ai/user/Beelkic) <br>
- [AMap Console](https://console.amap.com/) <br>
- [AMap REST API endpoint](https://restapi.amap.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from a Python command-line tool, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, the requests package, and an AMAP_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
