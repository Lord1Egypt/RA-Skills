## Description: <br>
Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Regan-Milne](https://clawhub.ai/user/Regan-Milne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to persist and restore encrypted agent memory across sessions and machines through a Jackal-backed storage service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memory is persisted to an external third-party service. <br>
Mitigation: Use the skill only for memory you are comfortable storing through that service, and avoid saving secrets or private data. <br>
Risk: The encryption key can appear in normal command output when key generation is run. <br>
Mitigation: Run key generation only in private terminals and keep logs or shared sessions from capturing the key. <br>
Risk: Encrypted memories are unrecoverable if the local encryption key is lost. <br>
Mitigation: Back up the encryption key securely before relying on the stored memory. <br>


## Reference(s): <br>
- [Claw Store Skill](https://clawhub.ai/Regan-Milne/claw-store-skill) <br>
- [Claw Store service homepage](https://web-production-5cce7.up.railway.app) <br>
- [Claw Store login](https://web-production-5cce7.up.railway.app/auth/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JACKAL_MEMORY_API_KEY and the Python cryptography package for the bundled client.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
