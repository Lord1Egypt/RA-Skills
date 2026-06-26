## Description: <br>
Manages cooking-recipe recipes and grocery lists through authenticated commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demonkit](https://clawhub.ai/user/demonkit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate with cooking-recipe, add, list, search, show, and delete stored recipes, and create or update grocery lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends authentication and recipe or grocery-list API traffic to a configured backend, with a shared backend available only when explicitly enabled. <br>
Mitigation: Use a trusted or self-hosted backend when possible, disclose shared backend usage when enabled, and avoid describing the skill as local-only. <br>
Risk: OAuth credentials and account login are required for normal use. <br>
Mitigation: Provide exact setup steps for required OAuth configuration and never reveal secrets or tokens in agent output. <br>
Risk: Commands can create and delete stored recipe and grocery-list data. <br>
Mitigation: State the affected recipe or list clearly when performing persistent changes, especially deletion. <br>


## Reference(s): <br>
- [Cooking Recipe ClawHub page](https://clawhub.ai/demonkit/cooking-recipe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and recipe or grocery-list responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication and configuration next steps; must not expose secrets or tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
