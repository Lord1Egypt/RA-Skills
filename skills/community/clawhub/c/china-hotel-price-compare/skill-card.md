## Description:

先浏览再比价，TourMind+途牛+同程+美团+RollingGo五源并发比价，找出全网最低价。含评分、距离、早餐、取消政策等详细信息。暑期出行多平台比价，轻松找到最划算的住宿方案

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to browse hotels in Chinese cities, filter by area, point of interest, budget, and rating, then compare prices for a selected hotel across multiple travel platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches, dates, locations, and point-of-interest preferences are sent through publisher-operated cloud proxies.

Mitigation: Review the publisher proxy data flow before use and avoid submitting travel details unless that routing is acceptable.

Risk: The release ships a shared proxy token directly in its code.

Mitigation: Treat the proxy path as a third-party trust boundary and review the skill before installing or distributing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/china-hotel-price-compare)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with hotel lists, prices, comparison summaries, warnings, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-time prices, ratings, distances, breakfast and cancellation details, and external booking links; prices can change.]

## Skill Version(s):

4.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
