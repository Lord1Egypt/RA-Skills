## Description: <br>
Generates pre-signed URLs for Bytedance TOS `doc-preview` processing to preview and convert documents to PDF, images (PNG/JPG), or HTML, and to export page ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Bytedance TOS document-preview URLs, convert stored documents into PDF, image, or HTML previews, query page counts, and export page ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TOS credentials, security tokens, pre-signed URLs, preview links, and decoded preview URLs can grant temporary access to documents. <br>
Mitigation: Use temporary or least-privilege TOS credentials, avoid pasting secrets into chat or shell history, and treat generated links and tokens as temporary passwords. <br>
Risk: Batch export can write converted pages to a destination TOS bucket and object path. <br>
Mitigation: Verify the destination bucket and object prefix before running export workflows, especially when using `x-tos-save-bucket` or `x-tos-save-object`. <br>
Risk: The `--direct-url` mode fetches a user-provided URL without generating it from the configured TOS client. <br>
Mitigation: Use `--direct-url` only with exact, trusted document-preview URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-tos-doc-process) <br>
- [README](README.md) <br>
- [Reference](REFERENCE.md) <br>
- [Workflows](WORKFLOWS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide execution of scripts that produce local preview files or JSON batch-export responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
