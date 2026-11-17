## Description:

每日采集 X 平台 AI 内容，进行基础三档排名，并将选题日报写入 Obsidian，适合个人创作者快速发现内容选题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External personal creators and content operators use this skill to collect AI-related X posts, rank promising items, and maintain an Obsidian daily idea archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse a logged-in X feed during content collection.

Mitigation: Run it only after an explicit collection request and review whether the active browser session should be used for that task.

Risk: The skill writes local files into an Obsidian vault or fallback workspace path.

Mitigation: Confirm the target vault path before execution and keep backups or version control for the destination folder.

Risk: Broad SEO-related activation wording could trigger the skill for tasks that do not require X collection.

Mitigation: Use precise prompts such as collecting an AI content daily report, and avoid invoking it for general SEO advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/creator-alpha-feed-free)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown Obsidian daily reports with ranked summaries and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated reports to an Obsidian vault path and may fall back to a workspace mirror if the vault is not writable.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
