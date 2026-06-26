## Description: <br>
Helps users discover and install agent skills when they are looking for functionality that might exist as an installable skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to identify relevant installable skills, compare basic quality signals, present options, and provide CLI install commands when users want added capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to install third-party skills globally or skip confirmation. <br>
Mitigation: Inspect recommended skill sources first and run installs only after clear user confirmation; avoid global or auto-confirm flags unless intentionally requested. <br>
Risk: Recommendations based only on search results can surface low-quality or untrusted skills. <br>
Mitigation: Check install counts, source reputation, and repository signals before recommending or installing a skill. <br>


## Reference(s): <br>
- [ClawHub Skill Lookup release page](https://clawhub.ai/drumrobot/discover-skill) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested npx skills commands, source reputation checks, install counts, and skill directory links.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
