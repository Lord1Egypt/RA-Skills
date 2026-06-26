## Description: <br>
Reduce Anthropic API costs for OpenClaw agents by guiding cache, compaction, context hygiene, token budgeting, and codebase map practices for Claude models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngocgd](https://clawhub.ai/user/ngocgd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce Anthropic API spend in OpenClaw sessions by tuning configuration, controlling context growth, and applying repeatable navigation and compaction habits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration recommendations can change context retention, cache behavior, or session continuity. <br>
Mitigation: Review proposed openclaw.json changes before applying them and align TTL, heartbeat, compaction, and bootstrap limits with the user's workflow. <br>
Risk: Memory files and codebase maps can accidentally retain sensitive project details. <br>
Mitigation: Avoid storing secrets in memory or map files, and review generated maps before sharing or committing them. <br>
Risk: The optional atris install command fetches a separate package outside this artifact. <br>
Mitigation: Inspect the atris package before running the optional npx install command and follow the organization's package trust policy. <br>


## Reference(s): <br>
- [Anthropic Token Optimizer Skill Page](https://clawhub.ai/ngocgd/anthropic-token-optimizer) <br>
- [openclaw-token-optimizer](https://clawhub.ai/asif2bd/openclaw-token-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only recommendations; users review changes before applying them.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
