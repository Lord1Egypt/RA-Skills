## Description: <br>
Coding style memory that adapts to your preferences, conventions, and patterns for consistent coding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chayjan](https://clawhub.ai/user/chayjan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to remember explicitly confirmed coding style preferences and apply them to future code output while keeping the preference store local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save coding preferences the user no longer wants applied. <br>
Mitigation: Confirm each preference before it is saved and periodically review ~/coding/memory.md for stale entries. <br>
Risk: A local coding-preference memory can affect future code output in ways that are no longer desired. <br>
Mitigation: Use the skill's query and forget workflows to inspect or remove stored preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chayjan/coding-1-0-3) <br>
- [Publisher profile](https://clawhub.ai/user/chayjan) <br>
- [Skill homepage](https://clawic.com/skills/coding) <br>
- [Preference criteria](criteria.md) <br>
- [Code preference dimensions](dimensions.md) <br>
- [Memory templates](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with concise text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local files under ~/coding/ only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter); release metadata version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
