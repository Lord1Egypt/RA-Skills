## Description: <br>
Convert RSS or Atom feed URLs into Markdown using the bundled local converter script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myx0m0p](https://clawhub.ai/user/myx0m0p) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch a public RSS or Atom feed and produce readable Markdown, either on stdout or in a workspace-relative Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts user-provided feed URLs. <br>
Mitigation: Only provide feed URLs the user intends to contact; the bundled script validates http and https URLs and rejects localhost, private, and unsafe redirect targets. <br>
Risk: Writing output can overwrite existing Markdown files. <br>
Mitigation: Choose output paths deliberately; the bundled script restricts output to workspace-relative .md paths. <br>
Risk: Generated Markdown may contain untrusted feed content. <br>
Mitigation: Review generated Markdown before using it as trusted context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myx0m0p/feed-to-md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, text] <br>
**Output Format:** [Markdown generated from RSS or Atom feed entries, with optional shell command guidance for invoking the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write to stdout or to a workspace-relative .md file; supports item limits and short or full templates.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
