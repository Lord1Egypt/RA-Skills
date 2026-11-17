## Description:

Reviews embedded C/C++ source for common safety and correctness issues, maps findings to relevant MISRA rules where supported, and can produce a shareable Chinese HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embedded engineers use this skill to review C/C++ firmware for defects such as unsafe interrupt behavior, memory errors, and concurrency issues. It returns prioritized findings with source locations, fix advice, and supported MISRA references for code review or CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence and partial coverage because a referenced local path was not present in the scanned bundle.

Mitigation: Confirm the referenced file is available and review it before relying on the assessment.

Risk: The reviewer reads supplied files and can write an optional HTML report; the security guidance notes that its file scope is not declared.

Mitigation: Point it at intended source files or directories, choose a deliberate report destination, and review findings before acting on the fix advice.

Risk: Optional HTML reports are Chinese-language, which may limit review by readers who do not read Chinese.

Mitigation: Use the text output or have a Chinese-reading reviewer assess the HTML report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujycode/skills/embedded-code-reviewer)
- [MISRA mapping](artifact/references/misra-mapping.md)
- [Changelog](artifact/references/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Files]

**Output Format:** [Severity-ranked review findings; optional Chinese-language HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include source locations, root causes, fix advice, and relevant MISRA references; CI-friendly exit status.]

## Skill Version(s):

1.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
