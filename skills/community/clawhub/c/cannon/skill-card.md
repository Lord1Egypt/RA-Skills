## Description: <br>
Cannon package manager for Ethereum deployments. Use when building, testing, deploying, or inspecting Cannon packages. Covers cannonfile syntax, CLI commands (build, run, test, publish, inspect), actions (deploy, invoke, clone, pull, router, diamond), and package workflows. NOT for general Solidity development questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbeal-eth](https://clawhub.ai/user/dbeal-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Cannon package workflows for Ethereum smart contract builds, tests, deployments, publishing, inspection, and registry operations. It is intended for Cannon-specific deployment work, not general Solidity development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real Cannon deploy, publish, register, or publisher-management commands can affect on-chain state, fees, package ownership, or published artifacts. <br>
Mitigation: Run dry-run first, explain the exact operation, and verify chain ID, RPC URL, wallet, package/version, artifacts, fees, and command before any real execution. <br>
Risk: Private keys or privileged wallets used for deployment and publishing can expose funds or package permissions if mishandled. <br>
Mitigation: Use a dedicated low-balance deployment key, prefer environment variables or impersonation for simulations, and require explicit approval before using a real private key. <br>
Risk: Wrong-network or wrong-version deployment guidance can create irreversible blockchain state. <br>
Mitigation: Test locally on Cannon Network chain 13370 before target chains and confirm package references, presets, and target network details with the user. <br>


## Reference(s): <br>
- [Cannon CLI Reference](references/cli.md) <br>
- [Cannonfile Specification](references/cannonfile.md) <br>
- [Testing Patterns](references/testing.md) <br>
- [Registry and Publishing](references/registry.md) <br>
- [Full Cannonfile JSON Schema](https://raw.githubusercontent.com/usecannon/cannon/refs/heads/dev/packages/lsp/src/schema.json) <br>
- [Cannonfile Fragment JSON Schema](https://raw.githubusercontent.com/usecannon/cannon/refs/heads/dev/packages/lsp/src/schema-fragment.json) <br>
- [Cannon Deployments](https://usecannon.com/deploy) <br>
- [Cannon Website](https://usecannon.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose high-impact blockchain commands that require dry-run, review, and explicit confirmation before real execution.] <br>

## Skill Version(s): <br>
2.26.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
