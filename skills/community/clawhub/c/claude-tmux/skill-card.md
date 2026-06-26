## Description: <br>
Manage Claude Code instances living inside tmux sessions. Users usually create separate tmux sessions for separate projects. Use this skill when you need to read the latest Claude Code response in a particular tmux session / project, send it a prompt and get the response, or run /compact directly via tmux (no extra scripts required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulrahul](https://clawhub.ai/user/paulrahul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, prompt, compact, and debug Claude Code sessions running in tmux. It provides a repeatable command checklist for locating the right pane, reading recent scrollback, sending prompts, and reporting the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from and type into live terminal panes. <br>
Mitigation: Verify the tmux session and pane target before sending input, and avoid shared or production tmux sessions. <br>
Risk: Captured tmux scrollback may contain sensitive information. <br>
Mitigation: Treat captured pane output as sensitive and only share the minimum lines needed for the user's request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulrahul/claude-tmux) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline tmux shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include captured terminal scrollback and verbatim Claude Code replies from the selected tmux pane.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
