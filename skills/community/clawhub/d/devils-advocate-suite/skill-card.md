## Description: <br>
Executes structured adversarial thinking to stress-test high-stakes decisions, identify systemic risks, and prevent groupthink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midnightstudioai](https://clawhub.ai/user/midnightstudioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Decision makers, product leaders, strategy reviewers, and developers use this skill to challenge assumptions, run pre-mortems, stress-test PR/FAQ narratives, apply dialectical inquiry, and resolve business trade-offs with TRIZ-style prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during broad high-stakes planning discussions because its trigger language is intentionally proactive. <br>
Mitigation: Use narrower trigger wording or explicit invocation when users want adversarial review only on request. <br>
Risk: Adversarial critiques can over-weight negative scenarios if treated as final decision guidance. <br>
Mitigation: Use the output as structured decision-review input and verify assumptions, evidence, and mitigations with accountable stakeholders. <br>
Risk: The local helper scripts process user-supplied failure scenarios and contradiction terms. <br>
Mitigation: Run the helpers locally with approved inputs and avoid including sensitive details unless the execution environment is appropriate. <br>


## Reference(s): <br>
- [Technical Summary: Adversarial Methodologies](references/methodology_summary.md) <br>
- [ClawHub release page](https://clawhub.ai/midnightstudioai/devils-advocate-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown decision-review reports with optional local Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk matrices, adversarial questions, assumption critiques, intervention plans, and TRIZ principle recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
