## Description: <br>
Searches Douyin creator accounts by keyword and returns account names, follower counts, likes, following counts, video counts, and profile links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing analysts, brands, MCNs, and e-commerce teams use this skill to discover and evaluate Douyin creator accounts for competitor research, influencer outreach, and market exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release suspicious because the script disables HTTPS certificate verification while sending REDFOX_API_KEY. <br>
Mitigation: Install only after review, prefer a fixed version that uses verified TLS, and rotate the API key if it was used on an untrusted network. <br>
Risk: The skill depends on a local REDFOX_API_KEY for access to RedFox services. <br>
Mitigation: Keep the key in environment configuration, verify its scope and revocation options, and do not place it in prompts, logs, code, or output files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-account-search) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox Hub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown table with profile links, backed by JSON results from the search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and supports paginated search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
