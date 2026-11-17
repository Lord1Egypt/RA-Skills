## Description:

阿淼发公众号 helps agents prepare and publish WeChat Official Account articles or image-text posts from Markdown, HTML, or plain text with editorial polishing, WeChat-native formatting, quality scoring, and API or browser publishing paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmxccc](https://clawhub.ai/user/tmxccc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to turn drafted content into WeChat Official Account posts, with publishing preparation, formatting, quality checks, and either API-based draft creation or browser-assisted posting. Developers can also use the included command references to configure account credentials and run publishing or conversion scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or save content to an external WeChat Official Account.

Mitigation: Keep pre-publish confirmation enabled for live accounts and review the account, method, title, summary, images, cover status, and quality score before publishing.

Risk: Turbo or no-confirm publishing paths can reduce human review before content reaches a live account.

Mitigation: Use Turbo or no-confirm behavior only for pre-polished, low-risk drafts and avoid it for production accounts unless an operator has already reviewed the final content.

Risk: Runtime installation through `npx -y` or `curl | bash` can execute unpinned third-party code.

Mitigation: Install Bun through a trusted and pinned process before using the skill, then run the scripts with that known runtime.

Risk: WeChat AppID and AppSecret credentials are required for API publishing.

Mitigation: Store credentials outside project directories with strict permissions or a credential manager, and avoid committing EXTEND.md files that contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skills/amiao-post-to-wechat)
- [WeChat Official Accounts platform](https://mp.weixin.qq.com)
- [WeChat draft API endpoint](https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN)
- [Bun runtime install documentation](https://bun.sh/install)
- [Configuration Reference](references/config-reference.md)
- [Editorial Rules](references/editorial-rules.md)
- [FSM Workflow](references/fsm.md)
- [Quality Scoring](references/quality-scoring.md)
- [Scripts CLI Reference](references/scripts.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, generated article metadata, and publishing reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WeChat-ready HTML, saved draft metadata, quality scores, publish logs, and setup guidance depending on the selected publishing path.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
