## Description:

文案去AI味服务，当用户要求"去AI化/人性化/降低AI味/改得像人写的"并希望通过小念AI后端实现而不是手动重写提示词时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yc556600](https://clawhub.ai/user/yc556600)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to humanize existing AI-generated Simplified Chinese copy, especially Xiaohongshu-style writing, by sending content to the Dashboard Console humanization API and receiving more natural text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a reusable bearer token.

Mitigation: Remove and rotate the embedded token, then require users to provide credentials through environment variables or a managed secret store.

Risk: The skill can send user text and authentication data to a configurable remote endpoint.

Mitigation: Use only trusted HTTPS service hosts, document the data handling expectations, and avoid submitting confidential, regulated, or secret-containing text unless the service is approved for that data.

Risk: Humanized output may change meaning, tone, claims, or compliance posture of the source copy.

Mitigation: Review generated copy before publication, especially for marketing, regulated, brand-sensitive, or user-facing content.

## Reference(s):

- [Dashboard Console API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/yc556600/skills/dashboard-humanize)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yc556600)
- [Dashboard Service](https://xiaonian.cc)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text by default, with optional JSON response containing the humanized title, content, AI score, and detailed result fields when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts content from stdin, a file, or command-line input; supports title, custom prompt, length, tone, purpose, language, base URL, and authentication options.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
