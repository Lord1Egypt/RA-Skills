## Description:

Guides developers in adding and reviewing installable Progressive Web Apps with offline support, safe caching policies, and visible update prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to implement or review web app installability, service workers, offline fallbacks, caching rules, and user-controlled updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caching sensitive or write requests could expose stale or private data.

Mitigation: Keep authentication, payments, permission changes, and write endpoints network-only; review service worker scope and caching rules.

Risk: Silent service worker activation could unexpectedly refresh a user's work.

Mitigation: Show a clear update prompt and let the user choose when to refresh.

## Reference(s):

- [Manifest, icon and installation entrance](references/manifest-and-icons.md)
- [Service Worker, Workbox and update flow](references/service-worker-workbox.md)
- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-pwa-implementation)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include manifest settings, service worker policies, offline fallback, and update prompts.]

## Skill Version(s):

2.9.0 (source: server release, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
