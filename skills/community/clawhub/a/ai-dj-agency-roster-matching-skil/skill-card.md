## Description: <br>
Run the AI DJ Agency pipeline - onboard DJs into the roster and match event organisers with qualified talent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockchain-records](https://clawhub.ai/user/blockchain-records) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External event organisers use this skill to collect event briefs and find rostered DJs by location, genre, DJ type, and budget. DJs use the intake flow to consent to being recorded in a local roster for booking outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The roster stores DJ names, locations, availability, fee ranges, and contact handles locally. <br>
Mitigation: Collect only consented contact details, keep the roster private or encrypted, and avoid committing it unless that is intended. <br>
Risk: City and country lookups may be sent to Nominatim for geocoding. <br>
Mitigation: Use the matcher only when external geocoding is acceptable, and review whether location lookup disclosure is needed for the deployment. <br>
Risk: The skill requires replies to include social and Discord calls to action. <br>
Mitigation: Remove or adapt the calls to action if they do not fit the operator's communications policy or user expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blockchain-records/ai-dj-agency-roster-matching-skil) <br>
- [Nominatim geocoding endpoint](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON candidate output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper creates and reads local roster and geocache JSON files under data/ when commands are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
