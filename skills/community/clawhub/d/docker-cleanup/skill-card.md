## Description:

Docker Cleanup Toolkit helps agents analyze Docker resource usage, prune stopped containers, dangling images, unused volumes and orphaned networks, and generate cleanup reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Docker disk usage, identify reclaimable resources, and run controlled cleanup and reporting commands for local Docker environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker prune commands can remove stopped containers, dangling images, unused networks, or unused volumes, and force mode bypasses interactive confirmation.

Mitigation: Run analysis mode first, review Docker's unused-resource list, avoid --force and broad --all or --volumes cleanup on important systems, and ensure backups exist before pruning volumes.

Risk: Generated HTML reports load Bootstrap CSS from jsDelivr when opened.

Mitigation: Use plain text or JSON output when offline or avoiding third-party network requests, or review the HTML report dependency before opening it in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/docker-cleanup)
- [Publisher profile](https://clawhub.ai/user/ericlooi504)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; script output may be plain text, JSON, or HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can inspect Docker resources and, when cleanup flags are used, invoke Docker prune commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
