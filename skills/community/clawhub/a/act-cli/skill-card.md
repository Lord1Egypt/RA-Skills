## Description: <br>
Runs ACT WebAssembly component tools via `act call` for agents that need sandboxed tools such as SQLite, HTTP, or filesystem components without system dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[actcore](https://clawhub.ai/user/actcore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover ACT component tools, inspect their schemas, and run them with JSON arguments, metadata, and explicit filesystem grants when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote or untrusted WebAssembly components can be risky when combined with broad filesystem grants. <br>
Mitigation: Use pinned or trusted component references, inspect tools with `act info` first, and grant only the narrow directory access needed instead of using full filesystem access by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/actcore/act-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [ACT command output is JSON on stdout; logs go to stderr.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
