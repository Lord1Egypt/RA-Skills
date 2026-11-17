## Description:

Automates EPUB processing to extract book text and cover assets and generate summaries, framework analysis, checklists, worksheets, flowcharts, and FAQ materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntsnail](https://clawhub.ai/user/ntsnail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn EPUB books into structured reading assets, including extracted text, summaries, analysis files, and optional practice templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically run privileged package installation when dependencies are missing.

Mitigation: Install jq, python3, and unzip separately through approved system setup, and run the skill without sudo privileges.

Risk: The skill processes EPUB archives, which may be untrusted or malformed.

Mitigation: Use only trusted EPUBs, preferably in a sandboxed environment, and review the generated quality report before relying on outputs.

Risk: Generated summaries and framework files may include generic templates rather than reliable book-specific analysis.

Mitigation: Manually review and edit generated summaries, framework analysis, and optional worksheets before using them as final analysis.

## Reference(s):

- [ClawHub Book Processor release page](https://clawhub.ai/ntsnail/skills/book-processor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Generated book asset files, including text, Markdown, Mermaid, JSON configuration, and image outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an EPUB input and supports optional process_config.json flags that control additional generated assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
