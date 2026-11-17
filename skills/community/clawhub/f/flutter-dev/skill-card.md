## Description:

Flutter Dev provides guidance for cross-platform Flutter development, including widget patterns, Riverpod and Bloc state management, GoRouter navigation, performance optimization, platform integration, testing, networking, forms, animations, and localization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smasherlxd](https://clawhub.ai/user/smasherlxd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get practical Flutter implementation guidance, code patterns, checklists, and testing or performance advice while building cross-platform mobile, web, and desktop applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Networking examples may log request bodies, response details, errors, or tokens if copied directly into a production Flutter app.

Mitigation: Redact logs and disable request or body logging in production builds.

Risk: Caching examples may store sensitive or user-specific API responses without enough production hardening.

Mitigation: Allowlist cacheable endpoints, avoid or encrypt sensitive caches, and clear user-specific caches on logout.

Risk: Platform examples include broad mobile permissions that could be unnecessary for a specific app feature.

Mitigation: Request only the mobile permissions required for implemented features and review platform permission prompts before release.

## Reference(s):

- [Widget Patterns](references/widget-patterns.md)
- [Riverpod State Management](references/riverpod-state.md)
- [Bloc State Management](references/bloc-state.md)
- [GoRouter Navigation](references/gorouter-navigation.md)
- [Project Structure](references/project-structure.md)
- [Performance Optimization](references/performance.md)
- [Testing Strategies](references/testing.md)
- [Platform Integration](references/platform-specific.md)
- [Animations](references/animations.md)
- [Networking](references/networking.md)
- [Forms](references/forms.md)
- [Localization](references/localization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Dart, YAML, shell, Swift, Kotlin, XML, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include copy-pasteable implementation snippets, checklists, and recommendations that should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
