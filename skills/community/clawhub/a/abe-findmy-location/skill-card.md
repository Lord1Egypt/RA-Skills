## Description: <br>
Track a shared contact's location via Apple Find My with street-level accuracy, returning address, city, and home/work/out context from map landmarks or an AI vision fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill on macOS to query the location of a contact who already shares location through Apple Find My and return a readable address or structured JSON result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Find My location data and full-screen location screenshots. <br>
Mitigation: Use it only with appropriate consent and account access, verify the selected contact before relying on results, and delete temporary screenshots after use. <br>
Risk: Unknown-location fallback may upload screenshots containing location data to SkillBoss/HeyBoss. <br>
Mitigation: Prefer configured known locations or a local-only workflow where possible, and enable the API key only when external screenshot processing is acceptable. <br>
Risk: Hammerspoon and screen automation require broad local permissions and can click the wrong target if misconfigured. <br>
Mitigation: Grant only required macOS permissions, secure or disable the Hammerspoon click server when not needed, and manually verify automation behavior during setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abeltennyson/abe-findmy-location) <br>
- [peekaboo screen automation CLI](https://github.com/steipete/peekaboo) <br>
- [Hammerspoon automation](https://www.hammerspoon.org/) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Human-readable location string or JSON object; may include a temporary screenshot path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Find My access, Accessibility and Screen Recording permissions, and SKILLBOSS_API_KEY for vision fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
