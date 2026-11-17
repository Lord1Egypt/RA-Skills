## Description: <br>
A Markdown-based agent memory workflow for recording explicit user corrections, recalling recent lessons, and limiting preference pollution through basic anti-contamination rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to help an AI coding assistant remember explicit corrections, avoid repeating mistakes, and keep lightweight local correction and reflection notes. It is intended for single-agent personal workflows rather than multi-project memory isolation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious because the skill declares command-execution capability that is not needed for its stated Markdown-based memory workflow. <br>
Mitigation: Review the skill before installing and grant only the read/write access needed for local Markdown memory files. <br>
Risk: Saved correction and reflection memory may be reused later with weak project scoping. <br>
Mitigation: Inspect and clear ./evolution-engine/memory.md and corrections.md when switching projects or handling sensitive information. <br>
Risk: The free edition does not provide namespace isolation, which can allow preferences or lessons from one project to affect another. <br>
Mitigation: Use separate workspace directories or manually separate memory files for different projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/evolution-engine-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions and local Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local ./evolution-engine/memory.md and corrections.md files when the hosting agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
