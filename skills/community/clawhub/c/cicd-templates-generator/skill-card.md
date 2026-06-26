## Description: <br>
Generates CI/CD workflow templates for GitHub Actions, GitLab CI, and Jenkins based on selected language, framework, test, deployment, and release options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate starter CI/CD workflow files for Python, JavaScript, and Go projects. It is intended to speed up workflow creation while leaving the generated pipeline available for review before commit or execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow files can introduce deployment triggers, publish jobs, third-party actions, shell installation steps, or secret references that affect a repository after commit. <br>
Mitigation: Use print-only or review mode first, then inspect the generated workflow before committing or enabling it. <br>
Risk: Generated templates may include placeholder secret names or deployment assumptions that do not match the target repository or organization policy. <br>
Mitigation: Replace placeholders with approved secret names and remove unused deploy or publish stages before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/cicd-templates-generator) <br>
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Design document](artifact/DESIGN-cicd-templates-generator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated CI/CD configuration files such as YAML or Jenkinsfile text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print generated workflow content or write files to the selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
