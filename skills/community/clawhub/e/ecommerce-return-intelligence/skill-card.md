## Description: <br>
Analyzes ecommerce return reasons and distinguishes product problems, expectation mismatches, logistics issues, and description issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, analysts, and support teams use this skill to review return records, classify return reasons, identify frequent issues, and prepare reviewable follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer return records may include personal or sensitive data. <br>
Mitigation: Desensitize customer personal information before analysis and process only files intentionally selected for review. <br>
Risk: The local Python helper can read selected files and write a report to a chosen output path. <br>
Mitigation: Use explicit input and output paths, choose the output location carefully, and avoid pointing the helper at unrelated private directories. <br>
Risk: Return classifications can be incomplete or misleading when source records lack reason text or product context. <br>
Mitigation: List missing information and require human review before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/ecommerce-return-intelligence) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](README.md) <br>
- [Skill specification](resources/spec.json) <br>
- [Output template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 when using the local helper script; can also produce structured text directly from the provided template and specification.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
