## Description: <br>
Fetch and analyze Concept2 Logbook workout data via API with pulse zone analysis and trend tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katla50](https://clawhub.ai/user/katla50) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Concept2 rowing, SkiErg, and BikeErg workouts, inspect heart-rate zones and pace consistency, and summarize training trends from the Concept2 Logbook API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Concept2 API tokens grant access to personal workout data if exposed. <br>
Mitigation: Use a revocable API token, pass it only through trusted shells, and avoid pasting tokens into shared logs or transcripts. <br>
Risk: JSON exports and summaries may include personal workout, heart-rate, and profile information. <br>
Mitigation: Store exports in protected locations and review them before sharing. <br>
Risk: Training recommendations may be incomplete or misleading when logbook data is stale, sparse, or missing heart-rate fields. <br>
Mitigation: Treat recommendations as informational, check data freshness, and use qualified coaching or medical advice for training or health decisions. <br>


## Reference(s): <br>
- [Concept2 Logbook API Reference](references/api-reference.md) <br>
- [Concept2 Developer Documentation](https://log.concept2.com/developers/documentation/) <br>
- [Concept2 API Keys](https://log.concept2.com/developers/keys) <br>
- [Concept2 API Validator](https://log.concept2.com/developers/validator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output can be summary text, table text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Concept2 API access token; JSON exports may contain personal workout and heart-rate data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
