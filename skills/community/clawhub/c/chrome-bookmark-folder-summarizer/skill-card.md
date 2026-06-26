## Description: <br>
Reads Chrome bookmarks and extracts URLs by a user-provided folder name, then generates batch webpage summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blacker521](https://clawhub.ai/user/blacker521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to extract URLs from a named Chrome bookmark folder and produce structured summaries of the saved pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads bookmark titles and URLs from the selected Chrome bookmark folder, which may expose private, work, internal, or sensitive links. <br>
Mitigation: Use exact folder matching where possible, narrow scope with non-recursive or pick-first options when appropriate, and review extracted URLs before summarizing large or sensitive folders. <br>
Risk: Summarizing bookmarked pages may require visiting external URLs and processing page content outside the local bookmark file. <br>
Mitigation: Confirm the target folder and review the URL list before fetching or summarizing pages, especially for internal or access-controlled sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blacker521/chrome-bookmark-folder-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON extraction results and structured page summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves original bookmark order and includes a cross-page comparison when summaries are generated.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
