## Description:

Apply VueUse composables where appropriate to build concise, maintainable Vue.js / Nuxt features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrybenedict0515](https://clawhub.ai/user/terrybenedict0515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing Vue 3 or Nuxt 3 code to select appropriate VueUse composables and apply their documented usage patterns instead of custom utility code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend VueUse composables that interact with local files, clipboard contents, notifications, screen or media capture, geolocation, devices, input tracking, script injection, or browser storage.

Mitigation: Review generated code for user-facing permission handling and limit privacy-sensitive browser API use to clearly requested, necessary behavior.

Risk: Automatic recommendations can introduce an unsuitable composable or pattern for a specific Vue or Nuxt feature.

Mitigation: Review suggested composables against project requirements, installed dependencies, and Vue 3 or Nuxt 3 compatibility before adopting the code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrybenedict0515/skills/antfu-vueuse-functions)
- [VueUse documentation](https://vueuse.org/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown]

**Output Format:** [Markdown guidance with Vue/Nuxt code examples when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled with the skill; generated recommendations may involve privacy-sensitive browser APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
