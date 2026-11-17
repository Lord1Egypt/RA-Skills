## Description:

Helps developers build HarmonyOS NEXT apps with the Baidu Maps HarmonyOS SDK, including map display, overlays, POI and AOI search, route planning, navigation, and location features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when adding Baidu Maps capabilities to HarmonyOS NEXT apps, especially map display, overlays, search, route planning, navigation, location, and related SDK package setup. It guides code changes, dependency selection, API lookup, and build checks for Baidu Maps HarmonyOS projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to perform broad dependency migrations and import rewrites across a HarmonyOS project.

Mitigation: Require explicit approval before package migrations, pin @bdmap package versions, review lockfile and source diffs, and run the documented build checks after changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/skills/baidu-map-harmonyos-sdk)
- [Baidu HarmonyNEXT SDK FAQ](https://lbsyun.baidu.com/faq/api?title=harmonynextsdk)
- [SDK Module Index](references/api/modules.md)
- [SDK Reference Guide](references/reference.md)
- [Package Management Guide](references/guidelines/package-management.md)
- [Build and Test Guide](references/guidelines/build-and-test.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with ArkTS/TypeScript code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dependency and import changes for @bdmap packages; review package migrations and lockfile diffs before applying.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
