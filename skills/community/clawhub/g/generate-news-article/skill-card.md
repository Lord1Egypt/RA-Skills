## Description: <br>
Generate individual Markdown articles from SerpAPI Google search results with images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[near2sea](https://clawhub.ai/user/near2sea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operators use this skill to turn Google search results from SerpAPI into dated Markdown article files with optional cover images and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release embeds a third-party SerpAPI key. <br>
Mitigation: Remove the bundled key, rotate it, and require users to supply their own key through environment variables or secret storage before running the skill. <br>
Risk: The script uses hard-coded local paths for the SerpAPI dependency and output directory. <br>
Mitigation: Replace hard-coded paths with workspace-relative configuration before execution. <br>
Risk: Keyword and result-count inputs are interpolated into an embedded Python heredoc. <br>
Mitigation: Avoid untrusted inputs until interpolation is fixed or validate inputs before passing them to the script. <br>
Risk: The skill downloads remote images into generated article assets. <br>
Mitigation: Disable remote image downloads or validate image sources before using generated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/near2sea/generate-news-article) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown files with YAML front matter and relative image links, plus downloaded image assets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one article per search result into a date-based output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
