## Description:

BOM Compare Tool compares two versions of a bill of materials and identifies added, removed, quantity-changed, specification-changed, and price-changed material items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, procurement teams, and BOM reviewers use this skill to compare old and new BOM files for design changes, supplier reconciliation, procurement-to-engineering checks, and version upgrade analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BOM data from untrusted parties could include crafted values that make terminal output misleading.

Mitigation: Use trusted BOM inputs where possible, review comparison results in a controlled terminal, and validate material changes before acting on them.

Risk: The workflow and report text are Chinese-language, which may be unsuitable for teams that require another language.

Mitigation: Install only when a Chinese-language BOM comparison workflow is acceptable, or translate and review outputs before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/bom-compare-tool)
- [Publisher profile](https://clawhub.ai/user/yongjie666888)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code]

**Output Format:** [Markdown or terminal text report summarizing BOM differences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language report content; compares CSV or XLSX BOM inputs when used with the bundled script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
