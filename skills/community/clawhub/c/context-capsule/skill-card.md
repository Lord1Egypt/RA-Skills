## Description: <br>
Compresses older OpenClaw agent session history into a bounded, lane-change-aware context capsule that keeps recent messages verbatim, flags abandoned directions, quarantines injected instructions, and redacts secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parad0x-labs](https://clawhub.ai/user/parad0x-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce prompt size in long-running OpenClaw sessions while preserving recent messages and high-value older context such as decisions, tasks, errors, files, links, questions, and durable facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Older session history is compressed into a lossy capsule, so exact wording, nuance, and low-priority details can be lost. <br>
Mitigation: Use normal history or a retrieval system when verbatim transcript fidelity is required, and review important long-session context before relying on it. <br>
Risk: Secret and PII redaction is best-effort pattern matching and should not be treated as a formal privacy guarantee. <br>
Mitigation: Avoid using the skill as the only safeguard for sensitive chats, and keep credential handling controls in place before agent sessions reach the context engine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parad0x-labs/context-capsule) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Plain-text extractive context capsule with configurable plugin settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Capsule size and activation are controlled by minMessages, keepRecentMessages, maxCapsuleTokens, capsuleTokenRatio, and minCompressTokens.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
