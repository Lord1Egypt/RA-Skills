## Description:

Provides agent guidance for using the adspower-browser CLI to operate AdsPower browser profiles, groups, tags, proxies, browser kernels, client patches, and API status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adspower](https://clawhub.ai/user/adspower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn AdsPower profile-management requests into adspower-browser CLI commands for opening profiles, managing groups, tags, proxies, cookies, fingerprints, kernels, patches, and API availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on real AdsPower profiles, cookies, proxies, account credentials, and profile-sharing targets.

Mitigation: Install only when the adspower-browser package and publisher are trusted, and require explicit confirmation before cookie export, profile sharing, profile deletion, cache clearing, close-all, or other account-impacting operations.

Risk: API keys and credentials may be exposed when passed directly in command-line arguments or JSON payloads.

Mitigation: Prefer environment variables or other secret-handling mechanisms, avoid putting API keys in shell history, and redact sensitive values from logs or shared transcripts.

Risk: Profile update, delete, cache-clear, proxy, and fingerprint commands can make persistent changes to browser environments.

Mitigation: Review target profile IDs, group IDs, proxy IDs, and command JSON before execution, and use list or status commands first when identifiers are uncertain.

## Reference(s):

- [AdsPower Official Website](https://www.adspower.com/)
- [Tool Intent Map](references/tool-intent-map.md)
- [Browser Profile Management](references/browser-profile-management.md)
- [Group Management](references/group-management.md)
- [Application Management](references/application-management.md)
- [Proxy Management](references/proxy-management.md)
- [Browser Tag Management](references/browser-tag-management.md)
- [Browser Kernel Management](references/browser-kernel-management.md)
- [Client Patch Management](references/client-patch-management.md)
- [User Proxy Config](references/user-proxy-config.md)
- [Fingerprint Config](references/fingerprint-config.md)
- [Browser Kernel Config](references/browser-kernel-config.md)
- [Browser Kernel Download Management](references/browser-kernel-download-management.md)
- [UA System Version](references/ua-system-version.md)
- [Chrome TLS Cipher Suites](references/chrome-tls-cipher.md)
- [Country Code](references/country-code.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI aliases, command parameters, profile identifiers, proxy settings, fingerprint settings, API-key handling guidance, and confirmation prompts for risky operations.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
