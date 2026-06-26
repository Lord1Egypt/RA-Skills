## Description: <br>
A design-only workflow designer for the Dify and Coze platforms that produces structured workflow JSON as text output without running bundled scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chikawa11](https://clawhub.ai/user/chikawa11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to design Dify or Coze automation workflows from conversational requirements. It emits node selections, design rationale, and parseable workflow JSON for review or downstream import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflows can include code, HTTP-request, search, file, or credential-related nodes that may perform active automation after import. <br>
Mitigation: Review generated workflow JSON and any credential-bearing fields before importing or running it. <br>
Risk: Optional converter utilities write local Dify YAML or Coze ZIP artifacts when run manually. <br>
Mitigation: Run converter scripts only when local export is intended and choose an appropriate output directory. <br>
Risk: The generated workflow may contain incorrect node schemas or variable references if requirements are ambiguous. <br>
Mitigation: Validate the emitted JSON against the selected platform documentation and inspect the variable checklist before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chikawa11/chat2workflow) <br>
- [Dify node documentation](artifact/node_docs/dify.md) <br>
- [Coze node documentation](artifact/node_docs/coze.md) <br>
- [Converter utility usage](artifact/CONVERTER_USAGE.md) <br>
- [Safety audit](artifact/SAFETY_AUDIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration guidance] <br>
**Output Format:** [Tagged text sections containing node selection, design principle, and raw workflow JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow JSON is intended to be reviewed before import or execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
