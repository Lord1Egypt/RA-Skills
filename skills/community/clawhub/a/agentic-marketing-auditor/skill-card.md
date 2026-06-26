## Description: <br>
Audits repositories for marketing readiness by checking README and documentation signals that help AI products be discovered by LLMs and generative search engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and marketing teams use this skill to run a lightweight local audit of repository documentation for AI discoverability signals such as llms.txt and agent-friendly README summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit uses lightweight documentation heuristics and may identify discoverability gaps without proving search ranking impact. <br>
Mitigation: Treat findings as review prompts and validate documentation changes with product, marketing, and legal stakeholders before publishing. <br>
Risk: The skill reads README.md from the repository path supplied by the user. <br>
Mitigation: Run it only against repositories you intentionally choose and review terminal output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/agentic-marketing-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/tmstudio667-commits) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text CLI audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads the chosen local repository's README.md and checks for llms.txt; prints findings and recommendations without changing files or sending data out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
