## Description:

Researches industry reports and checks figures to create editable, source-traceable PowerPoint briefings with chart data and speaker notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and business teams use this skill to research an industry and prepare management-ready, editable presentations with checked chart figures, speaker notes, and slide-level sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Required JishuDB setup may install a local application and change MCP client configuration.

Mitigation: Review the installation plan and configuration changes and obtain explicit authorization before setup.

Risk: Research and presentation records may persist in JishuDB.

Mitigation: Confirm the destination and retention consent before transferring or saving source material.

Risk: The Windows helper invokes PowerShell despite setup text saying it must not.

Mitigation: Review the Windows helper and reconcile the documentation mismatch before installation.

Risk: Setup downloads application components from CNB or GitHub.

Mitigation: Review the expected download sources and verify downloads before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bowen-aijishu/skills/end-to-end-industry-presentations)
- [Skill homepage (listed in release metadata; not verified import provenance)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/end-to-end-industry-presentations)
- [Evidence contract](references/evidence-contract.md)

## Skill Output:

**Output Type(s):** [Editable presentation, Markdown, CSV chart data, Research records]

**Output Format:** [Editable PPTX, Markdown slide notes and source mappings, CSV, and JishuDB records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes speaker notes, slide-level citations, and a source appendix.]

## Skill Version(s):

0.1.17 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
