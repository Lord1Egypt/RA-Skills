## Description: <br>
Lint docker-compose.yml files for security, best practices, and port conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Docker Compose files for security issues, operational best practices, service summaries, and host port conflicts before running or shipping compose-based stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security adjudication was clean but noted that direct artifact text was unavailable for a full coherence review. <br>
Mitigation: Review the packaged SKILL.md, STATUS.md, and docker-compose-linter.py before installation or CI use. <br>
Risk: The skill can be used to gate CI through strict mode, so false positives or parser limitations could interrupt deployment workflows. <br>
Mitigation: Run it first in advisory mode, tune --ignore and --min-severity for the repository, and require human review before enforcing strict failures. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/charlie-morrison/docker-compose-linter) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line lint, service, port, and audit reports in text, JSON, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports strict CI exits, minimum severity filtering, and repeated rule ignores.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
