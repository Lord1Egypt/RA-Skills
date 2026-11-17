## Description:

Detects and reduces AI-writing markers in Chinese text, with support for pasted text or file input and outputs rewritten text plus comparison reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Chinese-language content authors use this skill to detect common AI-writing patterns, rewrite text for a more natural tone, and compare detection scores before and after rewriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File and batch examples can create or overwrite rewritten output files.

Mitigation: Review output paths before running file or batch commands.

Risk: Optional style conversion can change tone beyond simple AI-marker reduction.

Mitigation: Review rewritten text to confirm it preserves the intended meaning, tone, and context.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with optional JSON detection output and rewritten files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdin, file input, batch examples, scene selection, optional style conversion, and local output files.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
