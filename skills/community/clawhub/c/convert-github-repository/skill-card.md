## Description:

Converts GitHub repository content and metadata from a GitHub URL or local repository path into Markdown documentation, JSON metadata, CSV issue and pull request exports, folder-tree JSON, or structured README JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a GitHub repository or local git checkout and export its structure, files, issues, pull requests, releases, and README content into structured documentation or data formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository exports can include sensitive code, issues, pull requests, or release content.

Mitigation: Use a least-privilege GitHub token and review generated exports before sharing or publishing them.

Risk: Generated files may overwrite important local data if written to an unsafe output location.

Mitigation: Choose a dedicated output directory and inspect the conversion manifest for skipped and converted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/convert-github-repository)
- [Source metadata](https://github.com/MiniMax-AI/skills)
- [Reference index](references/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated repository exports in Markdown, JSON, CSV, or folder-tree JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a conversion manifest with converted and skipped file counts, skipped reasons, total size, and output path.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
