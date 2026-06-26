## Description: <br>
AdsPower profile operation via adspower-browser CLI. open/launch/start browser or profile, environment, config profile, AdsPower; create/update/delete/list profiles; groups, tags, proxies; kernel download/list; client patch; API check-status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adspower](https://clawhub.ai/user/adspower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage AdsPower browser profiles through the adspower-browser CLI, including opening, creating, updating, deleting, listing, sharing, and closing profiles. It also helps build commands for groups, tags, proxies, browser kernels, client patches, fingerprint settings, cookies, user agents, and API status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through sensitive or destructive AdsPower profile operations, including deleting profiles, wiping cache, closing all profiles, sharing profiles, changing proxies, exporting cookies, and changing fingerprints. <br>
Mitigation: Require explicit user confirmation before those operations and review generated commands before execution. <br>
Risk: AdsPower API keys, passwords, cookies, 2FA keys, and proxy credentials may be exposed if pasted into shared logs, prompts, or transcripts. <br>
Mitigation: Use environment variables such as ADS_API_KEY where possible, redact secrets from transcripts and logs, and avoid sharing credential values with the agent unless required for the immediate task. <br>


## Reference(s): <br>
- [AdsPower Official Website](https://www.adspower.com/) <br>
- [Browser Profile Management](references/browser-profile-management.md) <br>
- [Tool Intent Map](references/tool-intent-map.md) <br>
- [Fingerprint Config](references/fingerprint-config.md) <br>
- [Proxy Management](references/proxy-management.md) <br>
- [User Proxy Config](references/user-proxy-config.md) <br>
- [Browser Tag Management](references/browser-tag-management.md) <br>
- [Group Management](references/group-management.md) <br>
- [Browser Kernel Management](references/browser-kernel-management.md) <br>
- [Application Management](references/application-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands and JSON parameter snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AdsPower profile, proxy, fingerprint, cookie, API key, and runtime command details supplied by the user.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
