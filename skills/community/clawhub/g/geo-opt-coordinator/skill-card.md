## Description:

GEO intelligent optimization coordinator for key setup, key verification, task listing, and routing single deep-imitation requests to companion skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill as a GEO workflow coordinator to configure the local GEO API key, verify access, inspect optimization task status, and delegate daily automation or deep-imitation actions to companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a local GEO API key file that could expose service access if logged, shared, or stored with broad permissions.

Mitigation: Store the key with restrictive file permissions, avoid printing it in logs or shell history, and rotate or revoke it if exposure is suspected.

Risk: The skill routes work to companion GEO skills, so stale companion-skill behavior could produce incorrect task handling.

Mitigation: Confirm that geo-cycle-autopilot, geo-mass-publish-check, and geo-deep-imitate are installed and aligned with the current GEO workflow before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chameleon-nexus/skills/geo-opt-coordinator)
- [GEO API Production Service](https://ai.gaobobo.cn)
- [GEO Optimization Tasks Endpoint](https://ai.gaobobo.cn/api/geo/optimization/tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local GEO key files at ~/.qclaw/geo-api-key or ~/.openclaw/geo-api-key and companion GEO workflow skills.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-06-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
