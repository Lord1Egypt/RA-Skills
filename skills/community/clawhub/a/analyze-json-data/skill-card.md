## Description: <br>
Analyze JSON data and generate a structured API design document or OpenAPI specification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect JSON data and turn observed structures into an API design document or OpenAPI 3.0 specification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks for an API key even though the visible local JSON-to-OpenAPI implementation does not explain what service needs it. <br>
Mitigation: Review before installing, and do not provide an API key unless the publisher documents why it is needed and whether JSON data is transmitted off-host. <br>
Risk: The skill analyzes user-provided JSON and can write output files, so unsuitable input files or unintended paths could expose or overwrite data. <br>
Mitigation: Use only JSON files intended for analysis and choose output paths deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/analyze-json-data) <br>
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON OpenAPI 3.0 specification] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an OpenAPI JSON file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; changelog released 2026-05-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
