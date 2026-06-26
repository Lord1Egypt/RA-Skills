## Description: <br>
Automates CI/CD pipeline creation and monitoring for GitHub Actions, GitLab CI, and Jenkins, including build, test, deploy workflow generation and pipeline status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to generate CI/CD workflow configurations, create repeatable build/test/deploy stages, and check recent pipeline status across supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI/CD files can change build, deployment, or publishing behavior in real environments. <br>
Mitigation: Review generated workflow files before committing them, especially deployment and production-branch behavior. <br>
Risk: Pipeline status checks may use repository or CI platform tokens. <br>
Mitigation: Use least-privilege tokens, avoid embedding credentials in generated files, and prefer a virtual environment with pinned dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/ci-cd-pipeline-toolkit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus generated CI/CD configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workflow files and may make pipeline status API calls when the user supplies repository, project, or token inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
