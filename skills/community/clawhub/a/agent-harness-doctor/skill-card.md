## Description: <br>
Automated audit and fix for OpenClaw agent harnesses. Scans your setup, scores on 8 dimensions (Session Bridge, Startup Sequence, Smoke Test, Atomic Checkpoint, Output Verification, State Format, Multi-Agent Protocol, Fallback Plan), generates a prioritized improvement plan, and can auto-apply P0 fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess and harden OpenClaw agent harnesses by scoring startup, state, verification, checkpointing, and fallback practices. It can produce a diagnostic report and optionally apply prioritized harness fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A diagnostic workflow can still make persistent changes to agent instruction or state files when fix application is requested. <br>
Mitigation: Use diagnostic mode with an empty fix_apply list for report-only runs, and review or back up AGENTS.md and agent-progress.json before applying fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neroagent/agent-harness-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON diagnostic results and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace harness files when fix application is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
