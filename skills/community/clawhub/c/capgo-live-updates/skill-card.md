## Description:

Guides developers through implementing Capgo live updates in Capacitor apps, including setup, configuration, rollout strategies, and CI/CD integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riderx](https://clawhub.ai/user/riderx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this guide to add and manage web-layer over-the-air updates in Capacitor apps with Capgo, including staged releases and rollback. Native changes still require an app-store release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed live updates could disrupt production apps or conflict with app-store and user-consent requirements.

Mitigation: Test on beta or staged channels, retain release changelogs and approval controls, and check applicable store and consent rules.

Risk: CI examples can expose deployment credentials or pull changing dependencies.

Mitigation: Protect CAPGO_TOKEN as a CI secret and pin CLI and container versions before production use.

## Reference(s):

- [Capgo documentation](https://capgo.app/docs)
- [Capgo Capacitor updater plugin](https://github.com/Cap-go/capacitor-updater)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript, shell, and CI configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
