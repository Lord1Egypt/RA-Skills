## Description: <br>
Publishes markdown to AutEng with curl and returns shareable links for rendered documents, including documents with Mermaid diagrams, KaTeX, and code blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical writers use this skill to publish user-chosen markdown through AutEng's hosted renderer and retrieve a shareable link. It is useful for documents that include Mermaid diagrams, KaTeX, code blocks, and optional expiration metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental upload of secrets, credentials, private notes, proprietary documents, internal diagrams, regulated data, or personal information in markdown sent to AutEng. <br>
Mitigation: Review markdown before publishing, omit sensitive content unless it is intended to leave the environment, and set an expiration when appropriate. <br>


## Reference(s): <br>
- [AutEng publish markdown API endpoint](https://auteng.ai/api/tools/docs/publish-markdown/) <br>
- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/auteng-docs-curl-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands send selected markdown to AutEng and may return share_url, title, and expires_at fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
