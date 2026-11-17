## Description:

Run one release-time security sweep over an agent's own surfaces: prompt-injection exposure, MCP tool permission boundaries, secret leaks, and dependency risk. Use before tagging a release, after adding a tool, or when a scanner flags your repo. Four paid calls per sweep, all inline, no operator queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this workflow before a release or after tool changes to review prompt-injection exposure, MCP tool permissions, secret leaks, and dependency risks. It returns findings to support release gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan requests may contain confidential prompts, tool descriptions, configuration, logs, diffs, or dependency manifests; the workflow can retain request data in repository outputs.

Mitigation: Review and redact submissions before sending them; check the provider's data-handling terms; store retry payloads in restricted temporary storage outside the repository; exclude reports from version control and delete temporary data afterward; set a spending limit before paid retries.

## Reference(s):

- [DDG Agent Security Sweep on ClawHub](https://clawhub.ai/0xcircuitbreaker/skills/ddg-agent-security-sweep)
- [DDG Agent API](https://agents.daedalusdevelopmentgroup.com)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Files, Guidance]

**Output Format:** [Structured JSON scan reports with release-gating findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and request payloads may contain confidential information and should be handled as restricted data.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
