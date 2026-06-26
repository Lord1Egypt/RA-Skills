## Description: <br>
Implements a nightly OpenClaw dream cycle that audits memory, trims bloated workspace files, and generates a morning brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to set up scheduled memory audits, workspace cleanup checks, and morning summaries for ongoing agent maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Silent scheduled memory or workspace cleanup could affect important local context without enough review controls. <br>
Mitigation: Run the audit and brief scripts manually first, then enable scheduled runs only after adding path limits, change logs, backups, approval for edits, and a clear disable path. <br>
Risk: Briefs and audit reports may summarize stale, incomplete, or overly broad local memory files. <br>
Mitigation: Review generated summaries before acting on them and keep the workspace and memory directories scoped to the intended OpenClaw files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell script output and cron-style configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit summaries and morning briefs based on local OpenClaw workspace and memory files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
