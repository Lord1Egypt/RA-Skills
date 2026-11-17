## Description: <br>
AI Doc LITE helps agents assess long commercial documents, extract core claims and logic, and identify basic risks such as ambiguity, contradictions, and undefined terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business reviewers use this skill to prepare contract reviews, summarize memoranda, and organize long-document analysis before human decision-making. It provides analysis support and does not replace licensed legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file-write authority for document-analysis workflows. <br>
Mitigation: Run it in a restricted workspace, review proposed commands before execution, and grant file-write access only to intended output paths. <br>
Risk: The skill may handle commercial contracts, memoranda, callback URLs, credentials, or other confidential inputs. <br>
Mitigation: Avoid providing confidential documents, credentials, or callback URLs unless the publisher clarifies what data can be sent externally and how it is protected. <br>
Risk: The skill provides legal-adjacent risk analysis but states that it does not replace licensed legal advice. <br>
Mitigation: Use outputs for review preparation only and have qualified counsel confirm legal effect, compliance, and signing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page: ai-assistant-free](https://clawhub.ai/thcjp/skills/ai-assistant-free) <br>
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown text with structured document assessment, core logic, and risk sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose command execution, file reads, file writes, callback usage, or external API activity depending on the agent environment.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
