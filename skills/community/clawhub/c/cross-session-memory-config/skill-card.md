## Description: <br>
Configures OpenClaw cross-session memory rules by adding shared long-term memory guidance to SOUL.md and AGENTS.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardcoder849](https://clawhub.ai/user/richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill when they intentionally want group chat and private chat sessions to share durable memory through global memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared memory rules can cause group chat and private chat context, including sensitive decisions or personal data, to be written to global memory files. <br>
Mitigation: Install only where cross-session sharing is intended, review the inserted rules first, and avoid use where private or group memories must remain separated. <br>
Risk: The setup script persistently changes core OpenClaw behavior by creating or appending rules in SOUL.md and AGENTS.md. <br>
Mitigation: Back up SOUL.md and AGENTS.md before running the script, then inspect the added sections after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richardcoder849/cross-session-memory-config) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an idempotent setup script that appends missing memory-sharing rules to SOUL.md and AGENTS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
