## Description: <br>
AI self-evolution engine based on the SEA (Sense-Evolve-Act) loop for self-assessment, learning, evolution workflows, collaborative learning, and safety controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to assess an agent's capabilities, select learning paths, and plan supervised self-improvement workflows. It is intended for agents that run Node.js scripts and need guidance for learning, assessment, and evolution routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage changes to persistent memory, instruction, or knowledge files. <br>
Mitigation: Require review of exact diffs before allowing changes to MEMORY.md, AGENTS.md, SOUL.md, knowledge files, or learning logs. <br>
Risk: The skill may encourage installing additional skills without concrete limits. <br>
Mitigation: Approve each new skill installation only after reviewing its source, provenance, and security scan result. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dagangtj/ai-evolution-engine-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; script output is diagnostic guidance and should be reviewed before applying persistent agent changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
