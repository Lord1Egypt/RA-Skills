## Description: <br>
Generate GitHub Actions workflows from plain English. Use when setting up CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[branexp](https://clawhub.ai/user/branexp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to generate GitHub Actions workflow YAML from plain English for CI setup, pull request checks, scheduled jobs, and deployment automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow descriptions may be sent to OpenAI during generation. <br>
Mitigation: Do not include tokens, credentials, private infrastructure details, or sensitive deployment logic in prompts. <br>
Risk: Generated GitHub Actions workflows can run with repository permissions and access configured secrets. <br>
Mitigation: Print or write the YAML to a new file first, then review it like code before committing or installing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/branexp/gh-action-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Files] <br>
**Output Format:** [GitHub Actions workflow YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print generated YAML or write it to a workflow file when output or install options are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
