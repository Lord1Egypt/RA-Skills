## Description: <br>
Provides zero-configuration accessible travel lookups for attractions, hotel accessibility, transportation-related tips, and personalized travel guidance using built-in data for 30+ popular Chinese attractions and major hotel brands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers, caregivers, and travel planners use this skill to check accessibility information for supported Chinese attractions and hotel brands, including wheelchair access, accessible restrooms, room features, route notes, and preparation guidance for wheelchair, visual, hearing, stroller, and elderly travel needs. <br>

### Deployment Geography for Use: <br>
Global; content coverage is focused on China. <br>

## Known Risks and Mitigations: <br>
Risk: Venue and hotel accessibility details may change after release. <br>
Mitigation: Treat results as advisory and confirm accessibility facilities, room availability, and route closures with the attraction or hotel before travel. <br>
Risk: The artifact declares an optional proxy token and includes an unused network helper, even though current tools use local data. <br>
Mitigation: Installers should keep the skill on the reviewed version and verify future releases before assuming the same local-only behavior. <br>
Risk: The skill gives elderly travel preparation notes but is not medical advice. <br>
Mitigation: Users with medical or post-operative travel concerns should follow professional medical guidance before traveling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/accessible-travel-guide) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON strings containing accessibility lookup results, availability notes, route details, booking guidance, contacts, and travel tips.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are generated from local built-in data and should be treated as advisory rather than real-time venue status.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
