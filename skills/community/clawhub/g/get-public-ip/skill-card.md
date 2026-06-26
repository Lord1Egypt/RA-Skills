## Description: <br>
Checks the machine's public egress IP across domestic and international network environments, automatically switching to the fastest reachable lookup service with timeout protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regexl](https://clawhub.ai/user/regexl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to ask an agent to retrieve the current public egress IP and report the source service and elapsed time, with fallback across multiple lookup endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests to public IP lookup services disclose the user's public IP and normal request metadata to those services. <br>
Mitigation: Use the skill only when public IP lookup is intended and the user is comfortable contacting the listed services. <br>
Risk: Network failures or blocked lookup services can prevent a result. <br>
Mitigation: The skill uses multiple endpoints with per-node timeout protection and reports failure when no endpoint returns a valid IP. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/regexl/get-public-ip) <br>
- [ip.sb public IP endpoint](https://ip.sb) <br>
- [ipip.net public IP endpoint](https://myip.ipip.net) <br>
- [icanhazip public IP endpoint](https://icanhazip.com) <br>
- [httpbin IP endpoint](https://httpbin.org/ip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text status message with the detected public IP, lookup source, and elapsed time] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses timeout-bounded outbound requests to public IP lookup services and validates IP format before reporting a result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
