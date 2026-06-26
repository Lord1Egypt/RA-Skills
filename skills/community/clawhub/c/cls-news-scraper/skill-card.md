## Description: <br>
Extracts real-time stock-positive market news from Cailian Press (CLS), filtered by time window, sector, and event type for catalyst identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningjingzhiyuande](https://clawhub.ai/user/ningjingzhiyuande) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to collect CLS market news, identify stock-positive catalysts, and prepare structured rows for downstream scoring or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-news catalyst extraction can be mistaken for investment advice or acted on without sufficient verification. <br>
Mitigation: Treat outputs as research support, verify important items against primary sources, and apply independent judgment before using them in decisions. <br>
Risk: Configured CLS endpoints or sources may be incorrect, unauthorized, or inconsistent with applicable terms. <br>
Mitigation: Confirm the configured endpoint or source is legitimate and compliant with relevant terms before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningjingzhiyuande/cls-news-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table or structured rows containing ticker, company, catalyst, source URL, timestamp, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for downstream filtering, scoring, and human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
