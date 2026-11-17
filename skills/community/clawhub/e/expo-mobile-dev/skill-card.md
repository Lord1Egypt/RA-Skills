## Description:

Expo Mobile Dev guides agents through scaffolding and configuring a React Native Expo app with region-aware choices for international and China mainland releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to start Expo mobile projects, select a target region, install an opinionated React Native stack, and plan authentication, backend, OTA update, and store-submission paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs many remote agent skills that can influence later agent sessions.

Mitigation: Review each remote skill source, pin trusted versions where possible, and install only the subset needed for the project.

Risk: Credential-generation steps can expose secrets through terminal output, shell history, or CI logs.

Mitigation: Run credential generation locally, avoid retained logs, gitignore private key and env files, and store generated secrets in EAS Secrets or the hosting provider's secret store.

Risk: The workflow can scaffold projects, install packages, and fetch current documentation over the network.

Mitigation: Review proposed shell commands before execution and run them in a project workspace where package and configuration changes can be inspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenshowinnovation/skills/expo-mobile-dev)
- [Backend / API Server](references/backend.md)
- [Authentication](references/auth.md)
- [China Mainland Deployment Guide](references/china-deployment.md)
- [Store Presence & Metadata](references/store-presence.md)
- [EAS Build & Submit Recipes](references/eas-recipes.md)
- [app.config.ts Patterns](references/app-config.md)
- [Expo EAS Update documentation](https://docs.expo.dev/eas-update/introduction/)
- [Pushy OTA documentation](https://pushy.reactnative.cn/)
- [better-auth Expo integration](https://www.better-auth.com/docs/integrations/expo)
- [TanStack Query React installation](https://tanstack.com/query/latest/docs/framework/react/installation)
- [TanStack Form React quick start](https://tanstack.com/form/latest/docs/framework/react/quick-start)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, TypeScript snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to scaffold an Expo project, install packages, fetch current documentation, install remote AI skills, and generate Apple OAuth client-secret text.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
