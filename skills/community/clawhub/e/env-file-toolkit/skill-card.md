## Description: <br>
Manage .env files with validation, diffing, template generation, merge, key listing, and missing-key checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnywang2001](https://clawhub.ai/user/johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and manage local environment variable files, including comparing environment files, generating examples, merging values, and checking that required keys are present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diff output, merge output, list-keys --with-values, and template --keep-values can expose secrets from .env files. <br>
Mitigation: Treat generated output and files as sensitive; avoid sharing them in logs, screenshots, tickets, or commits. <br>
Risk: The utility reads and writes local environment files, including generated .env.example and merged .env files. <br>
Mitigation: Review file paths and output targets before running commands, and keep generated files out of version control when they contain real values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnnywang2001/env-file-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include environment variable values when diffing, merging, listing with values, or keeping values in generated templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
