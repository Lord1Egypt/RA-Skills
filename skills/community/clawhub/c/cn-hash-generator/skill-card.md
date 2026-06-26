## Description: <br>
Generates MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b hashes, Base64 encodings and decodings, UUIDs, and HMAC signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to generate hashes, Base64 encodings and decodings, UUIDs, and HMAC signatures locally with a Python standard-library utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HMAC keys or sensitive text passed on the command line may be retained by shell history or terminal logging. <br>
Mitigation: Avoid placing reusable secrets directly in shell commands; prefer short-lived inputs, stdin where practical, and a terminal environment with history disabled or cleared for sensitive use. <br>
Risk: MD5 and SHA-1 are available for compatibility but are weak choices for new security-sensitive integrity or authentication workflows. <br>
Mitigation: Use SHA-256, SHA-512, BLAKE2b, or HMAC with SHA-256 or stronger algorithms for security-sensitive use; reserve MD5 and SHA-1 for legacy compatibility checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freedompixels/cn-hash-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python 3.7+ standard-library utility; server security evidence found no network access, persistence, or hidden data collection.] <br>

## Skill Version(s): <br>
1.2.8 (source: server release evidence; artifact frontmatter reports 1.2.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
