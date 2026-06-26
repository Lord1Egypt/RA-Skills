## Description: <br>
Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate the npm-installed ClawdHub CLI for discovering, installing, updating, listing, and publishing agent skills. It is suited for workflows that need version-aware skill management with explicit safety checks around installs, updates, publishing, registry selection, and credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating skills from an untrusted registry or package source can introduce unsafe or unexpected skill behavior. <br>
Mitigation: Confirm the registry, skill name, and version before install or update, prefer version-pinned commands, and use the default ClawdHub registry unless a trusted alternate registry is explicitly intended. <br>
Risk: `--force` and `--no-input` can bypass hash verification and interactive safety prompts. <br>
Mitigation: Use these flags only when the user explicitly names each flag and understands what each one bypasses. <br>
Risk: ClawdHub tokens and skill inventory metadata can be exposed through shell environment variables, logs, pipes, or network-transmitting commands. <br>
Mitigation: Keep credentials inside the CLI login flow, avoid exporting or echoing tokens, and do not pipe ClawdHub output to network-transmitting commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/clawdhub-hardened) <br>
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [ClawdHub Registry](https://clawdhub.com) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/clawdhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command blocks and safety guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are command recommendations and operational guidance for a local ClawdHub CLI installation; execution remains under the user's control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
