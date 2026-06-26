## Description: <br>
After file changes, this skill guides an agent to run two consecutive verification checks, such as tests, builds, runtime checks, or documentation/configuration checks, before considering the task complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BelugaRex](https://clawhub.ai/user/BelugaRex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to add a repeatable verification routine after code, documentation, configuration, or resource file edits. It is intended to reduce accidental regressions by requiring two passing checks before the agent reports completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands may run project code or start processes with side effects in unfamiliar repositories. <br>
Mitigation: Require confirmation before commands that start services, touch production data, use the network, take a long time, or have unclear side effects. <br>
Risk: A repeated runtime, build, or documentation check may not prove the edited logic is correct. <br>
Mitigation: Prefer existing test, build, lint, or documentation validation commands, and disclose limitations when only a basic runtime check is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BelugaRex/double-check) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline verification command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to report verification outcomes and rerun the same selected check after corrections.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
