## Description: <br>
Run long-lived AI coding agents in persistent tmux sessions with Ralph retry loops and completion hooks for multi-step coding tasks and PRD-based workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luke-deltadesk](https://clawhub.ai/user/luke-deltadesk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to run coding agents through persistent tmux-based retry loops for long-lived programming tasks, multi-step feature work, and PRD checklist execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-running coding-agent loops can make unattended repository changes or continue using configured agent credentials. <br>
Mitigation: Run loops in a branch or worktree, monitor active tmux sessions, and kill sessions when finished. <br>
Risk: Agent output may mark tasks complete despite incomplete or incorrect code changes. <br>
Mitigation: Review git diff, logs, and test results before accepting or merging changes. <br>
Risk: High-autonomy or skip-test workflows can increase risk in sensitive repositories. <br>
Mitigation: Avoid full-auto or skip-test modes for sensitive repositories and confirm trust in ralphy-cli and coding-agent credentials before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luke-deltadesk/coding-agent-loops) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tmux session commands, Ralph loop usage patterns, completion hooks, PRD checklist guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
