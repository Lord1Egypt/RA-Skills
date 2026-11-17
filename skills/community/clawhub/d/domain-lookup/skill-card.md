## Description:

一个提供全面域名研究工具（包括RDAP、WHOIS和DNS查询功能）的模型上下文协议（MCP）服务器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query domain registration, RDAP, WHOIS, DNS-related information, nameservers, contact data, and domain status through the XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the required XBY API key in a plaintext .env file.

Mitigation: Use a limited-scope key, avoid shared workspaces, verify local file permissions, and remove the .env entry when finished.

Risk: Domain lookup requests and the XBY API key are sent to XiaoBenYang's API.

Mitigation: Review the upstream service before use and avoid submitting sensitive domains unless that third-party processing is acceptable.

Risk: The source documentation contains copy-paste mismatches that may confuse reviewers about the skill's scope.

Mitigation: Review the advertised domain_lookup behavior against scripts/tools.py and the security evidence before installation.

## Reference(s):

- [XiaoBenYang API key and service site](https://xiaobenyang.com)
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/domain-lookup)
- [ClawHub publisher profile](https://clawhub.ai/user/alinklab)

## Skill Output:

**Output Type(s):** [text, API calls, configuration guidance]

**Output Format:** [Markdown or plain text summarizing JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided XBY_APIKEY before lookup requests can run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
