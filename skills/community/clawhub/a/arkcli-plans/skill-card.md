## Description:

Helps agents manage ARK Agent Plan and Coding Plan subscriptions, team seats, model routing, and related API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account administrators use the skill to check, purchase, and renew subscriptions, manage team seats and keys, and inspect plan models or local agent harness status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that model-routing changes can affect where plan requests are directed.

Mitigation: Check the plan and available model targets, then confirm the intended route before applying a change.

Risk: The security guidance notes access to agent configuration paths, which may contain sensitive information.

Mitigation: Run local harness status checks only in a trusted environment and avoid sharing sensitive configuration contents.

Risk: Purchases and renewals can charge the account, and API-key rotation invalidates the previous key.

Mitigation: Show and obtain explicit agreement to the required terms before a purchase or renewal; after key rotation, update dependent clients and harnesses.

## Reference(s):

- [Purchase plans and agreement flow](references/arkcli-plans-buy.md)
- [Renew plans](references/arkcli-plans-renew.md)
- [Agreement signing](references/arkcli-plans-agreement-signing.md)
- [List plan models](references/arkcli-plans-model-list.md)
- [Apply a model route](references/arkcli-plans-model-apply.md)
- [List team seats](references/arkcli-plans-team-seat-list.md)
- [Assign team seats](references/arkcli-plans-team-seat-assign.md)
- [Rotate team API keys](references/arkcli-plans-team-rotate-apikey.md)
- [Rotate a personal API key](references/arkcli-plans-personal-rotate-apikey.md)
- [Check local harness status](references/arkcli-plans-harness-status.md)
- [Official Agent Plan over-quota billing guidance](https://ark.volcengine.com/region:cn-beijing/docs/agent-plan-personal-over-quota-postpaid-management)
- [Official Agent Plan model deprecation notice](https://ark.volcengine.com/region:cn-beijing/docs/agent-plan-personal-model-deprecation-announcement)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text guidance with command selection and safety checks; no standalone files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
