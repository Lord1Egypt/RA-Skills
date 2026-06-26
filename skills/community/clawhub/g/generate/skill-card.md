## Description: <br>
Generate random test data including text, numbers, UUIDs, and structured formats. Use when creating mock datasets, sample records, or randomized test inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate mock text, numbers, UUIDs, dates, names, emails, addresses, JSON, CSV, and other randomized sample data for testing and development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local generation history at ~/.generate/data.jsonl. <br>
Mitigation: Install only where this local history file is acceptable, and review or delete the file when generated data should not persist. <br>
Risk: The csv --output option writes to a user-provided path and can overwrite existing files. <br>
Mitigation: Use explicit non-sensitive output paths and check for existing files before running CSV export commands. <br>
Risk: The password command produces test strings and is not recommended for real credentials. <br>
Mitigation: Use a dedicated password manager or approved secrets workflow for real credentials. <br>


## Reference(s): <br>
- [Generate on ClawHub](https://clawhub.ai/bytesagain3/generate) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples; generated command output may be plain text, JSON, CSV, UUIDs, dates, names, emails, addresses, or passwords.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands write generation history to ~/.generate/data.jsonl, and csv --output writes CSV data to a user-provided path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
