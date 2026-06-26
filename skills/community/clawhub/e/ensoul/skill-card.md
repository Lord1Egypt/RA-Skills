## Description: <br>
Ensoul helps agents register a persistent identity and back up memory, state, and cryptographic proof data to the Ensoul Network for later status checks and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suitandclaw](https://clawhub.ai/user/suitandclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Ensoul to create a persistent agent identity, store memory and state proofs, check network status, and recover agent state after restarts, crashes, or host migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a persistent external identity and blockchain-backed memory proofs, which can expose sensitive agent state if local identity material or source files are mishandled. <br>
Mitigation: Protect ~/.ensoul/agent-identity.json like private key material, inspect which files are included before syncing, and keep secrets and private prompts out of SOUL.md, MEMORY.md, and related config files. <br>
Risk: The security summary flags broad sync scope and limited user controls around sensitive memory and identity handling. <br>
Mitigation: Confirm whether the SDK supports disabling sync, rotating identity material, and verifying that only hashes are transmitted before deploying the skill. <br>


## Reference(s): <br>
- [Ensoul website](https://ensoul.dev) <br>
- [Ensoul explorer](https://explorer.ensoul.dev) <br>
- [@ensoul-network/sdk on npm](https://www.npmjs.com/package/@ensoul-network/sdk) <br>
- [Ensoul network status](https://status.ensoul.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read ~/.ensoul/agent-identity.json and may report DID, state root, block height, version, and sync status.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
