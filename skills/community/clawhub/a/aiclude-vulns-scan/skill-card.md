## Description:

Search security vulnerability scan results for MCP Servers and AI Agent Skills from the AICLUDE scan database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastergear4824](https://clawhub.ai/user/mastergear4824)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and security reviewers use this skill to look up vulnerability reports for MCP servers and AI agent skills, or to register a target for server-side scanning when no prior report exists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried package names and target types are sent to AICLUDE for lookup and possible server-side scanning.

Mitigation: Use the skill only when sharing that package-identifying information with AICLUDE is acceptable.

Risk: The artifact security evidence notes dependency hygiene issues in dev dependencies.

Mitigation: Refresh the lockfile and patch flagged dev dependencies before running tests, build tools, or development servers in shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mastergear4824/skills/aiclude-vulns-scan)
- [AICLUDE scan dashboard](https://vs.aiclude.com)
- [AICLUDE security skill npm package](https://www.npmjs.com/package/@aiclude/security-skill)
- [AICLUDE security MCP npm package](https://www.npmjs.com/package/@aiclude/security-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown vulnerability report with risk levels, findings, assessments, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries send the package name and target type to AICLUDE; source code, files, and credentials are not sent according to the artifact documentation.]

## Skill Version(s):

3.0.0 (source: release evidence and package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
