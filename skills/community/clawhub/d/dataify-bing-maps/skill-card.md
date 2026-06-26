## Description: <br>
When the user uses Bing Maps to search for locations or view maps, this skill is executed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to turn natural-language Bing Maps requests into Dataify Bing Maps API parameters, review the generated parameter table, and run confirmed map or place searches through Dataify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bing Maps search terms, coordinates, place IDs, and request parameters are sent to Dataify during confirmed live calls. <br>
Mitigation: Use the skill only when sharing those parameters with Dataify is acceptable, and review the generated parameter table before confirming a live call. <br>
Risk: A broad or reused Dataify API token could increase exposure if mishandled. <br>
Mitigation: Use a dedicated Dataify token for this skill and provide it only through the supported token argument or environment variable. <br>
Risk: Locale-sensitive requests may use an unintended language or region if `setlang` is omitted. <br>
Mitigation: Set `setlang` explicitly when language or regional behavior matters. <br>


## Reference(s): <br>
- [Dataify Bing Maps API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, JSON dry-run payloads, shell commands, and direct Dataify API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live calls require a Dataify API token and explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
