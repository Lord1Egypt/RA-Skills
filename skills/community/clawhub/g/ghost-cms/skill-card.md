## Description: <br>
Ghost CMS helps agents create, publish, schedule, and manage Ghost blog content, newsletters, members, comments, analytics, media, users, and themes through the Ghost Admin API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisagiddings](https://clawhub.ai/user/chrisagiddings) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to manage Ghost CMS sites from an agent, including drafting, publishing, scheduling, subscriber and member workflows, comments, analytics, newsletters, media uploads, user administration, and theme management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Ghost Admin API authority and can perform site-changing operations. <br>
Mitigation: Install only when full Ghost Admin access is acceptable, use a staging site or dedicated integration key when possible, and review requested operations before execution. <br>
Risk: Publishing and newsletter operations can make content public or email subscribers. <br>
Mitigation: Review generated content before publishing or emailing subscribers, and prefer drafts or scheduled posts for human approval workflows. <br>
Risk: A bundled script can update a hard-coded post without confirmation. <br>
Mitigation: Avoid running update-teapot.js unless its target and behavior have been reviewed for the intended Ghost site. <br>
Risk: Exported member data or snippets may contain sensitive site or subscriber information. <br>
Mitigation: Keep exported member data and snippets outside version-controlled folders unless they have been reviewed and sanitized. <br>


## Reference(s): <br>
- [Skill Overview](SKILL.md) <br>
- [README](README.md) <br>
- [Ghost CMS Setup and Authentication](references/setup.md) <br>
- [Ghost Admin API Reference](references/api-reference.md) <br>
- [Content Management](references/content.md) <br>
- [Members and Subscribers](references/members.md) <br>
- [Newsletters](references/newsletters.md) <br>
- [Comment Management](references/comments.md) <br>
- [Analytics and Insights](references/analytics.md) <br>
- [Ghost Theme Management](references/themes.md) <br>
- [Lexical Card Types Reference](references/lexical-cards.md) <br>
- [Lexical Migration Guide](LEXICAL-MIGRATION.md) <br>
- [Ghost Snippets](snippets/README.md) <br>
- [Ghost Admin API Docs](https://ghost.org/docs/admin-api/) <br>
- [Ghost Editor Documentation](https://ghost.org/help/using-the-editor/) <br>
- [Lexical Framework](https://lexical.dev/) <br>
- [Ghost Theme Docs](https://ghost.org/docs/themes/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payloads, and Ghost Admin API operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user commands, Node.js/npm, GHOST_ADMIN_KEY, and GHOST_API_URL; operations may create, update, delete, publish, email, upload, or modify Ghost site resources.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
