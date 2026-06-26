## Description: <br>
Converts GitHub repository content and metadata from a URL or local repository into Markdown documentation, JSON metadata, CSV tables, folder tree JSON, or structured README JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to export GitHub repositories or local Git repositories into documentation, metadata, issue and pull request CSVs, and repository tree representations while preserving structure and reporting skipped files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require GitHub credentials for private repositories or higher API rate limits. <br>
Mitigation: Use a least-privilege GITHUB_TOKEN and do not embed tokens in prompts, files, or exported artifacts. <br>
Risk: Repository exports can include sensitive source files, issue content, pull request content, or metadata. <br>
Mitigation: Convert only repositories the user is authorized to handle and keep generated exports in a controlled folder. <br>
Risk: The artifact README contains stale generic API_KEY and read/write examples. <br>
Mitigation: Follow the SKILL.md GitHub-token behavior and ignore README API_KEY examples until the publisher updates them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/convert-github-repository) <br>
- [Publisher-provided source link](https://github.com/MiniMax-AI/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, shell-command guidance, and manifest-style summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes conversion manifests with converted and skipped file counts, skip reasons, and output paths; may write exported files to a controlled output folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact changelog and frontmatter use 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
