## Description: <br>
Gemini CLI for one-shot Q&A, summaries, and generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenbaiyujason](https://clawhub.ai/user/chenbaiyujason) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Gemini CLI for one-shot answers, summaries, generation, and larger outputs that should be saved to files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The file-output helper can write or overwrite files outside the advertised output folder. <br>
Mitigation: Use the default output location, avoid absolute paths or traversal-like filenames, and review target paths before using file-output mode. <br>
Risk: Prompts and generated outputs may be saved locally and processed by the Gemini CLI account configured on the machine. <br>
Mitigation: Avoid sensitive prompts unless local saved output is intended, and confirm which Gemini account the CLI is logged into before use. <br>


## Reference(s): <br>
- [Gemini developer documentation](https://ai.google.dev/) <br>
- [ClawHub gemini-file release](https://clawhub.ai/chenbaiyujason/gemini-file) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON file-path responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File-output mode returns an absolute file_path and can optionally include generated content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
