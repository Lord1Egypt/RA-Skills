## Description:

Auto Sec Blogger collects security and technology news, uses an LLM to select and draft security blog posts, publishes drafts to Notion for review, and can publish approved posts to a Git-backed blog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rebugui](https://clawhub.ai/user/rebugui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to automate security-news collection, LLM-assisted article drafting, Notion review workflows, and Git-backed blog publishing. It is intended for teams that already operate Notion and GitHub Pages or a compatible static blog workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing scripts can write blog files and push commits to a configured Git repository.

Mitigation: Test first against a disposable blog repository, require a clean working tree, and restrict staging to generated post paths before live use.

Risk: The skill depends on Notion, GitHub, and LLM credentials for automated collection and publishing.

Mitigation: Use scoped Notion and GitHub credentials, keep dotenv files outside published repositories, and rotate credentials after testing.

Risk: Background or automatic publishing can publish approved Notion entries without a separate manual command.

Mitigation: Disable scheduled or loop-based publishers until reviewed, and require explicit human approval in Notion before enabling live publishing.

Risk: Category and slug values influence filesystem paths for generated posts.

Mitigation: Validate categories against an allowlist and sanitize slugs before creating files or directories.

Risk: Mermaid rendering can invoke an unpinned external CLI dependency.

Mitigation: Pin the Mermaid CLI version and run rendering in a controlled environment before production use.

## Reference(s):

- [Architecture Reference](references/architecture.md)
- [GLM API Documentation](https://open.bigmodel.cn/dev/api)
- [Notion API Documentation](https://developers.notion.com/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [ClawHub Skill Page](https://clawhub.ai/rebugui/skills/auto-sec-blogger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, API calls, Guidance]

**Output Format:** [Markdown articles, Notion page content, Git-backed blog files, and setup or execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured LLM, Notion, and optional GitHub credentials; publishing paths can write files and push commits.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
