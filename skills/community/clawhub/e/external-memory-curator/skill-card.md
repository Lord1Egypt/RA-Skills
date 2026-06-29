## Description: <br>
Organize external project memory with status files and safe promotion rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanbastias](https://clawhub.ai/user/juanbastias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain file-based project memory, resume work from status files, compact stale notes, and decide which facts should be promoted into durable memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can influence future agent behavior if inaccurate, stale, or over-promoted details are saved. <br>
Mitigation: Review memory edits and promote only durable, verified project state or preferences. <br>
Risk: Memory files may accidentally capture secrets or sensitive personal data. <br>
Mitigation: Avoid storing secrets or sensitive personal data, and review changes to MEMORY.md, TOOLS.md, AGENTS.md, and project status files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juanbastias/external-memory-curator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown notes and concise text summaries, sometimes with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local memory files such as MEMORY.md, TOOLS.md, AGENTS.md, and projects/<project>/status.md when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
