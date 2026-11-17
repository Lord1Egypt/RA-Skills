## Description:

Manage Docker stacks via Portainer API. v2.41 compatible: preserves env vars during redeploy. Claw stack uses one-shot redeployer; other stacks via PUT update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaixi](https://clawhub.ai/user/zaixi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Docker stacks through Portainer, including pulling images, restarting the gateway container, and redeploying Claw or other configured stacks while preserving environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has strong Portainer control over the configured Docker endpoint.

Mitigation: Use a narrowly scoped Portainer API key where possible and install only when that level of Docker control is acceptable.

Risk: The security guidance flags hard-coded .env loading and credential-handling concerns.

Mitigation: Review or remove the hard-coded .env loading before use and rotate any Portainer key previously used with this implementation.

Risk: The security guidance flags helper-container key exposure and ng-agent deletion behavior during update.

Mitigation: Avoid running update until those behaviors are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaixi/skills/claw-stack-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for invoking the bundled Portainer management script; the script itself performs Portainer API calls when run with configured credentials.]

## Skill Version(s):

5.1.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
