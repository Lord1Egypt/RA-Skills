## Description: <br>
Local DevOps/autonomy skill for OpenClaw (safe evolution loop with guardrails). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Delkoman88](https://clawhub.ai/user/Delkoman88) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Evolve to run a local OpenClaw skill evolution loop that snapshots status, generates and tests candidate skills, promotes reviewed candidates, and supports rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter active OpenClaw skills through an unspecified local controller script. <br>
Mitigation: Install only in an isolated development OpenClaw environment after inspecting the exact evolvectl.sh that will run. <br>
Risk: An untrusted EVOLVECTL path could delegate the workflow to unexpected local code. <br>
Mitigation: Do not point EVOLVECTL at an untrusted path. <br>
Risk: Generated candidate skills may introduce incorrect behavior or weaken guardrails if promoted without review. <br>
Mitigation: Require manual review and scanning before any generated skill is promoted into active use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Delkoman88/evolve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates operation to a local evolvectl.sh controller, with EVOLVECTL available to select the controller path.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
