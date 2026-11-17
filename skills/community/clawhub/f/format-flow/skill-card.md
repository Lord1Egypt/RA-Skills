## Description:

Convert and format documents across Word, PDF, Markdown, web pages, Excel, and images with compression, resizing, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sashavegal](https://clawhub.ai/user/sashavegal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to convert documents and web pages, format text, export spreadsheet data to JSON, and process image files through agent-guided shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency installation can modify the active Python environment.

Mitigation: Review and install dependencies in an isolated virtual environment before running the converter.

Risk: Web conversion can fetch arbitrary URLs and make outbound network requests.

Mitigation: Use trusted or allowlisted URLs, and avoid attacker-supplied web inputs unless network behavior is controlled.

Risk: Batch and recursive conversion can process broad folder scopes and create or overwrite many output files.

Mitigation: Check the target path and run on a controlled copy of files before using broad batch or recursive modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sashavegal/skills/format-flow)
- [Publisher profile](https://clawhub.ai/user/sashavegal)
- [Pandoc installation documentation](https://pandoc.org/installing.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and converted document, JSON, and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify output files next to input files or in specified output paths; batch and recursive modes can process many files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
