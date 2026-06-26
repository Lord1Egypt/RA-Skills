## Description: <br>
Validates and documents the ClawHub owner migration process by publishing, moving, inspecting, and deleting a disposable skill during PR review. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized ClawHub maintainers and reviewers use this internal validation skill to test owner migration behavior with a disposable skill record. It is intended for controlled PR review, not for general installation or end-user workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to publish, migrate ownership of, and delete skills using sensitive publisher authority. <br>
Mitigation: Use only in a controlled internal validation environment with an authorized account, explicit human approval, and a disposable test skill. <br>
Risk: A migration or cleanup mistake could affect a real skill record or publisher ownership metadata. <br>
Mitigation: Confirm the target skill is disposable before execution and keep a cleanup or rollback plan ready. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-debug-1778256957) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown instructions with command-oriented workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized publisher access and a disposable test skill.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
