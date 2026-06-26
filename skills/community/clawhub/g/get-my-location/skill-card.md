## Description: <br>
Gets current IP location info including country, province, city, and coordinates with multi-source fallback and no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etmnb](https://clawhub.ai/user/etmnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve approximate IP-based geolocation for their current network address or a specified IPv4 or IPv6 address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP-based location checks contact external geolocation services and may expose the queried IP address. <br>
Mitigation: Run the skill only when external lookups are acceptable, and avoid looking up third-party IP addresses unless there is a legitimate reason. <br>
Risk: IP geolocation results are approximate and may not reflect a user's precise physical location. <br>
Mitigation: Treat returned country, region, city, and coordinates as approximate network-location signals rather than verified physical-location data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etmnb/get-my-location) <br>
- [freegeoip.app lookup endpoint](https://freegeoip.app/json/) <br>
- [api.ipbase.com lookup endpoint](https://api.ipbase.com/v1/json/) <br>
- [ip-api.com lookup endpoint](http://ip-api.com/json/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable text or JSON from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are approximate IP geolocation data from external lookup services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
