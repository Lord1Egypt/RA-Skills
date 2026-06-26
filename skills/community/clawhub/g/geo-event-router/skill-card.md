## Description: <br>
Analyzes, classifies, scores, and routes geostrategic news events using multi-factor scoring and optional LLM semantic analysis for push decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to evaluate macro-geopolitical news, create event fingerprints, and decide whether an event should be pushed immediately, watched, or ignored. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional analyzer or market-impact modules added outside this release may process article text or make network calls. <br>
Mitigation: Review and scan any added optional modules before deployment, especially components connected to LLM analysis or market data. <br>


## Reference(s): <br>
- [ClawHub Geo Event Router release](https://clawhub.ai/liweijie0709-cmyk/geo-event-router) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [geo_event_router.py](artifact/geo_event_router.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown or structured text with Python code snippets, scoring outputs, event fingerprints, and push-decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include event type labels, numeric scores, score reasons, event IDs, fingerprints, severity labels, and optional LLM analysis summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact VERSION, and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
