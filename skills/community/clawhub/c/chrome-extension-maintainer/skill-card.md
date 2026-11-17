## Description:

Release-gate and maintenance workflow for Chrome extensions covering Chrome Web Store policy, MV3, privacy, permissions, SEO/GEO, analytics triage, browser E2E evidence, i18n, packaging, and green/yellow/red publish decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and extension maintainers use this skill to review Chrome extension release candidates, diagnose growth, analytics, privacy, permission, MV3, i18n, packaging, and public-surface issues, and produce green/yellow/red ship recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may ask an agent to inspect extension code, metadata, privacy claims, analytics exports, and local release artifacts.

Mitigation: Limit inputs to intended repositories and release artifacts, review findings before acting, and avoid sharing private or sensitive data unnecessarily.

Risk: Maintenance guidance could be mistaken for approval to upload, submit, unpublish, rollback, publish, or broadly promote an extension or skill package.

Mitigation: Require explicit user approval before irreversible external actions, registry publishing, store submission, unpublishing, rollback, or broad public promotion.

## Reference(s):

- [Chrome Extension Maintenance And Evolution Playbook](references/chrome-extension-maintenance-playbook.md)
- [Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies)
- [Chrome Web Store Privacy Policy Guidance](https://developer.chrome.com/docs/webstore/program-policies/privacy)
- [Declare Permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions)
- [MV3 Service Worker Lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle)
- [Extension End-to-End Testing](https://developer.chrome.com/docs/extensions/how-to/test/end-to-end-testing)
- [Chrome Web Store Rollback](https://developer.chrome.com/docs/webstore/rollback)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown review reports with command snippets and release-gate decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces findings, tests run, verified flows, blockers, rollback or recovery notes, and green/yellow/red recommendations; external publishing actions require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
