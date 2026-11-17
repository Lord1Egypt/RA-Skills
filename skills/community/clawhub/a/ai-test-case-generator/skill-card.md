## Description:

Generates structured QA test cases from requirements using test-design methods such as equivalence partitioning, scenario analysis, orthogonal decomposition, and state-transition analysis, with Markdown output and optional Excel conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lianwilliam](https://clawhub.ai/user/lianwilliam)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, test teams, and developers use this skill to turn product requirements into comprehensive functional, boundary, exception-flow, and risk-prioritized test cases. It can also provide commands to convert generated Markdown test cases into an Excel file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases may be sent to an external conversion service over insecure HTTP transport.

Mitigation: Use the Excel export only for non-confidential requirements, or require explicit approval and an HTTPS-only approved conversion path before sending generated content.

Risk: The generated test cases may contain incomplete, incorrect, or misleading coverage recommendations.

Mitigation: Have a qualified tester review the Markdown test cases before importing them into a test management or execution workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lianwilliam/skills/ai-test-case-generator)
- [Markdown-to-Excel conversion endpoint](http://office-tools.wh.ctrm.5636cloud.com/api/v1/office/md-to-excel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown test cases with optional shell or Python conversion commands and an Excel download link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send generated test-case content to an external HTTP conversion service when Excel export is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
