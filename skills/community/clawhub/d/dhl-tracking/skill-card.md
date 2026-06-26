## Description: <br>
Track German DHL parcels through the dhl.de tracking API with simple HTTP requests and no API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idrs](https://clawhub.ai/user/idrs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and end users can check DHL parcel status, delivery progress, delivery windows, and event history for German DHL Paket tracking numbers. <br>

### Deployment Geography for Use: <br>
Global, with functionality scoped to German DHL parcel tracking. <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers are sent to dhl.de through an unofficial endpoint. <br>
Mitigation: Install and run the skill only when users are comfortable sending the provided DHL tracking number to dhl.de. <br>
Risk: Repeated background checks can create unnecessary polling against DHL services. <br>
Mitigation: Use cron or monitoring only intentionally, and avoid aggressive polling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/idrs/dhl-tracking) <br>
- [DHL tracking data endpoint](https://www.dhl.de/int-verfolgen/data/search) <br>
- [DHL tracking website](https://www.dhl.de/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text tracking summary, raw JSON from DHL, and markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include German status text, delivery progress, delivery window, event history, and a parsed JSON copy for programmatic use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
