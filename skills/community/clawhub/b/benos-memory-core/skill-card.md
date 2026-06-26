## Description: <br>
Core runtime and volatile memory module for BenOS agents to store and retrieve active session state, open loops, decisions, and scratch notes at runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benmjohnson69](https://clawhub.ai/user/benmjohnson69) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let BenOS agents hydrate local session context and reuse active initiatives, open loops, recent decisions, and notes across runtime interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface stale or sensitive local session memory from BenOS runtime files. <br>
Mitigation: Do not store secrets or untrusted instructions in runtime files, and periodically inspect or clear ~/.openclaw/workspace/benos/runtime/. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benmjohnson69/benos-memory-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [JSON objects containing status messages and hydrated local memory state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local BenOS runtime files when present; no external API calls are evidenced.] <br>

## Skill Version(s): <br>
0.1.2 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
