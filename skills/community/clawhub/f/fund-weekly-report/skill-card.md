## Description:

Fund Weekly Report generates Chinese fund weekly report Word documents from Excel data, covering active equity, fixed income, index funds, FOFs, QDII, REITs, and related weekly performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujing2013](https://clawhub.ai/user/yujing2013)

### License/Terms of Use:

MIT-0

## Use Case:

External users and fund analysts use this skill to transform provided weekly fund return workbooks, and optionally ETF flow workbooks, into a structured Chinese weekly fund report. It is intended for report drafting and data-driven narrative generation from trusted local inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill's file access and output behavior exceed the safety limits claimed in its documentation.

Mitigation: Review before installing, use only trusted local inputs, avoid arbitrary local paths, constrain reads to uploaded files or an approved workspace, and prevent report overwrites.

Risk: The server guidance warns against running legacy generator scripts against untrusted requests.

Mitigation: Run only reviewed scripts in a controlled workspace and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujing2013/skills/fund-weekly-report)
- [Fund Weekly Report skill definition](artifact/SKILL.md)
- [Chapter breakdown](artifact/references/chapter_breakdown.md)
- [Excel data mapping rules](artifact/references/data_mapping.md)
- [Data processing logic](artifact/references/data_processing_logic.md)
- [ETF flow data usage](artifact/references/etf_flow_usage.md)
- [Word template usage](artifact/references/template_usage.md)
- [Writing templates](artifact/references/writing_templates.md)
- [Improved writing templates](artifact/references/writing_templates_v2.md)
- [Learned report writing templates](artifact/references/writing_templates_v3_learned.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Microsoft Word document with agent-facing text, Markdown, code, and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Excel input files and writes the generated report to the user's working directory.]

## Skill Version(s):

1.8.3 (source: server release metadata; artifact frontmatter reports 1.8.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
