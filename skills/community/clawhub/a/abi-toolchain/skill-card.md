## Description: <br>
ABI lifecycle management for smart contract projects, including ABI generation, drift detection, proxy ABI handling, and typed frontend integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[old-greggyboy](https://clawhub.ai/user/old-greggyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep smart contract ABIs synchronized with frontend code, compare ABI changes, and apply Foundry, Hardhat, Viem, Wagmi, and proxy ABI patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script can write outside the intended ABI destination and has a fallback command-safety issue. <br>
Mitigation: Review or patch scripts/sync-abi.sh before CI or automatic build-hook use; run it only in trusted repositories, validate .abi-sync entries, constrain output paths under ABI_DEST, and prefer passing file paths to Python as arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/old-greggyboy/abi-toolchain) <br>
- [ABI formats reference](references/abi-formats.md) <br>
- [Viem ABI types](https://viem.sh/docs/glossary/types#abi) <br>
- [Wagmi CLI](https://wagmi.sh/cli/getting-started) <br>
- [Foundry forge build artifacts](https://book.getfoundry.sh/reference/forge/forge-build) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, TypeScript, JavaScript, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts for ABI synchronization and ABI diffing; users should review script behavior before CI or build-hook use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
