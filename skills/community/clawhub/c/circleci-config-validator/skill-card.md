## Description: <br>
Validate .circleci/config.yml files for syntax, structure, security, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate, audit, and inspect CircleCI pipeline configuration files before committing or running CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads whichever CircleCI configuration file path the user provides and may report locations that look like hardcoded secrets. <br>
Mitigation: Run it only on intended configuration files and review reported secret locations before sharing output. <br>
Risk: Findings are static lint results and may be incomplete or context-dependent. <br>
Mitigation: Use the results as review guidance alongside CircleCI's own validation and normal CI/CD review practices. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI output in text, JSON, or summary format, plus Markdown usage guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-specified CircleCI YAML file and reports validation findings without modifying files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
