## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachary2024](https://clawhub.ai/user/zachary2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable skills, compare skill quality signals, and generate install commands when a task may be served by an existing skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer ordinary requests toward globally installing third-party skills while skipping installer confirmations. <br>
Mitigation: Verify the exact source and publisher, inspect the selected skill or repository, and remove `-y` from installation commands so the installer confirmation prompt remains visible. <br>
Risk: Search results and popularity signals can be mistaken for approval or safety. <br>
Mitigation: Treat results as candidates only; review install counts, source reputation, repository evidence, and the skill contents before recommending or installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zachary2024/find-skills-vercel) <br>
- [Skills directory](https://skills.sh/) <br>
- [Example referenced skill page](https://skills.sh/vercel-labs/agent-skills/react-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend global skill installation commands; users should verify the source and publisher before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
