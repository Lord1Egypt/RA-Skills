## Description: <br>
Ampersend CLI for agent payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matiasedgeandnode](https://clawhub.ai/user/matiasedgeandnode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure the Ampersend CLI, manage agent payment credentials, and make paid x402 HTTP requests within user-defined spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real autonomous spending through paid requests. <br>
Mitigation: Install only when the user intentionally wants agent payments, set the smallest practical per-transaction, daily, and monthly limits, and inspect payment requirements before paid fetches. <br>
Risk: Automatic top-ups can increase the funds available to the agent. <br>
Mitigation: Avoid --auto-topup unless the user fully understands and accepts the funding path. <br>
Risk: Agent-visible dashboard sessions could expose approval or configuration controls. <br>
Mitigation: Keep dashboard approval and configuration in a browser the agent cannot access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matiasedgeandnode/asndurl) <br>
- [Publisher profile](https://clawhub.ai/user/matiasedgeandnode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ampersend CLI binary; Ampersend commands return JSON.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
