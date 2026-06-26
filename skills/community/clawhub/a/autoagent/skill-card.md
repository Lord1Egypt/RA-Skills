## Description: <br>
Automatically improve agent guidance through iterative testing and scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PeterPCW](https://clawhub.ai/user/PeterPCW) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Autoagent to optimize prompts, AGENTS.md entries, and skill definitions through a recurring test-and-score loop. The skill helps define success criteria, create a sandbox, run iterations, and keep a score history for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recurring optimization loop can edit sandbox guidance files and continue running after setup. <br>
Mitigation: Use a fresh non-sensitive sandbox path, monitor scores.md, and stop the cron job when optimization is finished. <br>
Risk: Copied scripts or external tools may expose sensitive or proprietary content during analysis. <br>
Mitigation: Review any scripts before allowing analysis and avoid including secrets or proprietary code unless necessary. <br>
Risk: Absolute sandbox paths could point into important project or system folders. <br>
Mitigation: Prefer a dedicated sandbox directory and confirm the resolved path before starting the loop. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Autoagent ClawHub Page](https://clawhub.ai/PeterPCW/autoagent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance, setup questions, sandbox file templates, and OpenClaw cron instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates sandbox guidance files, fixtures, scoring criteria, score history, and optional script-analysis notes.] <br>

## Skill Version(s): <br>
0.8.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
