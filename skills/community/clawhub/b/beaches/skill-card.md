## Description: <br>
Find nearby beaches when a user asks for beaches near them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer beach discovery requests from an authorized user location and return standardized POI-style results for travel planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location data can reveal sensitive user whereabouts. <br>
Mitigation: Request location only when needed, prefer approximate coordinates when possible, and avoid retaining precise location history. <br>
Risk: Beach search implementations may depend on external location or POI providers that can be unavailable or rate-limited. <br>
Mitigation: Handle provider failures and rate limits explicitly, and use short-lived caching for repeated location and category queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/beaches) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text describing nearby beach POI results, filters, and error states] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include location, radius, limit, filters, beach category, privacy guidance, and rate-limit handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
