## Description:

Helps agents preview and reorder previous Foodora orders with ordercli and track ETA/status, requiring explicit approval before placing an order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

External users use this skill to safely preview and reorder prior Foodora meals and monitor active order status through ordercli. It is intended for workflows where the user explicitly confirms before any purchase is placed.

### Deployment Geography for Use:

Foodora-supported regions; example setup uses Austria (AT).

## Known Risks and Mitigations:

Risk: The skill installs a mutable third-party ordercli release that handles Foodora account sessions.

Mitigation: Review and pin a trusted ordercli version before use, and install it only if the publisher and dependency chain are acceptable.

Risk: The skill can place purchases through Foodora when confirmation flags are used.

Mitigation: Run preview-only commands first and require explicit user confirmation before any command that places or confirms an order.

Risk: Vague prompts such as 'order food' could trigger unintended purchasing workflows.

Mitigation: Ask clarifying questions and stop at preview unless the user clearly intends to use Foodora and confirms the specific order.

## Reference(s):

- [Food Order skill page](https://clawhub.ai/steipete/skills/food-order)
- [ordercli homepage](https://ordercli.sh)
- [Foodora Austria](https://www.foodora.at/)
- [ordercli Go install module](https://github.com/steipete/ordercli/tree/main/cmd/ordercli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview details, confirmation prompts, status summaries, and ordercli commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
