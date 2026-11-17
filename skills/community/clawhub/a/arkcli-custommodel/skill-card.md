## Description:

Manages Ark custom models by importing, listing, inspecting, updating, deleting, and quantizing them, and explains that inference requires an endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage custom model assets in Ark, including importing weights from TOS and preparing ready models for deployment. It also helps distinguish custom model IDs from inference endpoints and routes unrelated foundation model or endpoint tasks to the appropriate workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is partial because two local path references could not be matched to bundled files.

Mitigation: Review and resolve the referenced companion material before relying on instructions that depend on it.

## Reference(s):

- [Custom model list and search](artifact/references/arkcli-custommodel-list.md)
- [Custom model details and endpoint references](artifact/references/arkcli-custommodel-get.md)
- [Import custom model weights](artifact/references/arkcli-custommodel-upload.md)
- [Update custom model metadata](artifact/references/arkcli-custommodel-update.md)
- [Delete a custom model](artifact/references/arkcli-custommodel-delete.md)
- [Available quantization modes](artifact/references/arkcli-custommodel-available-quantizations.md)
- [Quantize a custom model](artifact/references/arkcli-custommodel-quantize.md)
- [Volcengine TOS documentation](https://www.volcengine.com/docs/6349/74820?lang=zh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with arkcli commands and structured CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require user confirmation; asynchronous imports and quantization require status follow-up.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
