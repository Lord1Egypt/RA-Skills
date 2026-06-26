## Description: <br>
Fetches Yahoo Finance crude oil and gold futures data, detects threshold-based market moves, and maps those moves to geopolitical-event market impact context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to add commodity-price context to geopolitical-event monitoring workflows, including oil and gold thresholds, sector impact descriptions, and event bonus scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance to fetch commodity prices. <br>
Mitigation: Use it only in environments where outbound requests to Yahoo Finance are acceptable. <br>
Risk: Market-impact descriptions may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational context and require human review before important financial or operational decisions. <br>
Risk: Server-resolved provenance is unavailable for this version. <br>
Mitigation: Weigh the limited publisher provenance and review the artifact before relying on it in important workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/geo-market-impact-mapper) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/CL=F) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python objects and dictionaries with short text descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts Yahoo Finance for commodity prices; market-impact output is informational context, not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact VERSION constant, and SKILL.md version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
