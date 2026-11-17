## Description:

Ghost CMS integrates with the Ghost Admin API so agents can create, publish, schedule, and manage blog content, newsletters, members, comments, themes, snippets, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisagiddings](https://clawhub.ai/user/chrisagiddings)

### License/Terms of Use:

MIT

## Use Case:

Developers and site operators use this skill to manage Ghost CMS publishing workflows, subscriptions, comments, newsletters, analytics, themes, and local snippet libraries through agent-generated guidance and commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ghost Admin API credentials grant full site access with no read-only scope.

Mitigation: Install only for sites where full Admin API access is acceptable, use a staging site or dedicated integration key, store credentials securely, and rotate keys regularly.

Risk: Publish, delete, theme, member, and settings operations can immediately affect public content, subscribers, billing access, or site behavior.

Mitigation: Review generated commands before execution, prefer draft and scheduled workflows, save current state before destructive changes, and verify results after each operation.

Risk: The package includes scripts/update-teapot.js, which security evidence says can overwrite a hard-coded Ghost post.

Mitigation: Avoid running scripts/update-teapot.js unless it has been reviewed and adapted for the intended site and post.

Risk: Security evidence reports a theme download path validation bug that can write outside the intended directory.

Mitigation: Avoid theme download operations or constrain and review output paths until the validation issue is fixed.

## Reference(s):

- [Ghost Admin API Reference](references/api-reference.md)
- [Ghost CMS Setup & Authentication](references/setup.md)
- [Content Management](references/content.md)
- [Members & Subscribers](references/members.md)
- [Newsletters](references/newsletters.md)
- [Comment Management](references/comments.md)
- [Analytics & Insights](references/analytics.md)
- [Ghost Theme Management](references/themes.md)
- [Lexical Card Types Reference](references/lexical-cards.md)
- [Ghost Snippets Library](snippets/README.md)
- [Official Ghost Admin API Docs](https://ghost.org/docs/admin-api/)
- [Ghost CMS](https://ghost.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API operations that create, publish, update, delete, upload, or configure Ghost CMS resources.]

## Skill Version(s):

0.1.8 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
