## Description:

A design-only workflow designer for the Dify and Coze platforms. Through multi-round conversation, it produces a structured workflow JSON (nodes, edges, variable references) as text output. The skill itself produces only text and never runs any scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chikawa11](https://clawhub.ai/user/chikawa11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow builders use Chat2Workflow to design Dify or Coze workflow graphs through conversation. The skill returns tagged text sections with node selection, design rationale, and a raw workflow JSON object that can be reviewed before import or optional conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow JSON can contain Code, HTTP Request, search, or plugin/tool nodes that behave differently after import.

Mitigation: Review generated workflows before importing them into Dify or Coze, with special attention to those node types.

Risk: Secrets pasted into generated workflow JSON may be stored in the workflow artifact.

Mitigation: Do not embed real API keys, passwords, or bearer tokens in generated JSON.

Risk: The optional converter can write files outside the intended output folder when given an unsafe workflow name.

Mitigation: Use simple workflow names containing only letters, digits, underscores, and hyphens, and write to a disposable output directory.

Risk: Optional conversion utilities process local workflow JSON and third-party dependencies.

Mitigation: Run the optional converter only on trusted workflow JSON and consider pinning dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chikawa11/skills/chat2workflow)
- [Chat2Workflow skill source](artifact/SKILL.md)
- [Dify node documentation](artifact/node_docs/dify.md)
- [Coze node documentation](artifact/node_docs/coze.md)
- [Converter utility usage](artifact/CONVERTER_USAGE.md)
- [Safety audit](artifact/SAFETY_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Tagged plain text with a raw JSON workflow section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses use node_selection, design_principle, and workflow tags; the workflow section is raw JSON without outer markdown fences.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
