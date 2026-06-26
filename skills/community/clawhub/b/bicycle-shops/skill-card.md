## Description: <br>
Find nearby bicycle shops. Invoke when user asks for bike shops near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find nearby bicycle shops, bike stores, repair options, and related services from a user-provided location or city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location coordinates are required for nearby shop lookup. <br>
Mitigation: Ask for location only when needed, use trusted location providers, and avoid retaining precise coordinates beyond a short-lived lookup cache. <br>
Risk: Large or repeated lookup requests can increase privacy exposure and provider load. <br>
Mitigation: Keep radius and result limits bounded, honor the documented maximum limit, and use short-term caching for repeated location-category-radius queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/bicycle-shops) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured text describing nearby bicycle-shop lookup inputs, filters, errors, and standardized point-of-interest results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location coordinates, radius, limit, and optional filters such as open_now, min_rating, and keywords.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
