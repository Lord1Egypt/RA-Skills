## Description: <br>
Lade den Abfallkalender fuer den Landkreis Ravensburg ueber die offizielle Athos-Webseite herunter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolf128058](https://clawhub.ai/user/wolf128058) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to download address-specific waste collection calendars for municipalities in the Ravensburg district. It supports structured ICS output for automation and PDF output when a visual calendar is needed. <br>

### Deployment Geography for Use: <br>
Germany (Ravensburg district) <br>

## Known Risks and Mitigations: <br>
Risk: The queried address is sent to the Ravensburg Athos portal during calendar lookup. <br>
Mitigation: Use the skill only when sharing that address with the portal is acceptable. <br>
Risk: Address-specific calendar files and cache metadata may be stored locally. <br>
Mitigation: Use --no-cache for fresh downloads without cache reuse, or clear ~/.cache/abfallkalender-rv when local cache history should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wolf128058/abfallkalender-rv) <br>
- [Ravensburg Athos Waste Management Portal](https://athos-onlinedienste.rv.de/) <br>
- [OpenClaw](https://openclaw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [ICS or PDF files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers ICS for agent processing; PDF is available when a visual calendar is needed. Cache entries are address-specific and expire after 7 days by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
