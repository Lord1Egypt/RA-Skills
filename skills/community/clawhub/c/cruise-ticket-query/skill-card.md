## Description:

长江三峡游轮和城市游船船票查询，含价格、航线方向和退改政策，并提供去码头交通、景点门票和住宿推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to look up domestic river and city cruise ticket options, compare route details and prices, plan transport to cruise terminals, and find nearby attractions or hotels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise searches, origin and destination locations, and hotel preference text are sent to cloud proxy services and downstream travel or map providers.

Mitigation: Use the skill only with travel details appropriate for those services, and avoid entering unnecessary sensitive personal information.

Risk: Marketing text mentions multi-platform comparison, while the inspected code primarily shows Tuniu-oriented travel data and Gaode transport data.

Mitigation: Treat results as lookup guidance rather than exhaustive cross-platform comparison, and verify important prices, availability, and booking terms on the linked provider pages.

Risk: Ticket prices, availability, route times, and estimated transport costs can change after the skill returns results.

Mitigation: Confirm live details before booking or traveling, especially for time-sensitive departures or same-day transit plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/cruise-ticket-query)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with travel result lists, estimated transport details, and booking or navigation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live proxy services and downstream travel or map providers; prices, availability, travel times, and links may change.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
