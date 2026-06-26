## Description: <br>
Use Cryptowerk to register documents and data, using hashes to maintain privacy, fetch seals, and verify proofs for files or append-only records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[holgercw](https://clawhub.ai/user/holgercw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create deterministic proof-carrying data workflows for files, verifiable logs, and append-only records using Cryptowerk seals and local sidecar artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cryptowerk receives hashes of files selected for registration or verification. <br>
Mitigation: Use the skill only when sharing stable hashes and proof timestamps with Cryptowerk is acceptable. <br>
Risk: Local cwconfig.json and .cwseal files may expose credentials or proof metadata if committed or synced. <br>
Mitigation: Keep these files out of public repositories, shared folders, and automated sync locations; restrict local file permissions. <br>
Risk: Stable hashes and proof timestamps may reveal too much about highly sensitive files. <br>
Mitigation: Avoid using the workflow on files where a persistent hash or timestamp would create unacceptable disclosure risk. <br>


## Reference(s): <br>
- [Cryptowerk API Notes](references/cryptowerk-api-notes.md) <br>
- [Storage and State](references/storage-and-state.md) <br>
- [Cryptowerk homepage](https://www.cryptowerk.com) <br>
- [ClawHub release page](https://clawhub.ai/holgercw/cryptowerk-verifiable-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON sidecar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Cryptowerk retrieval IDs, seals, and verification results stored in .cwseal sidecar files.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
