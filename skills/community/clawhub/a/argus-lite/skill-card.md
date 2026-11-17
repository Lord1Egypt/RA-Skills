## Description:

Argus Lite scans a single Python file for ten critical and high-priority security and bug patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Argus Lite to run a lightweight review of one Python file for common security issues and bug patterns before deeper review or scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review verdict is suspicious because the install step and runtime behavior need review before use.

Mitigation: Review the skill before installing, run it in a virtual environment, and pin or verify the rich dependency.

Risk: The default SOURCE_PATH value can scan the first Python file found from the current directory instead of an explicit target.

Mitigation: Set SOURCE_PATH to an explicit Python file before running the scan.

Risk: The skill includes an upgrade and payment prompt that is advertising rather than scan output.

Mitigation: Treat Pro install and purchase links as promotional content and separate them from security findings.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/occupythemilkyway/argus-lite)
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/argus-lite)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown instructions with bash and Python code blocks; terminal text and table scan results when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, pip3, and the rich Python package; SOURCE_PATH selects the Python file or directory to scan.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
