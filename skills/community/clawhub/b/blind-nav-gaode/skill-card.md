## Description: <br>
BlindNav Assistant helps blind, low-vision, and mobility-impaired users use Gaode map services for voice-first location lookup, nearby-place search, accessible-facility search, walking and transit route planning, and SOS location assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukongmazi](https://clawhub.ai/user/wukongmazi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who rely on speech-first navigation can ask an agent for their current location, nearby services, accessible facilities, walking directions, public-transit options, or emergency location assistance. The skill is intended for accessible travel workflows where concise TTS-ready output is more useful than raw map data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses precise live location and sends coordinates to Gaode map services for navigation and place search. <br>
Mitigation: Install only with clear user consent for live-location use, provide the required GAODE_API_KEY only in intended deployments, and limit use to contexts where external map-service processing is acceptable. <br>
Risk: The SOS flow can process precise location on broad help phrases without a clear confirmation step. <br>
Mitigation: Review or disable SOS behavior unless the user has intentionally opted into immediate emergency location sharing; add a confirmation step when the deployment requires explicit consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wukongmazi/blind-nav-gaode) <br>
- [Publisher profile](https://clawhub.ai/user/wukongmazi) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON strings containing TTS-oriented voice_friendly, voice_summary, or voice_alert text for agent narration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GAODE_API_KEY and user location inputs; outputs are optimized for speech and should not be read as raw JSON to end users.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
