## Description: <br>
Fetches and filters official CNINFO disclosures by event type and industry to extract positive catalysts for A-share monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningjingzhiyuande](https://clawhub.ai/user/ningjingzhiyuande) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, researchers, and agents use this skill to monitor official CNINFO announcements for selected A-share catalysts and return normalized fields for alerting or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Announcement fields such as trigger price, confidence, and invalidation condition may be mistaken for trading instructions. <br>
Mitigation: Treat these fields as research aids only, verify the official disclosure source, and avoid automated trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningjingzhiyuande/cninfo-announcement-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured rows containing ticker, company, catalyst, source URL, timestamp, confidence, trigger price, and invalidation condition.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses official disclosure links only and excludes auto-trade instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
