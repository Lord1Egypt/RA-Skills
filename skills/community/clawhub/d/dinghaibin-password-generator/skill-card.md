## Description: <br>
Generate passwords, PINs, and passphrases from command-line options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to generate candidate passwords, PINs, or memorable passphrases for low-risk workflows and local testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords, PINs, and passphrases should not be treated as cryptographically secure because the security evidence reports non-cryptographic randomness. <br>
Mitigation: Use the outputs only for low-risk testing or update the implementation to use Python's secrets module or another CSPRNG before generating real secrets. <br>
Risk: The skill text claims secure generation, which may overstate the protection provided by the current implementation. <br>
Mitigation: Review the generated values and documentation before deployment, and avoid using this release for account passwords, API tokens, recovery codes, or other important secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/dinghaibin-password-generator) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text values and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script supports configurable length, character classes, exclusions, PIN mode, passphrase mode, separators, and count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
