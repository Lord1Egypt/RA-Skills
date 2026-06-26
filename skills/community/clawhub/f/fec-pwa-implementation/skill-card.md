## Description: <br>
Provides Progressive Web App implementation guidance for installability, manifest metadata, Service Worker registration, Workbox caching, offline fallback, update prompts, maskable icons, and iOS compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adding or reviewing PWA behavior for installable web apps, weak-network/offline fallback scenarios, repeat-visit caching, and visible update flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service Worker cache rules can accidentally cache authentication, payment, permission-changing, or other sensitive requests. <br>
Mitigation: Review the generated Service Worker scope and cache rules, and keep sensitive requests network-only. <br>
Risk: Offline fallback, update prompts, and Service Worker removal behavior can fail differently across browsers and installed-app surfaces. <br>
Mitigation: Test update prompts, offline fallback, and Service Worker removal behavior before shipping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-pwa-implementation) <br>
- [Manifest and icons reference](references/manifest-and-icons.md) <br>
- [Service Worker and Workbox reference](references/service-worker-workbox.md) <br>
- [Frontend Craft repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON, and HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on PWA manifests, Service Worker registration, Workbox caching, offline fallback, install prompts, update prompts, and validation steps.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
