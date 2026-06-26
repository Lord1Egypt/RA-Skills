## Description: <br>
Invokes Claude Code through a Node.js wrapper to delegate software design, development, testing, optimization, refactoring, and related coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[the-invulnus](https://clawhub.ai/user/the-invulnus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run Claude Code from a project directory for coding, debugging, testing, refactoring, and design discussion tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates coding tasks to Claude Code with permission to read, edit, write files, run shell commands, and use project or user Claude settings. <br>
Mitigation: Use it only in controlled project directories under version control and review changes before accepting them. <br>
Risk: External Claude Code processing may receive repository content, prompts, or other project data. <br>
Mitigation: Avoid sensitive repositories unless that processing is explicitly allowed for the project. <br>
Risk: The optional log file may contain code, prompts, or confidential output. <br>
Mitigation: Treat log files as sensitive artifacts and store or delete them according to the project's data-handling requirements. <br>
Risk: Resuming an unrelated Claude Code session can mix task context across workstreams. <br>
Mitigation: Start fresh sessions for unrelated work and use resume IDs only for the same task thread. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Plain text or Markdown with optional code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a Claude Code session ID for resume workflows and optional log-file output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
