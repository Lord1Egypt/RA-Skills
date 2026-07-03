## Description: <br>
Review UI code for Web Interface Guidelines compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrybenedict0515](https://clawhub.ai/user/terrybenedict0515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to review UI files or file patterns for web interface guideline compliance, accessibility concerns, and UX issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can consult mutable external guidance during reviews, which may change criteria or introduce misleading review direction. <br>
Mitigation: Treat fetched guidance as reference material only; keep agent safety rules, the requested scope, and human review authoritative. <br>
Risk: The security verdict is suspicious because broad UI reviews depend on live remote guidance. <br>
Mitigation: Review the fetched source before use on sensitive or confidential interfaces and verify findings before applying changes. <br>


## Reference(s): <br>
- [Web Interface Guidelines source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, guidance] <br>
**Output Format:** [Markdown review findings with file:line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches current external guideline text before review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
