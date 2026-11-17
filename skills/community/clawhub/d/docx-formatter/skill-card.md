## Description:

DOCX Formatter helps agents generate Chinese official-document Word files with standardized title, body, paragraph, page, and punctuation formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rokami](https://clawhub.ai/user/rokami)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to convert Markdown or structured JSON content into Chinese official-format Word documents for reports, summaries, plans, speeches, and related formal materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script adds the python-docx dependency before use.

Mitigation: Install in an isolated environment and consider pinning python-docx before deployment.

Risk: The skill is specialized for Chinese official-document formatting and can be triggered for broad document requests.

Mitigation: Prefer explicit invocation for specific .docx formatting tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rokami/skills/docx-formatter)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Code, Guidance]

**Output Format:** [DOCX files generated from Markdown or JSON content, with optional Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local .docx output files and may install python-docx in a local virtual environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
