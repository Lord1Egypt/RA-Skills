## Description:

Creates concise, emotionally aware micro-vacation plans for business travelers using location, time of day, nearby POIs, Amap navigation links, and Xiaohongshu discovery cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

Business travelers and travel-assistant agents use this skill to turn sparse context such as city, hotel, landmark, current time, and travel deadlines into one actionable nearby outing. It is designed for short leisure windows around meetings, evenings, layovers, and hard-deadline airport or rail departures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may control a logged-in local Chrome session for Xiaohongshu discovery.

Mitigation: Review before installing, prefer a separate browser profile, and only enable browser automation when the account/session exposure is acceptable.

Risk: The skill may send user locations and destination searches to third-party map services.

Mitigation: Avoid sharing sensitive exact addresses when not needed, verify generated routes in the map app, and adjust the starting point manually if it is approximate.

Risk: The skill saves travel preferences and history by default.

Mitigation: Opt out of memory logging when supported and remove sensitive or unwanted entries from the local standups memory file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/bleisure-micro-vacation)
- [Intent triage workflow](artifact/references/intent-triage.md)
- [Output template](artifact/references/output-template.md)
- [Time context rules](artifact/references/time-context.md)
- [Hard-deadline travel checklist](artifact/references/deadline-travel.md)
- [Amap POI search workflow](artifact/references/amap-poi-search.md)
- [Amap navigation URI workflow](artifact/references/amap-navigation-uri.md)
- [Amap URI API route documentation](https://lbs.amap.com/api/uri-api/guide/travel/route)
- [Xiaohongshu CDP workflow](artifact/references/xiaohongshu-cdp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Concise Markdown itinerary with an image or discovery cue, time-aware timeline, safety note, Amap navigation URI, and Xiaohongshu links or keywords.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local browser automation for Xiaohongshu discovery, third-party map lookups for POI coordinates, and persistent local preference notes when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
