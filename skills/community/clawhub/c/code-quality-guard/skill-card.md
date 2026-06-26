## Description: <br>
Professional pre-deployment code review and quality enforcement. Ensures imports are valid, tags are closed, and logic follows best practices before announcing a build is live. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill before builds or deployment to review imports, JSX or HTML tag balance, environment expectations, logs, and potential code-quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository, log, or configuration review can expose unrelated host details or unredacted production data. <br>
Mitigation: Scope use to the intended project and avoid supplying unrelated environment dumps or unredacted production logs. <br>
Risk: Generated review guidance can be incomplete or unsuitable for a specific deployment. <br>
Mitigation: Review generated findings before sharing them or using them as release-blocking advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/code-quality-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown review notes with checklists and optional inline shell commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review generated findings before sharing them or acting on deployment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
