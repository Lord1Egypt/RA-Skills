## Description:

Guides agents to suggest an automated workflow for scanning and remediating npm dependency vulnerabilities in Node.js projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jelllove](https://clawhub.ai/user/jelllove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when npm audit results or dependency CVEs require remediation guidance. It prompts use of an automated workflow that scans project package directories, applies npm audit fixes, refreshes dependencies, and verifies builds and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits silent installation of unpinned global tools for npm vulnerability workflows.

Mitigation: Require user approval before installing missing tools, show the exact package and command, and prefer project-local or pinned tooling over global installs.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces advisory text that may lead an agent to run project-local npm audit and remediation commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
