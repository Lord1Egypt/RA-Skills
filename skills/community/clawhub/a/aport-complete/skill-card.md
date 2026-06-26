## Description: <br>
Verify a completed task against your APort passport's deliverable contract before marking it done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a completion gate before closing work, opening pull requests, or handing off tasks. It guides the agent to collect required evidence, submit APort deliverable-policy verification, and respond to allow or deny decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries, evidence, or output_content can include secrets, credentials, PII, private source content, or confidential ticket details that would be sent to APort. <br>
Mitigation: Review and redact sensitive material before submitting verification requests, and send only the minimum evidence needed to satisfy the passport contract. <br>
Risk: The optional npx setup path can execute package code in the local environment. <br>
Mitigation: Review the package and installation command before running it, especially in production or privileged agent environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/uchibeke/aport-complete) <br>
- [APort](https://aport.id) <br>
- [APort agent skill](https://aport.id/skill) <br>
- [APort API documentation](https://aport.io/api/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HTTP access to APort verification endpoints and an APORT_AGENT_ID value from an APort passport.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
