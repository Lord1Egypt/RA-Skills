## Description:

Cashback helps users create cashback short links, check rebate rates, and review personal rebate orders for supported overseas brand stores through Duomai affiliate channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and agents use this skill to convert supported Adidas, Space NK NL, and designwebstore DE links into cashback links, check merchant rebate rates, and query personal cashback orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable scripts can accept broader merchant names or URLs than the documented three-merchant scope.

Mitigation: Confirm inputs are limited to Adidas, Space NK NL, and designwebstore DE before invoking scripts, and do not send unsupported merchant URLs.

Risk: Product links, merchant queries, and order lookups are sent to the feima-lab API service and require FX_AI_API_KEY plus the separately installed fx-base dependency.

Mitigation: Use the skill only when the publisher, API service, and a reviewed or version-pinned fx-base dependency are trusted; avoid URLs containing private tokens.

## Reference(s):

- [Cashback ClawHub Release](https://clawhub.ai/fangshan101-coder/skills/cashback)
- [feima-lab Open Platform](https://platform.feima.ai/)
- [feima-lab API Service](https://api-ai-brain.fenxianglife.com)
- [Link Convert Output Template](references/link-convert-output.md)
- [Order Query Output Template](references/order-query-output.md)
- [Store Rebate Output Template](references/store-rebate-output.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown responses backed by JSON API results and Node.js command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, FX_AI_API_KEY, and the separately installed fx-base skill.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
