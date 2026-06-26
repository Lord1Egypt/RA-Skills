## Description: <br>
Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. Requires the blackbox CLI and a Blackbox AI API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgungPrabowo123](https://clawhub.ai/user/AgungPrabowo123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding, review, refactoring, and project automation tasks to the Blackbox AI CLI from an agent terminal. It is suited for one-shot tasks, interactive or background sessions, checkpoint resume workflows, and parallel coding-agent runs when the user has configured the required CLI and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blackbox CLI may send relevant project context to external AI services. <br>
Mitigation: Use the skill only for projects where that data sharing is acceptable, and avoid placing secrets in prompts or files exposed to the agent. <br>
Risk: Delegated coding-agent sessions can modify files in the selected working directory. <br>
Mitigation: Run in a scoped project directory, keep version control enabled, review diffs after each run, and avoid `--yolo` on important repositories. <br>
Risk: Long-running or multi-model sessions can consume credits and continue in the background. <br>
Mitigation: Monitor background sessions and credit usage, and stop sessions that are no longer needed. <br>


## Reference(s): <br>
- [Blackbox AI](https://www.blackbox.ai/) <br>
- [Blackbox AI Dashboard](https://app.blackbox.ai/dashboard) <br>
- [Blackbox CLI Repository](https://github.com/blackboxaicode/cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/AgungPrabowo123/blackbox-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate interactive or background Blackbox CLI sessions that modify files in the selected working directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
