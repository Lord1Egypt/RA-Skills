## Description: <br>
Save and organize web articles as bookmarks with AI summaries and auto-tagging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chliny](https://clawhub.ai/user/chliny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect URLs or article text into a local markdown bookmark library, generate concise summaries and tags, maintain an index, and optionally sync the collection to a configured GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bookmarked pages and summaries can be stored in local files, git history, and a configured GitHub repository. <br>
Mitigation: Use a dedicated ARTICLE_BOOKMARK_DIR, leave ARTICLE_BOOKMARK_GITHUB unset for local-only storage, and avoid bookmarking private, proprietary, or sensitive pages unless that storage path is acceptable. <br>
Risk: Deletion and save workflows modify markdown files and git history in the configured bookmark directory. <br>
Mitigation: Confirm article details before deletion and point ARTICLE_BOOKMARK_DIR only at the intended bookmark folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chliny/article-bookmarker) <br>
- [bookmark-script.md](references/bookmark-script.md) <br>
- [file-structure.md](references/file-structure.md) <br>
- [usage-examples.md](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown files and concise agent guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARTICLE_BOOKMARK_DIR and git; ARTICLE_BOOKMARK_GITHUB and gh enable optional private GitHub synchronization.] <br>

## Skill Version(s): <br>
0.2.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
