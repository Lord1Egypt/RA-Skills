## Description:

Content3 API for creating videos, managing content, submitting reviews, and posting to social media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimitriharding](https://clawhub.ai/user/dimitriharding)

### License/Terms of Use:


## Use Case:

Developers, creators, and content operations teams use this skill to operate the Content3 API for generating short-form videos, managing content libraries, submitting human reviews, promoting approved content, and creating social media drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a bearer API key in a plain local file.

Mitigation: Store the Content3 API key with owner-only file permissions and avoid sharing the local configuration path.

Risk: A full-access API key can grant broader permissions than a workflow needs.

Mitigation: Use separate least-privilege API keys and avoid the full-access * scope unless it is explicitly required.

Risk: The documented workflows can create public review links or publish drafts to connected social accounts.

Mitigation: Require explicit user confirmation before creating public share links or publishing social media drafts.

## Reference(s):

- [Content3 Developer Documentation](https://content3.app/developers)
- [Content3 ClawHub Skill Page](https://clawhub.ai/dimitriharding/skills/content3)
- [dimitriharding ClawHub Publisher Profile](https://clawhub.ai/user/dimitriharding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoints, JSON request bodies, and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Content3 API key and appropriate API scopes for the requested workflow.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
