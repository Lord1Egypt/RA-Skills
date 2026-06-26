## Description: <br>
Manage a Bring! shopping list by adding, removing, completing, and listing grocery items through a Bring! account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zahlmann](https://clawhub.ai/user/zahlmann) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to manage a personal or household Bring! shopping list from natural-language grocery requests. It is suited for adding, removing, completing, and checking items on the account's default Bring! list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs Bring account credentials and can read and update the user's default Bring shopping list. <br>
Mitigation: Use secure environment-variable storage and install only when the agent should have access to that account and list. <br>
Risk: Ambiguous grocery requests could add, remove, or complete the wrong item. <br>
Mitigation: Confirm unclear add, remove, or complete requests before running the command. <br>
Risk: Dependencies are declared without pinned versions. <br>
Mitigation: Pin and review dependencies before use in stricter or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zahlmann/bring-shopping-list) <br>
- [Bring!](https://www.getbring.com/) <br>
- [bring-api Python package](https://github.com/miaucl/bring-api) <br>
- [uv package manager](https://docs.astral.sh/uv/) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Natural-language confirmations with CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRING_EMAIL and BRING_PASSWORD; actions apply to the first default Bring! shopping list.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
