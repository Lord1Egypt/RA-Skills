## Description: <br>
Automate builds, tests, and deployments across web, mobile, and backend applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to select CI/CD platforms, create build and deployment workflows, debug failed builds, and apply web and mobile pipeline patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CI/CD snippets can expose credentials or signing material if copied without production hardening. <br>
Mitigation: Store credentials only in protected CI secret stores, require approvals for production deploys, pin and review third-party actions, avoid caching or uploading signing files, and delete decoded keystores after builds. <br>
Risk: Workflow examples may need environment-specific review before production deployment. <br>
Mitigation: Review proposed workflows against the target repository, runner permissions, deployment environment, and release approval process before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/ci-cd) <br>
- [Mobile CI/CD Patterns](mobile.md) <br>
- [CI/CD Templates](templates.md) <br>
- [Web CI/CD Patterns](web.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides copy-paste CI/CD snippets and implementation guidance for web, mobile, Docker, GitHub Actions, and GitLab CI workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
