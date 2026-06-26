## Description: <br>
Cipher65536 encodes and decodes files as Base65536 Unicode text, with optional gzip compression, filename preservation, and scramble mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to convert arbitrary files into text for transfer through text-only channels, then decode the text back into files. It can also apply compression and a scramble mode when users need basic obfuscation during transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used to bypass upload restrictions or workplace, DLP, and moderation controls. <br>
Mitigation: Use only where policy permits text-based file transfer, and do not use it to evade platform or organizational controls. <br>
Risk: The scramble mode overstates the safety of its custom encryption and may be unsuitable for highly sensitive files. <br>
Mitigation: Do not rely on scramble mode for high-sensitivity data; use reviewed cryptographic tools for confidential material. <br>
Risk: Generated key files are sensitive secrets, and encrypted files cannot be recovered if the key is lost. <br>
Mitigation: Store key files securely, transmit them separately from encoded content, and maintain a protected backup when recovery matters. <br>
Risk: Decoding untrusted text can write restored files to disk. <br>
Mitigation: Use explicit safe output paths, inspect decoded filenames, and verify restored files before opening them. <br>


## Reference(s): <br>
- [Encoding Details](references/encoding-details.md) <br>
- [Scramble Mode Details](references/scrambleing-details.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/turinfohlen/cipher65536) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Text files and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encoded output may contain high-plane Unicode characters; decoded output writes files to the local filesystem.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
