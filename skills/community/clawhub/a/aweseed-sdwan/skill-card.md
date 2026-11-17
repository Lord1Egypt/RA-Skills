## Description:

Set up AweSeed SD-WAN with the desktop client and automatic cross-site networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeeemmy](https://clawhub.ai/user/jeeemmy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and IT operators use this skill to install the correct AweSeed client, sign in with an Oray account, and connect devices across locations for personal access, enterprise networking, industrial connectivity, and remote management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding untrusted personal, corporate, or industrial devices to the same SD-WAN environment can expose networks or devices beyond the intended trust boundary.

Mitigation: Install and sign in only on trusted devices, avoid mixing environments without approval, and remove or revoke access for lost, retired, or untrusted devices.

Risk: Account compromise could allow unauthorized access to devices joined through the same Oray account.

Mitigation: Use a strong Oray account password and enable MFA if available.

Risk: Selecting an incorrect client package for multi-variant platforms such as Linux, NAS, or OpenWrt can lead to failed or inappropriate installation.

Mitigation: Use the official download page and API response to choose the platform-specific package instead of guessing static download URLs or filenames.

## Reference(s):

- [AweSeed official download page](https://pgy.oray.com/download)
- [AweSeed beta download page](https://pgy.oray.com/download/beta)
- [AweSeed macOS client API example](https://clientapi.sdwan.oray.com/softwares/PGY_ENT_VISITOR_MAC_LOCAL?x64=1&versiontype=stable&channel=0)
- [Synology standard edition help](https://service.oray.com/question/47140.html)
- [Synology accelerated edition help](https://service.oray.com/question/35980.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline URLs and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current download API URLs, client variant selection guidance, and installation workflow recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
