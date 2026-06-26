## Description: <br>
Performs lightweight defensive red-team reviews of AI workflows, focusing on misuse paths, boundary failures, and data leakage risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI engineers use this skill to review AI workflow descriptions, permission boundaries, and inputs and outputs for misuse paths, boundary failures, data risks, and mitigation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit workflow may read file contents from user-supplied paths, which can expose secrets or sensitive data in generated reports. <br>
Mitigation: Run it only on intended workspace paths, avoid system roots and sensitive directories, and inspect reports before sharing them. <br>
Risk: A defensive red-team workflow can become unsafe if prompts drift toward executable attack steps or destructive system changes. <br>
Mitigation: Keep outputs limited to review-only analysis, dry-run checklists, and mitigations; do not request or provide destructive scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/ai-workflow-red-team-lite) <br>
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured sections and optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review-oriented findings and checklists; script-based runs should be reviewed before acting on or sharing the output.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
