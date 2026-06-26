## Description: <br>
Queries DataEase organizations, switches organization context, lists dashboards or data screens, and exports selected resources as screenshots or PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwei-fit2cloud](https://clawhub.ai/user/xuwei-fit2cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to inspect DataEase organization access, find dashboards or data screens, and export selected resources for reporting or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live DataEase tokens and dashboard content that may be sensitive. <br>
Mitigation: Use a least-privileged or short-lived DataEase account or token, keep .env files private, and treat exported screenshots and PDFs as confidential. <br>
Risk: Command output or transcripts may expose live tokens, resource identifiers, or confidential dashboard details. <br>
Mitigation: Review command output before sharing transcripts, avoid shared terminals and logs, and redact sensitive values. <br>
Risk: The security evidence marks the release as suspicious because credential and export handling need user review. <br>
Mitigation: Install only when the DataEase instance and execution machine are trusted, and review the skill behavior before deployment. <br>


## Reference(s): <br>
- [DataEase ClawHub release page](https://clawhub.ai/xuwei-fit2cloud/dataease) <br>
- [DataEase API reference](references/api.md) <br>
- [Resource alias mappings](references/resource_aliases.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or JSON-style status text with generated JPEG/PDF files or absolute saved-file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include matched organization or resource IDs, export parameters, candidate lists for ambiguous matches, and local output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
