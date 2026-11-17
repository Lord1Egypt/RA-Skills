## Description:

Exfer helps agents use a permissionless proof-of-work blockchain for machine-to-machine payments, wallet balance checks, HTLCs, mining, and covenant-based transaction flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahuman-exfer](https://clawhub.ai/user/ahuman-exfer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Exfer to automate value-bearing blockchain workflows such as wallet creation, balance checks, payments, HTLCs, multisig, escrow, vaults, delegation, node operation, and mining.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running downloaded binaries from an unpinned latest release can execute unverified code.

Mitigation: Pin the release and verify a checksum or signature from a trusted source before running the binary.

Risk: Wallet passphrases placed in environment variables can be exposed on shared or logged systems.

Mitigation: Use EXFER_PASS only in controlled environments and avoid shell history, process inspection, and centralized logging exposure.

Risk: Payment, contract, and mining examples may perform real value-bearing blockchain actions.

Mitigation: Review amounts, addresses, RPC endpoints, fees, and timeouts before execution, and test with non-production funds where possible.

Risk: Background mining examples can create persistent processes through nohup or LaunchAgent.

Mitigation: Enable background mining only intentionally and document how to stop and remove the service before deployment.

## Reference(s):

- [Exfer repository](https://github.com/ahuman-exfer/exfer)
- [ClawHub Exfer skill page](https://clawhub.ai/ahuman-exfer/skills/exfer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with shell, PowerShell, JSON, and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXFER_PASS for non-interactive wallet passphrase workflows; examples can initiate real blockchain transactions or persistent mining.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
