## Description: <br>
Generates GitHub Actions CI/CD workflows tailored to a project's detected stack, deployment target, and workflow preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to set up GitHub Actions CI/CD by detecting project stack details, asking for deployment preferences, and producing workflow files and secret checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow changes can affect deployment behavior, production environments, SSH commands, and GitHub Secrets usage. <br>
Mitigation: Review all generated .github/workflows changes before committing, especially deploy jobs, SSH commands, production environments, and configured GitHub Secrets. <br>
Risk: The skill requires repository access and is intended to draft or edit GitHub Actions workflows. <br>
Mitigation: Install it only when an agent should draft or edit CI/CD workflows, and grant only the repository access needed for that task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML workflow definitions, shell command snippets, and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository-specific GitHub Actions workflow content and deploy guidance based on detected project files and user choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
