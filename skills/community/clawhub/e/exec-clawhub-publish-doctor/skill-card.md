## Description:

Diagnose and mitigate exec-related tooling failures around ClawHub publishing and GitHub CLI queries, including authentication, browser login, missing dependencies, pending security-scan visibility, profile or skill URL confusion, and GitHub CLI JSON-field mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebirdback](https://clawhub.ai/user/bluebirdback)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to troubleshoot ClawHub skill publishing failures, run preflight checks, publish with retry-aware verification, and recover from GitHub CLI repo-search field mismatches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawHub authentication tokens may be exposed if pasted into shared shell sessions or logs.

Mitigation: Use token login only in trusted shells and treat ClawHub tokens as secrets.

Risk: Helper scripts write diagnostic output to fixed /tmp paths that can be inappropriate on multi-user systems.

Mitigation: Review and replace fixed /tmp output paths before running the scripts on shared hosts.

Risk: Unpinned global npm install or --force guidance can install unexpected CLI versions.

Mitigation: Use pinned, verified CLI install commands when preparing production or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluebirdback/skills/exec-clawhub-publish-doctor)
- [Publisher profile](https://clawhub.ai/user/bluebirdback)
- [ClawHub Publish Error Map](references/error-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local helper scripts that run ClawHub and GitHub CLI commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
