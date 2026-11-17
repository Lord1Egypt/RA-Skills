## Description:

Builds, debugs, ships, and hardens Android apps: Gradle, Jetpack Compose, XML Views, ADB, and the Play release path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to diagnose, implement, test, harden, and ship native Android apps across build, install, runtime, and Play release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read and maintain local Clawic Android notes, device/project/contact rows, and release metadata.

Mitigation: Install only if that local data access is acceptable, and keep writes inside the disclosed configuration paths.

Risk: Android logs, Gradle properties, local properties, signing setup, and CI uploads can expose credential material or sensitive release actions.

Mitigation: Store only secret pointers, never credential values, and explicitly approve destructive device or store actions, Gradle build scans, and CI or Play uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/android)
- [Skill homepage](https://clawic.com/skills/android)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file updates for Android notes and shared device, project, contact, and release records; does not store credential values.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
