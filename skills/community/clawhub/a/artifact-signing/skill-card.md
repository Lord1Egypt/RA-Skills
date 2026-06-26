## Description: <br>
A skill to sign artifacts using a digital certificate and private key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rajaryan18](https://clawhub.ai/user/rajaryan18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to sign local files, binaries, or release artifacts with a PEM-encoded private key and produce detached signature files for later verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private signing keys may be exposed or misused if an agent is given broad filesystem access or an unrestricted key. <br>
Mitigation: Use a limited-purpose signing key, prefer encrypted or hardware-backed key storage, and confirm the key path before signing. <br>
Risk: The skill creates detached signatures but does not provide certificate-chain identity guarantees. <br>
Mitigation: Verify signatures with the intended public key and do not rely on this skill for certificate-backed identity unless certificate support is added. <br>
Risk: An incorrect artifact or output path could result in signing the wrong file or writing a signature in an unintended location. <br>
Mitigation: Verify exact input and output paths before execution. <br>


## Reference(s): <br>
- [Artifact Signing release page](https://clawhub.ai/rajaryan18/artifact-signing) <br>
- [Usage examples](examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces detached signature files when the included signing script is executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
