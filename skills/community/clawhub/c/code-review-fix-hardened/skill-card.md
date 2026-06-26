## Description: <br>
Automated code review with fix suggestions and in-place code repairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan code for bugs, security issues, style problems, and performance concerns, then optionally apply simple in-place fixes. It also supports an explain mode for learning-oriented review output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal review commands can trigger third-party SkillPay billing with a local user identifier and a hardcoded billing key. <br>
Mitigation: Review or replace the billing key before installation, set an explicit SKILLPAY_USER_ID when billing is used, and install only where SkillPay billing is acceptable. <br>
Risk: The --fix mode can modify the reviewed source file in place. <br>
Mitigation: Run --fix only in a version-controlled worktree and inspect the resulting diff before committing or deploying changes. <br>
Risk: The skill keeps local usage state in .code-review-fix-state.json. <br>
Mitigation: Review the state file behavior and avoid sharing the file if local user identifiers or billing history should remain private. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/code-review-fix-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai) <br>
- [SkillPay billing service](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal-oriented text and Markdown-style review output, with optional file modifications when --fix is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write fixed code back to the reviewed file and stores local usage state in .code-review-fix-state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
