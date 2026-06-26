## Description: <br>
Autonomous daily self-introspection and self-improvement for OpenClaw agents that reviews conversation logs, identifies mistakes and improvement opportunities, and upgrades core rules automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to schedule daily and weekly agent self-review, collect workspace learning records, identify recurring mistakes, and promote mature lessons into persistent agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled runs can inspect conversation history and workspace learning files. <br>
Mitigation: Install only in workspaces where that review is intended, and periodically review or delete .daily-introspection records. <br>
Risk: Weekly promotion can alter persistent agent guidance before user review. <br>
Mitigation: Disable automatic promotion or require proposed diffs and human approval before writes to AGENTS.md, MEMORY.md, TOOLS.md, or .learnings files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raydoomed/daily-introspection) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown records and reports with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces daily introspection records, weekly evolution reports, and suggested or promoted rule updates.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
