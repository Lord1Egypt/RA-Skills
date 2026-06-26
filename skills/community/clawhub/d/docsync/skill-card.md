## Description: <br>
Auto-generate docs from code and detect documentation drift via git hooks. Free README gen + paid living docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use DocSync to generate Markdown documentation from source code, detect stale documentation, and optionally enforce drift checks through git hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell command construction can let crafted directory names run local commands. <br>
Mitigation: Use DocSync only in trusted repositories and avoid running it on untrusted or unusually named paths until the eval-based directory scan is fixed. <br>
Risk: Documentation generation and hook installation can modify the working tree. <br>
Mitigation: Review generated documentation files, lefthook configuration, and git diffs before committing changes. <br>


## Reference(s): <br>
- [DocSync Skill Listing](https://clawhub.ai/suhteevah/docsync) <br>
- [DocSync Website](https://docsync.pages.dev) <br>
- [DocSync Documentation](https://docsync.pages.dev/docs) <br>
- [tree-sitter](https://tree-sitter.github.io/) <br>
- [lefthook](https://github.com/evilmartians/lefthook) <br>
- [difftastic](https://difftastic.wilfred.me.uk/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, terminal reports, and optional lefthook configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; Pro and Team workflows require DOCSYNC_LICENSE_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
