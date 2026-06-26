## Description: <br>
Track expenses via natural language, get spending summaries, set budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log expenses in natural language, categorize spending, compare spending against budgets, and request summaries or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense descriptions, budgets, and stored records are processed through SkillBoss/HeyBoss services. <br>
Mitigation: Avoid entering highly sensitive financial details until the provider's privacy, retention, deletion, and export practices are understood. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Protect the key as a sensitive credential, scope it where possible, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-expense-tracker-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text responses with structured JSON expense records for logged expenses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SkillBoss API key and stores expense records through SkillBoss KV storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
