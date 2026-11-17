## Description:

Checks date availability for Ctrip Travel app presale bookings on a connected Android phone using ADB automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcqqq](https://clawhub.ai/user/zcqqq)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect logged-in Ctrip presale orders and report booking availability across a requested date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Android phone over ADB and may interact with permission or terms dialogs.

Mitigation: Run it only under close supervision and do not allow it to accept permission requests or user agreements on your behalf.

Risk: Screenshots containing booking details may be sent to the configured visual model API.

Mitigation: Use only a model provider and endpoint whose data handling policy you accept before processing order information.

Risk: Dependency risk may affect routine use.

Mitigation: Install with npm ci from the reviewed lockfile and update flagged transitive packages before regular operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zcqqq/skills/check-bookings-phone)
- [Publisher profile](https://clawhub.ai/user/zcqqq)
- [midscene.js model configuration](https://midscenejs.com/choose-a-model.html)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-order date statuses and timing summaries for the requested date range.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
