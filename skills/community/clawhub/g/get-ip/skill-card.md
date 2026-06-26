## Description: <br>
Get current public IP address and geolocation information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check a system's public IP address and approximate IP-based geolocation when troubleshooting network identity or answering location-related prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The lookup sends the user's public IP address to third-party IP lookup or geolocation providers. <br>
Mitigation: Confirm ambiguous location requests before running the lookup and avoid using the skill when sharing public IP information with those providers is not acceptable. <br>
Risk: IP-based geolocation can be approximate or provider-dependent. <br>
Mitigation: Present results as IP-based estimates and report which service succeeded when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qidu/get-ip) <br>
- [ipify public IP endpoint](https://api.ipify.org) <br>
- [ipinfo.io geolocation endpoint](https://ipinfo.io/) <br>
- [ifconfig.me public IP endpoint](https://ifconfig.me/) <br>
- [icanhazip public IP endpoint](https://icanhazip.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, JSON] <br>
**Output Format:** [Markdown or terminal text summarizing public IP address, approximate location, ISP, and organization when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses third-party IP lookup providers and may return provider-dependent location estimates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
