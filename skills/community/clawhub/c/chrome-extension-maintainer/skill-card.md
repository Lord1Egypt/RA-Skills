## Description: <br>
Release-gate and maintenance workflow for Chrome extensions covering Chrome Web Store policy, MV3, privacy, permissions, SEO/GEO, analytics triage, browser E2E evidence, i18n, packaging, and green/yellow/red publish decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Chrome extension release candidates, diagnose growth or analytics issues, align public surfaces, assess privacy and permission risk, choose validation gates, and produce a green/yellow/red ship recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide review of private extension code, analytics exports, support messages, and public listing or privacy materials supplied by the user. <br>
Mitigation: Limit provided inputs to the release evidence needed for the review, avoid unnecessary sensitive data, and review outputs before sharing them outside the project. <br>
Risk: Release, rollback, upload, submit, unpublish, deletion, registry publish, or broad promotion actions can be irreversible or externally visible. <br>
Mitigation: Require explicit user approval before any irreversible or external release action and report missing evidence as a blocker instead of inventing proof. <br>
Risk: Chrome Web Store policy, Chrome platform behavior, competitor claims, and search behavior can change over time. <br>
Mitigation: Verify current authoritative sources before making policy-sensitive release decisions or public claims. <br>


## Reference(s): <br>
- [Chrome Extension Maintenance And Evolution Playbook](references/chrome-extension-maintenance-playbook.md) <br>
- [Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies) <br>
- [Chrome Web Store Privacy Guidance](https://developer.chrome.com/docs/webstore/program-policies/privacy) <br>
- [Declare Extension Permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions) <br>
- [MV3 Service Worker Lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle) <br>
- [Extension End-to-End Testing](https://developer.chrome.com/docs/extensions/how-to/test/end-to-end-testing) <br>
- [Test Service Worker Termination](https://developer.chrome.com/docs/extensions/how-to/test/test-serviceworker-termination-with-puppeteer) <br>
- [Chrome Extension i18n API](https://developer.chrome.com/docs/extensions/reference/api/i18n) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, checklists, findings, file-change summaries, and ship-gate decisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should lead with critical findings, report validation evidence, identify release blockers, and end with a green/yellow/red recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
