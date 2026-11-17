## Description:

本机公网IP与归属地查询，通过 ip-api.com 公共接口获取公网 IP、归属地、运营商、经纬度等信息

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunwebgo](https://clawhub.ai/user/sunwebgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check the current device's public exit IP address, approximate network location, ISP, organization, coordinates, and time zone. It can also answer the same questions for a user-specified IP address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party IP lookup service receives the user's public exit IP and returns approximate network-location details.

Mitigation: Activate the skill only for explicit IP or network-location requests, and disclose that results come from a third-party lookup service.

Risk: The primary documented endpoint uses HTTP, which can expose lookup traffic to transport-layer interception or modification.

Mitigation: Prefer an HTTPS-only lookup source when available, or treat HTTP lookup results as low assurance.

Risk: Geolocation and ISP data may be approximate, especially for VPN, proxy, or hosting-provider exit nodes.

Mitigation: Present results as network exit information rather than a precise physical location.

## Reference(s):

- [custom-ipconfig ClawHub Skill Page](https://clawhub.ai/sunwebgo/skills/custom-ipconfig)
- [Publisher Profile](https://clawhub.ai/user/sunwebgo)
- [ip-api.com JSON endpoint](http://ip-api.com/json/)
- [ipapi.co JSON endpoint](https://ipapi.co/json/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Concise structured Chinese text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses at most one lookup per conversation and does not expose raw JSON in the final response.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
