## Description: <br>
Ai Assistant helps agents analyze long business, legal, proposal, and negotiation documents by extracting document purpose, core logic, assumptions, risks, version differences, and structure improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare review material for long commercial or legal documents, including risk lists, assumption checks, summaries, structure improvements, and version comparisons. It supports review preparation and decision support, but it does not replace professional legal or tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad read, write, command-execution, API, and credential-related capabilities for a document-analysis workflow. <br>
Mitigation: Install it only in an environment where file writes, API calls, credential access, and shell commands require explicit user approval or are sandboxed to non-sensitive files. <br>
Risk: The skill is intended for high-risk business and legal documents and may produce incorrect, incomplete, or overly confident analysis. <br>
Mitigation: Use outputs as review preparation only; require human review and professional counsel confirmation before relying on legal, tax, compliance, or signing decisions. <br>
Risk: Sensitive contracts, credentials, or private business documents could be exposed if the host agent grants unnecessary access. <br>
Mitigation: Avoid providing sensitive material unless the runtime enforces least-privilege file access, command restrictions, and approval gates for external API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Structured Markdown analysis with sections, tables, checklists, and recommended next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file-oriented guidance or shell-command proposals when the host agent grants those tools.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub server release metadata); artifact frontmatter lists 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
