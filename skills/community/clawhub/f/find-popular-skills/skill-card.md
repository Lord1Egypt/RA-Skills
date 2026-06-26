## Description: <br>
Find Popular Skills helps agents discover, evaluate, install, and publish agent skills from skills.sh and ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant agent skills, compare quality signals, and receive install or publish guidance for skills.sh and ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install and publish workflows can change the agent environment or publish content without enough user confirmation. <br>
Mitigation: Require explicit user approval and show the selected skill, source, and risks before running install or publish commands. <br>
Risk: Authentication tokens may be exposed if passed directly on the command line. <br>
Mitigation: Use safer authenticated sessions or environment-based token handling where supported, and avoid echoing or storing tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/find-popular-skills) <br>
- [skills.sh](https://skills.sh) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should include the selected skill, source, quality signals, and risks before install or publish commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
