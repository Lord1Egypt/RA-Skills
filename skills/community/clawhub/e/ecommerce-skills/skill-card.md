## Description:

Helps agents remove backgrounds, restore product photos, and generate marketplace-ready ecommerce listing image sets from user-provided product images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[designkit](https://clawhub.ai/user/designkit)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketplace operators, creative operations teams, and agencies use this skill to turn provided product photos into clean cutouts, sharper product images, or listing-ready image sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses shell and network workflows with configurable API destinations.

Mitigation: Install only if you trust Designkit/OpenClaw, constrain shell execution and network destinations in the runtime, and do not set OPENCLAW_API_BASE or DESIGNKIT_WEBAPI_BASE to untrusted hosts.

Risk: Local image paths provided by a user may be uploaded for remote processing.

Mitigation: Treat provided local image paths as data that may leave the machine, and only provide images intended for Designkit/OpenClaw processing.

Risk: The release evidence warns against using an unpinned npx install path in sensitive environments.

Mitigation: Use a pinned or reviewed installation method for sensitive environments.

## Reference(s):

- [Designkit OpenClaw](https://www.designkit.com/openClaw)
- [ClawHub Skill Listing](https://clawhub.ai/designkit/skills/ecommerce-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with image result URLs or previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Designkit OpenClaw API key and processes only image URLs or local image paths explicitly provided by the user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
