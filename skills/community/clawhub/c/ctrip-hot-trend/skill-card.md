## Description: <br>
Summarizes public Ctrip hotel, flight, and itinerary pages for lightweight travel analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to summarize public Ctrip hotel lists, compare flight prices and schedules, and generate lightweight itinerary summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use on login-protected, booking, payment, CAPTCHA, or control-bypass flows could violate platform rules or user expectations. <br>
Mitigation: Use the skill only for public Ctrip pages and do not use it for account activity, booking, payment, CAPTCHA handling, platform-control bypass, or API reverse engineering. <br>
Risk: Bulk or automated scraping could create compliance and platform-abuse risk. <br>
Mitigation: Keep use lightweight, apply frequency controls, and avoid large-scale collection. <br>
Risk: Travel prices and availability can change after collection. <br>
Mitigation: Treat results as point-in-time summaries and include the collection time when reporting price or inventory information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/ctrip-hot-trend) <br>
- [Ctrip homepage](https://www.ctrip.com/) <br>
- [Ctrip hotels](https://hotels.ctrip.com/) <br>
- [Ctrip flights](https://flights.ctrip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Include source page links and collection time when summarizing prices or availability.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
