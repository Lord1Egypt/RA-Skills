## Description: <br>
Browser Devtools is a local command-line utility inspired by Chrome Dev Editor that exposes help, status, list, add, search, export, and related commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to ask an agent for browser-devtools shell commands, simple local status checks, and basic local data entry, search, and export workflows. It is best treated as a small command-line helper rather than a complete Chrome Dev Editor integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local command usage may be logged or stored in the tool's data directory. <br>
Mitigation: Review the help output first, set BROWSER_DEVTOOLS_DIR to a controlled location, and avoid passing tokens, passwords, private URLs, or sensitive project details. <br>
Risk: The skill presents itself as browser developer tooling, but the evidence describes a limited shell utility rather than a complete Chrome Dev Editor integration. <br>
Mitigation: Use it only for the documented helper commands and verify behavior locally before relying on it in a workflow. <br>


## Reference(s): <br>
- [Browser Devtools on ClawHub](https://clawhub.ai/xueyetianya/browser-devtools) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read from and write to a local browser-devtools data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
