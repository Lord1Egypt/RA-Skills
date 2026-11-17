## Description:

Generates V12-style interactive HTML competitive intelligence reports for automotive NVH acoustic sealing and structural reinforcement using supplied company, competitor, and patent-search inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Business, patent-intelligence, and product strategy teams use this skill to create offline HTML briefings comparing a company against named competitors in automotive acoustic sealing and structural reinforcement. Full data-backed conclusions require the configured PatSnap MCP service; without it, the skill provides a report framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill may overstate its analysis capabilities.

Mitigation: Treat generated reports as customized static templates unless authorized PatSnap data and reviewed inputs support the conclusions.

Risk: The security review says user-controlled values can be written into generated HTML and the output path can be arbitrary.

Mitigation: Use trusted input values, run in a low-privilege workspace, and constrain the output path before use.

## Reference(s):

- [V12 HTML template](references/template_v12.html)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/competitive-intel-report)

## Skill Output:

**Output Type(s):** [files, code, guidance]

**Output Format:** [Single-file HTML report with optional Markdown guidance and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure CSS V12 template output; generated reports can be downloaded or printed to PDF.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
