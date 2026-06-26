## Description: <br>
Helps agents discover installable skills for a user's requested capability and guide search, selection, and optional installation with the Skills CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlylingo9817-sys](https://clawhub.ai/user/onlylingo9817-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable skills, compare presented options, and decide whether to install a skill for a recurring workflow or specialized task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend installing third-party skills and includes examples that skip confirmation prompts. <br>
Mitigation: Review the exact package source and publisher before installation, avoid skipping confirmations unless trusted, and prefer local or scoped installation for untrusted skills. <br>
Risk: Installed skills can change agent behavior or introduce misleading guidance into future workflows. <br>
Mitigation: Inspect the skill contents and available scan results before deployment, then keep only skills that are relevant to the intended task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onlylingo9817-sys/find-skills-bak) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill names, install commands, search guidance, and links to relevant skill listings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
