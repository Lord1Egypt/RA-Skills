## Description: <br>
GEO-focused fact-checking and evidence collection assistant for written content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content teams, marketers, and analysts use this skill to extract important factual claims, verify them against reliable sources, and revise written content so it is better supported for AI citation and decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage web verification for a wide range of factual content, including confidential drafts. <br>
Mitigation: Avoid using it on confidential drafts unless external lookup of related facts is acceptable. <br>
Risk: Unsupported rankings, outdated numbers, or weak source evidence can still lead to misleading content if accepted without review. <br>
Mitigation: Review the generated claim statuses, source quality, revised wording, risks, and open questions before publishing. <br>


## Reference(s): <br>
- [Geo Fact Checker release page](https://clawhub.ai/geoly-geo/geo-fact-checker) <br>
- [Claim Types for GEO Fact Checking](references/claim-types.md) <br>
- [Fact-Checking Patterns for GEO Content](references/fact-checking-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code, shell commands] <br>
**Output Format:** [Markdown reports with claim tables, evidence summaries, revised wording, and optional helper-script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify assumptions, claim types, verification status, primary sources, risks, and open questions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
