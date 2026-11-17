## Description:

Routes multi-step Capgo cloud workflows across native builds, OTA releases, store publishing, and organization administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riderx](https://clawhub.ai/user/riderx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile release teams use this skill to coordinate Capgo native builds, OTA updates, store publishing, and organization setup across multiple workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to Capgo can change app releases, channels, or organization settings.

Mitigation: Use read-only or narrowly scoped access by default and require explicit approval for mutations.

Risk: Pasting Capgo API keys into chat may expose credentials.

Mitigation: Prefer OAuth or secure secret storage over sharing API keys in chat.

Risk: Running the latest CLI version may introduce unexpected changes.

Mitigation: Consider pinning the Capgo CLI version rather than using @latest.

## Reference(s):

- [Capgo Cloud skill on ClawHub](https://clawhub.ai/riderx/skills/capgo-cloud)
- [Capgo MCP documentation](https://capgo.app/docs/ai/mcp/)
- [Capgo iOS cloud build documentation](https://capgo.app/docs/cli/cloud-build/ios/)
- [Capgo Android cloud build documentation](https://capgo.app/docs/cli/cloud-build/android/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes focused work to specialized Capgo workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
