## Description: <br>
On-demand German public-media documentary picks filtered against a personal profile, delivered via the configured output channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arturites](https://clawhub.ai/user/arturites) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to get four German-language documentary recommendations from recent public-media listings, filtered by a local personal profile and delivered through their configured output channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores viewing interests and avoidance preferences in PROFILE.md. <br>
Mitigation: Do not put secrets or highly sensitive personal details in the profile, and review the file before relying on recommendations. <br>
Risk: The skill downloads a public media listing and treats listing fields as recommendation candidates. <br>
Mitigation: Use the generated JSON only as untrusted input, preserve the skill's instruction to avoid invented links, and review recommendations before forwarding them. <br>
Risk: Recommendations are sent through the user's configured OpenClaw output channel. <br>
Mitigation: Confirm the output channel is configured for the intended recipient before running the skill. <br>


## Reference(s): <br>
- [ClawHub DokuTipp release page](https://clawhub.ai/arturites/dokutipp) <br>
- [DokuTipp homepage metadata](https://github.com/arturites/DokuTipp) <br>
- [MediathekView Filmliste data source](https://liste.mediathekview.de/Filmliste-akt.xz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [German Markdown recommendations delivered through the configured OpenClaw output channel, with local JSON used as intermediate input.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reads PROFILE.md for preferences, downloads and caches the public MediathekView list under the skill data directory, and selects 4 recommendations.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
