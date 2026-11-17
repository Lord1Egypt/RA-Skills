## Description:

Publish markdown and return share links using curl. Support markdown with mermaid diagrams such as component diagrams, flowcharts, and sequence diagrams. Also supports KaTex and code blocks. AutEng will return a shareable link to the published rendered document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to publish Markdown documents to AutEng with curl and retrieve shareable rendered-document links. It is useful for documents that may include Mermaid diagrams, KaTeX, and code blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published Markdown is sent to AutEng and a shareable URL is returned, which can expose content outside the local environment.

Mitigation: Do not publish secrets, credentials, private customer data, or internal documents unless AutEng access, retention, and expiration behavior is acceptable.

Risk: A response without share_url means the publish operation may have failed or returned an unexpected payload.

Mitigation: Treat any response missing share_url as an error and inspect the full JSON body before sharing or relying on the result.

## Reference(s):

- [AutEng publish-markdown endpoint](https://auteng.ai/api/tools/docs/publish-markdown/)
- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/skills/auteng-docs-curl-publish)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl examples and jq response handling guidance for retrieving share_url and compact success payloads.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
