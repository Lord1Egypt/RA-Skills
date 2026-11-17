## Description:

Helps agents structure content and create Feishu documents for technical documentation, plans, reports, notes, articles, novels, and similar document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tc1993](https://clawhub.ai/user/tc1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill when an agent needs to turn user-provided content into a structured Feishu document, including long-form documents that require segmentation, retries, and completion reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises real Feishu document creation, but the packaged script only simulates success and returns a Feishu-looking link.

Mitigation: Verify that the installed version calls a real authenticated Feishu API or approved Feishu tool and fails clearly when document creation cannot be verified.

Risk: Using the skill may send document content to Feishu, which can expose sensitive information if destination, permissions, or verification behavior are unclear.

Mitigation: Use it only for content intended for Feishu and avoid sensitive documents until the destination, access permissions, and post-creation verification are confirmed.

## Reference(s):

- [Feishu API Guide](references/feishu_api_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/tc1993/skills/create-feishu-doc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python snippets and JSON-style status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a Feishu document identifier, document link, append results, and verification status when backed by a real authenticated Feishu integration.]

## Skill Version(s):

1.0.8 (source: server release evidence, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
