## Description: <br>
Audit AI agent skills for security vulnerabilities, including scans against the OWASP Agentic Skills Top 10, pre-run safety checks, CI/CD gating, and stakeholder audit reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markeljan](https://clawhub.ai/user/markeljan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and platform teams use this skill to audit installed agent skills, check OWASP Agentic Skills Top 10 coverage, and generate text, JSON, SARIF, or HTML audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default command scans known agent skill directories in home and nearby project paths, which may be broader than intended. <br>
Mitigation: Use a scoped command such as `npx agentsec scan --path ./skills` when auditing a specific directory. <br>
Risk: Generated reports may reveal names or metadata of installed skills. <br>
Mitigation: Review reports before sharing them outside the intended audience. <br>


## Reference(s): <br>
- [Agentsec homepage](https://agentsec.sh) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [ClawHub skill page](https://clawhub.ai/markeljan/agentsec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to text, JSON, SARIF, and HTML report formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May advise scoped scans, policy presets, output paths, and report generation commands.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
