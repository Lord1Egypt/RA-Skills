## Description: <br>
Multi-format encoder, decoder, and hasher supporting Base64, Base64URL, Base32, Hex, URL-encoding, HTML entities, ROT13, Binary, ASCII85, and common hash algorithms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to encode, decode, hash, and identify encoded strings or file contents during local development, debugging, and data handling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive values may be exposed in shell history when passed as command-line arguments. <br>
Mitigation: Use stdin or file input for sensitive values. <br>
Risk: MD5 and SHA-1 are available but are not appropriate for security-sensitive integrity checks. <br>
Mitigation: Use stronger algorithms such as SHA-256, SHA-512, or SHA3-256 for security-sensitive hashing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Johnnywang2001/encoding-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python standard library tool; accepts input as arguments, stdin, or files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
