## Description: <br>
Privacy-first personal finance tracker with local SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gowtham1984](https://clawhub.ai/user/gowtham1984) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to import local bank statement files, categorize transactions, track budgets, ask spending questions, and generate personal finance reports while keeping data on their machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank transaction history is sensitive and is stored in a local SQLite database. <br>
Mitigation: Use the skill only on trusted machines, keep the skill data directory private, and avoid importing statements on shared systems. <br>
Risk: Generated HTML reports may contain personal financial details. <br>
Mitigation: Review generated reports before sharing them and store or delete report files according to the user's privacy requirements. <br>
Risk: Custom regex categorization rules can slow local processing when patterns are complex. <br>
Mitigation: Prefer exact or keyword rules where possible and review regex rules before running bulk recategorization. <br>


## Reference(s): <br>
- [Category Guide](references/category_guide.md) <br>
- [Query Examples](references/query_examples.md) <br>
- [Supported Bank Formats](references/supported_banks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with shell command examples and report summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local JSON, text, or HTML reports through bundled scripts; user-facing responses should summarize results rather than expose raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
