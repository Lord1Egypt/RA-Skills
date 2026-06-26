## Description: <br>
Analyze repo, detect stack, trace changes to user-facing entry points, generate E2E YAML test plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect repository changes and generate an executable end-to-end YAML test plan focused on user-facing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated E2E plans may include steps that touch real services, databases, credentials, or production-like environments. <br>
Mitigation: Review the generated YAML before running it with any execution skill and prefer non-production credentials and environments. <br>


## Reference(s): <br>
- [Stack Discovery Reference](references/stack-discovery.md) <br>
- [Test Case Generation Reference](references/test-case-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [YAML test plan plus Markdown summary with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces docs/testing/test-plan.yaml and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
