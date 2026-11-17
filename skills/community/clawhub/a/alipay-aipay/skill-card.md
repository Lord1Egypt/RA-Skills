## Description:

Assists developers and merchant integration teams with Alipay AI pay-per-use, AI web payment, and AI mobile payment integration and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alipay](https://clawhub.ai/user/alipay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and merchant integration teams use this skill to plan, implement, and validate supported Alipay AI payment products, including pay-per-use, web payment, mobile app payment, sandbox setup, and product onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update itself from npm during use.

Mitigation: Review the installed version and changelog before use, and allow network-based updates only in environments where that update path is acceptable.

Risk: The skill can install or refresh Alipay CLI tooling and use the active Alipay CLI login or session state.

Mitigation: Run it in a controlled workspace, confirm the intended Alipay account and app before acting, and avoid sharing production credentials unless the workflow requires them.

Risk: The skill can modify Alipay app, service, or signing records as part of onboarding flows.

Mitigation: Use sandbox or test resources first when possible, review each requested change, and verify the target app and service records before production changes.

Risk: The skill can send host-linked telemetry unless disabled with documented environment variables.

Mitigation: Disable telemetry through the documented environment variables when organizational policy or user preference requires it.

## Reference(s):

- [Alipay Open Platform](https://open.alipay.com/)
- [Payment integration flow](references/integration/flow.md)
- [Product onboarding flow](references/onboarding/flow.md)
- [Sandbox setup guide](references/integration/modules/sandbox/sandbox-setup-guide.md)
- [Interface guide](references/integration/modules/interface-guide.md)
- [Runtime entry](references/runtime-entry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide changes to user projects and Alipay payment configuration when the user authorizes an integration or onboarding flow.]

## Skill Version(s):

1.7.0 (source: evidence.release.version and artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
