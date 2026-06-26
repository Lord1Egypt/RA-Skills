## Description: <br>
IP address geolocation and network information lookup for Chinese and international IPs, IPv4, IPv6, and domain names using public endpoints without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to identify an IP address or domain's approximate location, ISP, ASN, organization, and likely proxy, mobile, or hosting status during troubleshooting or traffic review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP addresses or domains submitted for lookup are sent to public IP-information services, and the primary ip-api.com path uses HTTP. <br>
Mitigation: Avoid sensitive internal hostnames or confidential investigation targets, and prefer the HTTPS ipinfo.io path when confidentiality matters. <br>
Risk: Geolocation and proxy or hosting flags are database-backed estimates and may be inaccurate. <br>
Mitigation: Treat results as operational signals rather than definitive identity or physical-location evidence. <br>


## Reference(s): <br>
- [ClawHub China Ip skill page](https://clawhub.ai/ToBeWin/china-ip) <br>
- [ip-api.com JSON endpoint](http://ip-api.com/json/{IP}?lang=zh-CN&fields=status,message,country,regionName,city,isp,org,as,query,mobile,proxy,hosting) <br>
- [ipinfo.io JSON endpoint](https://ipinfo.io/{IP}/json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style formatted lookup summaries with optional inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize single IP, batch IP, domain, or local public IP lookup results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
