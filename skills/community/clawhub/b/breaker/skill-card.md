## Description: <br>
Breaker provides shell-command workflows for recording, listing, searching, exporting, and deleting local breaker-related entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to run a local CLI that stores, searches, removes, exports, and reports basic statistics for breaker-related entries. Review outputs carefully because the security evidence says the tool behaves as a local persistent record manager rather than a circuit breaker sizing or coordination engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is presented as a circuit-breaker engineering tool, but security evidence says it behaves like a local persistent notes or data manager. <br>
Mitigation: Do not rely on it for circuit breaker sizing or coordination; use it only for local record management unless independently reviewed and validated. <br>
Risk: Entries are retained locally and can later be exported or deleted. <br>
Mitigation: Avoid entering sensitive facility or operational data unless local retention and later export are acceptable. <br>


## Reference(s): <br>
- [Breaker on ClawHub](https://clawhub.ai/bytesagain1/breaker) <br>
- [bytesagain1 publisher profile](https://clawhub.ai/user/bytesagain1) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text with optional JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.breaker by default, or under BREAKER_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
