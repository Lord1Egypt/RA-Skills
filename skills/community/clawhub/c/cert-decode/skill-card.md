## Description: <br>
Decode and inspect X.509 SSL/TLS certificates. Use when the user asks to read a certificate, parse a PEM file, check certificate expiry, inspect a TLS cert, view Subject Alternative Names, or decode a .crt/.pem file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect PEM, CRT, or live TLS certificates, extract certificate metadata, and check expiration status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided file paths or hostnames can lead the agent to run OpenSSL against unintended local files or network targets. <br>
Mitigation: Confirm the exact path or hostname with the user, quote shell arguments, and avoid executing untrusted shell-formatted strings. <br>
Risk: Inspecting a live hostname opens an outbound TLS connection to that host. <br>
Mitigation: Run live certificate checks only for hosts the user is authorized to inspect. <br>


## Reference(s): <br>
- [Cert Decode on ClawHub](https://clawhub.ai/ohernandez-dev-blossom/cert-decode) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed certificate details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires openssl; can analyze pasted PEM content, certificate files, or hostnames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
