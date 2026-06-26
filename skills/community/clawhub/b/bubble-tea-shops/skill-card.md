## Description: <br>
Find nearby bubble tea shops. Invoke when user asks for boba near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find nearby bubble tea shops from an authorized location or city query. It standardizes point-of-interest results and supports filters such as open status, rating, price level, and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nearby search can reveal a user's precise location when latitude and longitude are supplied. <br>
Mitigation: Ask for location permission, prefer an approximate location when exact coordinates are not needed, and avoid retaining precise coordinates. <br>
Risk: Cached location-based search results can preserve sensitive movement or neighborhood context. <br>
Mitigation: Keep any cache short-lived, scope it to the bubble tea search purpose, and discard it after it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/bubble-tea-shops) <br>
- [Publisher profile](https://clawhub.ai/user/mikeclaw007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text point-of-interest list with validation and provider error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results use a fixed bubble-tea-shops category and may include shop details filtered by radius, open status, rating, price level, keywords, and result limit.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
