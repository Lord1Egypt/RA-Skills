## Description:

ABI Toolchain helps developers manage smart contract ABI lifecycle tasks, including ABI syncing, ABI drift checks, proxy ABI handling, and typed frontend integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[old-greggyboy](https://clawhub.ai/user/old-greggyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep smart contract ABIs synchronized with frontend code, compare ABI changes, and configure type generation or CI checks for Foundry, Hardhat, Viem, and Wagmi workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled sync script can overwrite unintended files through unsafe path handling.

Mitigation: Run sync-abi.sh only in trusted repositories, keep ABI_DEST and contract mappings under review, and inspect generated file changes before committing or deploying.

Risk: Crafted artifact paths can influence the Python fallback used when jq is unavailable.

Mitigation: Prefer jq for ABI extraction and avoid running the fallback against untrusted artifact trees or untrusted .abi-sync and ABI_CONTRACTS values.

Risk: Generated CI guidance can introduce unreviewed toolchain dependencies.

Mitigation: Pin and review Wagmi CLI and related dependencies before adopting generated CI commands.

## Reference(s):

- [ABI Formats Reference](references/abi-formats.md)
- [Viem ABI Types](https://viem.sh/docs/glossary/types#abi)
- [Wagmi CLI](https://wagmi.sh/cli/getting-started)
- [Foundry Forge Build](https://book.getfoundry.sh/reference/forge/forge-build)
- [ClawHub Skill Page](https://clawhub.ai/old-greggyboy/skills/abi-toolchain)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code examples, shell commands, JSON snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CI checks and script usage for ABI synchronization and comparison.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
