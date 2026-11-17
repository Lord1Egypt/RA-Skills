## Description:

Baidu Map RTOS Skills helps developers integrate the Baidu Map RTOS SDK application layer, including authentication, map components, Canvas adapters, overlays, search, offline maps, navigation, and mapAPP demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and review C/C++ integration guidance for Baidu Map RTOS SDK application-layer work, including initialization, authentication, Canvas adapters, map overlays, search, offline maps, navigation, and simulator demo extensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers Baidu internal SDK material that may require authorization.

Mitigation: Confirm authorization to use the Baidu Map RTOS SDK material before installing the skill or applying generated examples.

Risk: Generated search, routing, navigation, offline-download, and deletion examples may send location or query data over the network or consume local storage.

Mitigation: Review privacy, network, and storage implications before running generated SDK operations, especially with real users or production data.

Risk: Incorrect thread handling or Canvas adapter implementation can cause rendering failures or crashes in RTOS or simulator integrations.

Mitigation: Keep rendering work on the UI thread, bind the platform canvas before SetCanvas, and validate adapter behavior against the provided integration checklist.

## Reference(s):

- [Skill Definition](SKILL.md)
- [English README](README_EN.md)
- [Initialization, Authentication, and Canvas Adapter](references/init-auth.md)
- [Platform Adapter and Canvas Implementation](references/adapter-build.md)
- [Map State, Overlays, and Touch](references/overlay-map-control.md)
- [Search, Navigation, Offline Maps, and mapAPP Demo Extension](references/search-navi-offline.md)
- [End-to-End Demo Examples](references/demo.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with C/C++ code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK integration sequences, adapter implementation notes, API usage examples, and troubleshooting checks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
