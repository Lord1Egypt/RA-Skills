## Description: <br>
This skill helps agents write, deploy, and interact with GenLayer Python smart contracts featuring LLM calls, web access, and blockchain-consensus-safe non-determinism. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acastellana](https://clawhub.ai/user/acastellana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to draft GenLayer Intelligent Contracts, choose SDK patterns, prepare deployment commands, and reason about equivalence principles for LLM and web-enabled smart contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated deployment or write commands can affect blockchain state or target the wrong network or account. <br>
Mitigation: Review commands before running them, use localnet or testnet first, and verify the active network and account before deploy or write operations. <br>
Risk: Examples involving private keys, LLM calls, or web rendering can expose secrets or sensitive data if copied without review. <br>
Mitigation: Do not paste real private keys into shells, do not send secrets or personal data to LLM or web-render examples, and prefer safer APIs and pinned dependencies for production. <br>
Risk: LLM and web-enabled contract logic can produce incorrect or misleading guidance if prompts, outputs, or equivalence principles are poorly chosen. <br>
Mitigation: Validate outputs against expected schemas, constrain user-controlled prompt input, and review equivalence principle choices before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/acastellana/genlayer-dev) <br>
- [GenLayer SDK API Reference](references/sdk-api.md) <br>
- [Equivalence Principles - In-Depth Guide](references/equivalence-principles.md) <br>
- [GenLayer Contract Examples](references/examples.md) <br>
- [GenLayer Deployment Guide](references/deployment.md) <br>
- [GenVM Internals](references/genvm-internals.md) <br>
- [GenLayer Documentation](https://docs.genlayer.com) <br>
- [GenLayer SDK](https://sdk.genlayer.com) <br>
- [GenLayer Studio](https://studio.genlayer.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; review generated commands, active network, account, and secrets handling before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
