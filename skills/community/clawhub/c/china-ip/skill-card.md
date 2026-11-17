## Description:

China Ip looks up geographic location, ISP, network details, and proxy or hosting indicators for Chinese and international IP addresses, IPv6 addresses, and domain names using public lookup endpoints without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support teams use this skill to investigate IP addresses or domains, summarize location and network ownership, identify likely private or reserved addresses, and flag proxy, VPN, mobile, or hosting indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup values may be unsafe if untrusted IP addresses or domains are interpolated into shell command strings.

Mitigation: Validate each lookup value as an IP address or safe hostname and pass it to curl as a literal argument rather than through shell string interpolation.

Risk: The primary ip-api.com lookup path uses plain HTTP, which can expose non-sensitive lookup values or be modified in transit.

Mitigation: Prefer the HTTPS ipinfo.io path when possible and avoid using the skill for sensitive IP or domain lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-ip)
- [ip-api.com JSON endpoint](http://ip-api.com/json/{IP}?lang=zh-CN&fields=status,message,country,regionName,city,isp,org,as,query,mobile,proxy,hosting)
- [ip-api.com batch endpoint](http://ip-api.com/batch?lang=zh-CN)
- [ipinfo.io JSON endpoint](https://ipinfo.io/{IP}/json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted lookup summaries with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public IP lookup APIs with curl, fall back to offline IP segment heuristics, and summarize results for single or batch lookups.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
