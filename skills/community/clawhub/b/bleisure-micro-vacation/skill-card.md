## Description: <br>
Helps business travelers turn a city, hotel, landmark, or travel deadline into a short, emotionally aware micro-vacation plan with timing, routing, safety notes, and local discovery cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees on business travel use this skill to convert limited location and time context into one concise nearby outing. It is intended for hotel-area walks, evening decompression, meal or drink ideas, deadline-aware travel plans, and navigation-ready recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party map lookups and social search can expose location, travel intent, or destination preferences to external services. <br>
Mitigation: Share only the minimum location detail needed, review generated links before opening them, and prefer keyword-only discovery when privacy is more important than direct links. <br>
Risk: Optional logged-in browser automation through a local CDP proxy can act through an active browser profile. <br>
Mitigation: Use a separate browser profile for CDP mode, avoid enabling remote debugging on a primary profile, or keep Xiaohongshu discovery in keyword-only mode unless the setup is trusted. <br>
Risk: The skill may keep local travel-history notes in standups.md. <br>
Mitigation: Review, redact, rotate, or delete saved notes, and avoid storing sensitive exact addresses, identity details, or private itinerary information. <br>
Risk: Nightlife, walking, and travel recommendations can become stale or unsafe as hours, routes, and local conditions change. <br>
Mitigation: Check current opening hours and route conditions, prefer public and well-lit areas, and treat generated plans as suggestions rather than guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keyikoi/bleisure-micro-vacation) <br>
- [Intent triage workflow](references/intent-triage.md) <br>
- [Output template](references/output-template.md) <br>
- [Time context rules](references/time-context.md) <br>
- [Deadline travel checklist](references/deadline-travel.md) <br>
- [Amap POI search workflow](references/amap-poi-search.md) <br>
- [Amap navigation URI workflow](references/amap-navigation-uri.md) <br>
- [Amap URI API travel route documentation](https://lbs.amap.com/api/uri-api/guide/travel/route) <br>
- [Xiaohongshu CDP workflow](references/xiaohongshu-cdp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with image links or search cues, a concise timeline, Amap navigation URI links, Xiaohongshu links or keywords, and short safety notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append local travel preference notes to standups.md; uses current time, web or Amap POI results, an optional Amap API key, and optional Xiaohongshu browser automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
