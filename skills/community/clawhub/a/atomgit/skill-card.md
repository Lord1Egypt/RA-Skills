## Description:

AtomGit/GitCode repository management skill for operating user, repository, issue, pull request, file, branch, organization, enterprise, webhook, member, AI, and OAuth APIs through documented curl commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and adapt AtomGit/GitCode API calls for repository administration, issue and pull request workflows, content access, organization management, and related platform operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad AtomGit/GitCode tokens can expose account and repository operations beyond the immediate task.

Mitigation: Use the narrowest available token scopes, prefer read-only access for browsing or listing, and use separate short-lived tokens for write operations.

Risk: Documented actions include deletion, repository transfer, SSH-key, collaborator, webhook, and pull-request merge operations.

Mitigation: Require explicit user confirmation before these operations and verify the target owner, repository, branch, issue, or pull request before execution.

Risk: The skill includes AI and media endpoints that may send prompts, audio, or video data to the platform.

Mitigation: Use AI or media endpoints only when intentionally requested, and avoid sending sensitive content unless the user has approved the data flow.

Risk: Some documented endpoints have known failures or unclear parameter requirements.

Mitigation: Check the current API documentation and validate parameters with low-impact requests before relying on mutating calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/atomgit)
- [GitCode API documentation](https://docs.gitcode.com/docs/apis/)
- [GitCode token management](https://gitcode.com/setting/token-classic)
- [AtomGit token management](https://atomgit.com/setting/token-classic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ATOMGIT_TOKEN credential for authenticated API calls.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
