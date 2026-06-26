## Description: <br>
Set up AweSeed SD-WAN with the desktop client and automatic cross-site networking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeeemmy](https://clawhub.ai/user/jeeemmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and IT operators use this skill to select and install the correct AweSeed SD-WAN client, sign in with an Oray account, and connect devices across locations for personal access, enterprise networking, industrial connectivity, or remote device management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AweSeed creates remote-network connectivity through devices signed in to the same Oray account, making account and device membership part of the network trust boundary. <br>
Mitigation: Install only on devices the user owns or is authorized to manage, use strong Oray account security, review Oray privacy and admin controls, and obtain organizational approval before enrolling work, industrial, production, or regulated systems. <br>
Risk: Some target platforms have multiple package variants or privileged installation paths, which can lead to incorrect package selection or unnecessary administrative actions. <br>
Mitigation: Use the official download page, API response, and platform help pages as the source of truth; choose package variants by platform and architecture, and leave protected OS password entry to the user. <br>


## Reference(s): <br>
- [AweSeed stable download page](https://pgy.oray.com/download) <br>
- [AweSeed beta download page](https://pgy.oray.com/download/beta) <br>
- [AweSeed download API template](https://clientapi.sdwan.oray.com/softwares/<software_key>?x64=<0|1>&versiontype=<stable|develop>&channel=0) <br>
- [Synology standard edition help](https://service.oray.com/question/47140.html) <br>
- [Synology accelerated edition help](https://service.oray.com/question/35980.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown with inline URLs and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include official API URLs, platform-specific package selection guidance, and user-owned installer steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
