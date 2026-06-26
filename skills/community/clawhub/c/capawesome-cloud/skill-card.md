## Description: <br>
Guides agents through setting up and using Capawesome Cloud for Capacitor native builds, live updates, app-store publishing, and CI/CD workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robingenz](https://clawhub.ai/user/robingenz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Capawesome Cloud for Capacitor apps, including signed iOS and Android builds, over-the-air live updates, app-store submissions, and CI/CD automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers workflows that use Apple, Google, CI, keystore, certificate, service-account, and live-update signing materials. <br>
Mitigation: Use secret managers or masked CI variables, avoid pasting secrets into chat or shell history, and rotate any exposed credentials. <br>
Risk: Deployment, deletion, live-update upload, and commands using --yes can affect production apps or users. <br>
Mitigation: Before execution, explicitly confirm the app, channel, destination, track, build, and whether the action affects production users. <br>
Risk: Live updates can ship incompatible web changes or reload an app unexpectedly if not scoped and tested. <br>
Mitigation: Use versioned channels or versioned bundles, enable rollback protection where appropriate, test on the intended native version, and ask for user consent before reloads. <br>


## Reference(s): <br>
- [Native Builds](references/native-builds.md) <br>
- [Live Updates](references/live-updates.md) <br>
- [App Store Publishing](references/app-store-publishing.md) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Build Configuration](references/build-configuration.md) <br>
- [Environments](references/environments.md) <br>
- [Android Signing Certificates](references/certificates-android.md) <br>
- [iOS Signing Certificates](references/certificates-ios.md) <br>
- [Live Update Configuration](references/live-update-configuration.md) <br>
- [Live Update CI/CD Integrations](references/live-update-ci-cd-integrations.md) <br>
- [Capawesome Cloud Console](https://console.cloud.capawesome.io) <br>
- [Trapeze](https://trapeze.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent guidance may include Capawesome CLI commands, Capacitor configuration snippets, CI/CD examples, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
