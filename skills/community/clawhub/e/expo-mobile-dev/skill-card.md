## Description: <br>
Opinionated workflow for starting a React Native and Expo mobile app, including region-aware planning, Expo SDK scaffolding, app stack setup, AI development skill installation, and deployment guidance for international or China mainland releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to bootstrap Expo mobile apps with a deliberate choice of app name, purpose, target region, authentication, OTA, backend, and store-distribution path. It is especially useful for projects that need different decisions for international and China mainland app releases. <br>

### Deployment Geography for Use: <br>
Global, with explicit international and China mainland release paths. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow is broad enough to activate for casual mobile-app requests and may make more decisions than the user intended. <br>
Mitigation: Confirm the app name, purpose, and target region before scaffolding or applying region-specific setup. <br>
Risk: The skill can persistently install many third-party agent skills. <br>
Mitigation: Ask the user to explicitly approve or skip the AI skill installation step and review external skill sources before installation. <br>
Risk: The workflow can lead to purchases, app-store submissions, OTA publishes, metadata pushes, and cloud deployments. <br>
Mitigation: Require confirmation before EAS update or submit, metadata push, Pushy publish, paid account setup, or cloud deploy commands. <br>
Risk: The workflow handles sensitive credentials such as Apple .p8 keys, OAuth secrets, service-account JSON, SMS credentials, and app-store credentials. <br>
Mitigation: Keep secrets out of git and shared chats; store them in a secret manager or platform secret store. <br>


## Reference(s): <br>
- [App Config Patterns](references/app-config.md) <br>
- [Authentication](references/auth.md) <br>
- [Backend / API Server](references/backend.md) <br>
- [China Mainland Deployment Guide](references/china-deployment.md) <br>
- [EAS Build & Submit Recipes](references/eas-recipes.md) <br>
- [Store Presence & Metadata](references/store-presence.md) <br>
- [Apple Client Secret Generator](assets/generate-apple-client-secret.ts) <br>
- [Better Auth Expo Integration](https://www.better-auth.com/docs/integrations/expo) <br>
- [TanStack Query React Installation](https://tanstack.com/query/latest/docs/framework/react/installation) <br>
- [TanStack Form React Quick Start](https://tanstack.com/form/latest/docs/framework/react/quick-start) <br>
- [Zod Documentation](https://zod.dev/) <br>
- [Zustand Documentation](https://zustand.docs.pmnd.rs/) <br>
- [Expo EAS Update Introduction](https://docs.expo.dev/eas-update/introduction/) <br>
- [Expo EAS Metadata Schema](https://docs.expo.dev/eas/metadata/schema/) <br>
- [Expo Config Plugins](https://docs.expo.dev/config-plugins/introduction/) <br>
- [Pushy React Native Update](https://pushy.reactnative.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets, code examples, and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can propose package installs, AI skill installs, credential setup, app-store actions, OTA publishing, and cloud deployment steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
