## Description: <br>
Documents solved problems for team reuse by capturing resolved issues, lessons learned, post-mortems, knowledge-base entries, and searchable debugging knowledge for /ia-compound. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after non-trivial debugging to create validated solution notes, post-mortems, and reusable knowledge in docs/solutions with YAML frontmatter and cross-references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated solution notes can accidentally include secrets, private URLs, customer data, or sensitive incident details. <br>
Mitigation: Preview the target path and summary before writing, then review and redact generated notes before committing or sharing them. <br>
Risk: Broad trigger wording may invoke the workflow when a resolved issue does not need durable documentation. <br>
Mitigation: Use the skill only for non-trivial fixes where future sessions would benefit, and skip simple typos, obvious syntax errors, or immediately corrected issues. <br>
Risk: Incomplete context can produce misleading documentation or incorrect frontmatter classification. <br>
Mitigation: Collect module, symptom, investigation attempts, root cause, solution, and prevention before writing; block on missing critical context and validate YAML frontmatter before creating the file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iliaal/compound-eng-compound-docs) <br>
- [Documentation Capture Process](references/documentation-process.md) <br>
- [YAML Frontmatter Schema](references/yaml-schema.md) <br>
- [Quality Guidelines & Error Handling](references/quality-guidelines.md) <br>
- [Example Scenario](references/example-scenario.md) <br>
- [Resolution Template](assets/resolution-template.md) <br>
- [Critical Pattern Template](assets/critical-pattern-template.md) <br>
- [Frontmatter Validator](scripts/validate-frontmatter.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, code examples, and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local docs/solutions files after context gathering, schema validation, and user confirmation where required.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
