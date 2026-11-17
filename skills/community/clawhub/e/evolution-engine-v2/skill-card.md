## Description: <br>
进化引擎 helps an AI agent learn from explicit corrections and self-reflection by maintaining layered local Markdown memory, promotion rules, and evolution metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an AI coding or productivity agent reduce repeated mistakes, preserve confirmed preferences, and measure learning across sessions. It is suited for long-running projects where explicit corrections and reflections should become reusable guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps persistent local memory about corrections, preferences, and project patterns under ~/evolution-engine/. <br>
Mitigation: Install it only when that persistence is desired, review stored content periodically, and require explicit confirmation before the first write. <br>
Risk: The artifact declares command execution access even though its own dependency notes say command-line execution is not required. <br>
Mitigation: Remove or disable exec access for normal use, or require explicit approval before any command execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/evolution-engine-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance and local Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads persistent local memory under ~/evolution-engine/ when the hosting agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
