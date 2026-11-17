## Description:

Queries parcel logistics status for major Chinese couriers, including SF Express, ZTO, YTO, Yunda, STO, J&T, JD Logistics, EMS, and others, with automatic courier detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yokiy0828](https://clawhub.ai/user/yokiy0828)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query Chinese domestic parcel shipment status from a tracking number, optionally specifying the courier code and phone suffix when required. It returns a concise timeline of the shipment state and recent logistics events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes plaintext Kuaidi100 credentials in config.json.

Mitigation: Rotate the exposed credentials before use and distribute a non-secret template or environment-based configuration instead of live keys.

Risk: The artifact includes publish_evomap.py, an unrelated publisher script that can read a home-directory EvoMap secret.

Mitigation: Remove publish_evomap.py from the distributed skill unless EvoMap publication tooling is intentionally required and reviewed.

Risk: Shipment numbers and phone suffixes may be sent to Kuaidi100 during tracking queries.

Mitigation: Give users clear notice before sending tracking identifiers or phone suffixes to Kuaidi100 and collect only the values required for the selected courier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yokiy0828/skills/express-tracking)
- [Kuaidi100](https://www.kuaidi100.com)
- [Kuaidi100 polling API endpoint](https://poll.kuaidi100.com/poll/query.do)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Formatted plain text or Markdown-like command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracking output includes courier name, tracking number, delivery state, and up to 15 recent logistics events.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
