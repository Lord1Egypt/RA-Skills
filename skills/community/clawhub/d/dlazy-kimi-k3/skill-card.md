## Description:

Moonshot AI thinking model with text, image, and video understanding, suited to complex analysis, coding, and writing that needs long reasoning chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can call Kimi K3 through the dLazy CLI for complex analysis, coding, and writing, including prompts that use images or videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an external CLI and requires API authentication; scanner review could not inspect the package's internal behavior or establish its connection to the advertised model.

Mitigation: Review the CLI package before installation, use a scoped and revocable API key, and avoid sending sensitive prompts or media unless the service is approved.

## Reference(s):

- [CLI repository listed in the skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Text, Code, JSON]

**Output Format:** [JSON response envelope containing generated output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a prompt with optional images (up to 10) or videos (up to 8); asynchronous requests may return a task ID.]

## Skill Version(s):

1.2.39 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
