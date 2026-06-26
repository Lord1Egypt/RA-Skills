## Description: <br>
Checks whether specific IP addresses are listed as publicly exposed OpenClaw instances on the OpenClaw Exposure Watchboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhaubin](https://clawhub.ai/user/chenhaubin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and incident responders use this skill to check whether specific infrastructure IP addresses appear on the public OpenClaw Exposure Watchboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script makes many HTTPS requests to a fixed public watchboard during each lookup. <br>
Mitigation: Run it only when lookup activity to openclaw.allegro.earth is acceptable for the target IPs. <br>
Risk: A missing watchboard result is not a complete exposure assessment. <br>
Mitigation: Use the result as one public-watchboard check and pair it with normal internal exposure monitoring and remediation workflows. <br>


## Reference(s): <br>
- [OpenClaw Exposure Watchboard](https://openclaw.allegro.earth) <br>
- [ClawHub release page](https://clawhub.ai/chenhaubin/exposure-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Command-line text or JSON containing checked IPs, exposed page links, errors, and duration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script accepts one or more IPv4 addresses, optional verbose progress, and optional JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
