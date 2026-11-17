## Description:

Provides Chinese-language guidance for developing and managing a Vue 3 and Flask Project Portal admin system with RBAC, multi-project workflows, media uploads, S3-compatible storage, content management, settings, and logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[258468639](https://clawhub.ai/user/258468639)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill as implementation guidance for a Project Portal admin system. It helps plan and maintain RBAC, user and role management, project records, image and attachment handling, S3-compatible storage, dynamic content, system settings, and operational logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative RBAC changes, password resets, account disabling, S3 deletion, upload handling, and file proxying can affect access, expose files, or lose data if used carelessly.

Mitigation: Restrict those workflows to authorized administrators and review changes before applying them to production systems.

Risk: The skill describes a documentation-only admin portal workflow, so generated implementation guidance may still need project-specific security review.

Mitigation: Review authentication, authorization, upload limits, storage permissions, and file proxy behavior against the target deployment before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/258468639/skills/backend-admin-dev-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/258468639)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code paths, API routes, configuration names, and deployment notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only Chinese-language skill; no hidden execution, persistence, or deceptive behavior reported by server security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
