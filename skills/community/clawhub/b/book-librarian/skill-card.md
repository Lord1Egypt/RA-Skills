## Description: <br>
Manage reading life: recommend books, track reads, move wishlist to library, and suggest what to read next based on mood. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perplexingperfectionist](https://clawhub.ai/user/perplexingperfectionist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal reading companion to track owned and wanted books, log reading progress, and receive mood- and taste-based recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local reading history, taste preferences, and wishlist records in workspace files. <br>
Mitigation: Review or delete the generated books and memory files if that history should not be retained. <br>
Risk: New-book recommendations may use web search and can surface suggestions that are inaccurate, outdated, or unsuitable. <br>
Mitigation: Review recommendations before acting on them, especially before buying books or adding them to a library. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perplexingperfectionist/book-librarian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with CSV and Markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local book-tracking CSV files and memory/library.md after user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
