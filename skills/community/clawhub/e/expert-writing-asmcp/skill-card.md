## Description: <br>
Expert Writing ASMCP helps agents use AnyShare ASMCP to upload user-provided project files, generate a template-based outline, and produce a full professional document after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyshare-aishu](https://clawhub.ai/user/anyshare-aishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business users use this skill to turn project materials into structured professional documents such as feasibility studies, project proposals, business plans, technical plans, summaries, market research reports, product documents, annual reports, and solutions. Agents use it to manage the AnyShare document workflow, create outlines, wait for approval, and generate final Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continue processing and sharing documents without a clear fresh user confirmation. <br>
Mitigation: Require explicit user confirmation before body generation and before creating share links; remove or ignore the 5-minute auto-proceed rule. <br>
Risk: The skill requires AnyShare account access and may upload selected project files to AnyShare. <br>
Mitigation: Install only when AnyShare access is appropriate, store tokens only in mcporter configuration, verify target directories and link permissions, and avoid uploading sensitive files unless the user explicitly approves. <br>
Risk: The artifact includes an unsafe Python template-interpolation snippet in its operational guidance. <br>
Mitigation: Do not run the unsafe snippet as written; use safer structured argument construction and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyshare-aishu/expert-writing-asmcp) <br>
- [AnyShare ASMCP service](https://anyshare.aishu.cn/asmcp/) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Security checklist](SECURITY.md) <br>
- [Template catalog](templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and generated document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces outlines and full document drafts from user-provided source files and selected writing templates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
