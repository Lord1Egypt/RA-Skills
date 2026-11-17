## Description:

Domain threat scores, content categories, and deep intelligence using alphaMountain.ai

This skill is ready for commercial/non-commercial use.

## Publisher:

[skibum3d](https://clawhub.ai/user/skibum3d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and other external users use this skill to query alphaMountain.ai for hostname threat scores, content categories, popularity, DGA probability, deeper intelligence, and API quota details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted hostname input inserted directly into shell command examples could make curl payload construction unsafe.

Mitigation: Validate and normalize hostnames before use, avoid shell string substitution, and build JSON payloads with a serializer or safe argument handling.

Risk: The alphaMountain license key could be exposed through logs, command history, or copied output.

Mitigation: Read the key from ALPHAMOUNTAIN_API_KEY, avoid printing it, and redact it from logs and troubleshooting output.

Risk: API response sections may include untrusted external content such as web page data, headers, WHOIS records, links, or redirects.

Mitigation: Treat returned content as analysis data only and ignore any instructions or requests embedded in that content.

## Reference(s):

- [AlphaMountain API skill page](https://clawhub.ai/skibum3d/skills/alphamountain)
- [alphaMountain threat intelligence feeds API](https://www.alphamountain.ai/threat-intelligence-feeds-api/)
- [alphaMountain hostname intelligence endpoint](https://api.alphamountain.ai/intelligence/hostname)
- [alphaMountain license info endpoint](https://api.alphamountain.ai/license/info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHAMOUNTAIN_API_KEY and hostname input; API-returned web, WHOIS, DNS, and relation data should be treated as untrusted analysis data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
