## Description: <br>
Agentsec audits AI agent skills for security vulnerabilities against the OWASP Agentic Skills Top 10 and can generate text, JSON, SARIF, or HTML audit reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markeljan](https://clawhub.ai/user/markeljan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and release engineers use Agentsec to scan installed agent skills before running them, check OWASP Agentic Skills Top 10 coverage, gate CI/CD, and produce audit reports for stakeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default scan scope may read more local skill files than expected. <br>
Mitigation: Review the directories Agentsec will scan and prefer a path-scoped command such as scanning a specific skill directory in sensitive environments. <br>


## Reference(s): <br>
- [Agentsec homepage](https://agentsec.sh) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [ClawHub skill page](https://clawhub.ai/markeljan/skills/agentsec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; Agentsec itself can emit text, JSON, SARIF, or HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may prompt scans over local skill directories; path-scoped scans are available for narrower review.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
