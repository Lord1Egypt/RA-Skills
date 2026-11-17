## Description:

Bun Runtime provides Bun-based filesystem, process, and network operations for agents that need native Bun APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabin-thami](https://clawhub.ai/user/rabin-thami)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run Bun-native file, glob, process, and HTTP operations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad local file, shell, and network authority with little scoping.

Mitigation: Run it only in a constrained sandbox, restrict file paths and network destinations, and require clear user approval before writes, commands, or outbound requests.

Risk: The security guidance identifies unsafe input handling.

Mitigation: Revise command and script invocation paths to avoid eval or generated source and pass data through arguments or stdin.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rabin-thami/skills/bun-runtime)
- [Publisher Profile](https://clawhub.ai/user/rabin-thami)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON command results and Markdown shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bun runtime and may read files, write files, run shell commands, and make network requests.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
