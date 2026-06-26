## Description: <br>
Manage Bring! shopping lists via the unofficial bring-shopping Node.js library using email/password login. Use for listing lists, reading items, adding/removing items, and checking/unchecking items when API-style access is acceptable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutzenfriend](https://clawhub.ai/user/cutzenfriend) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and update Bring! shopping lists through a CLI-backed workflow when API-style access is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Bring! account credentials to access shopping lists. <br>
Mitigation: Store BRING_EMAIL and BRING_PASSWORD in environment configuration and install only when sharing those credentials with the skill is acceptable. <br>
Risk: Add, remove, check, and uncheck commands can change a real Bring! shopping list. <br>
Mitigation: Review write requests before execution and specify the intended target list for each write action. <br>
Risk: The skill depends on the third-party bring-shopping npm package. <br>
Mitigation: Review or pin the dependency before using the skill with a real Bring! account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cutzenfriend/bring-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output is JSON for list and item reads and status text for write actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRING_EMAIL and BRING_PASSWORD environment variables and may modify the selected Bring! shopping list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
