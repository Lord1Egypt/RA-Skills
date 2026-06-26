## Description: <br>
Installs a curated AOI/Aoineco starter pack of ClawHub skills for security, stability, memory, and ops through the ClawHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to install a beginner-friendly minimal, core, or full bundle of AOI/Aoineco ClawHub skills from a fixed list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bulk-installs multiple ClawHub skills from a fixed list. <br>
Mitigation: Review the minimal, core, or full skill list before running the script, and choose the smallest bundle that fits the user's needs. <br>
Risk: Install commands run under the currently authenticated ClawHub session. <br>
Mitigation: Confirm `clawhub whoami` shows the intended account before running the installer. <br>


## Reference(s): <br>
- [Skill List](references/skill_list.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installer scripts execute ClawHub CLI install commands for minimal, core, or full bundle modes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
