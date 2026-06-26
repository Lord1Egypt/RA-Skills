## Description: <br>
Helps users discover and install agent skills when they ask for specialized functionality or ways to extend an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KylinJackson](https://clawhub.ai/user/KylinJackson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable skills, present marketplace options, and optionally install selected skills with the Skills CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer broad requests toward external third-party skill recommendations and global installation commands. <br>
Mitigation: Use it only when external skill recommendations are intended, review the package source and contents before installation, and prefer non-global installation unless user-level persistence is desired. <br>
Risk: The documented install example uses a confirmation-skipping flag. <br>
Mitigation: Avoid confirmation-skipping flags unless the exact package and install command have already been reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/KylinJackson/find-skill-v2) <br>
- [Skills marketplace](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include marketplace links and install commands; users should review package sources before installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
