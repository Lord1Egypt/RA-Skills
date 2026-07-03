## Description: <br>
This skill checks PDF, Word, and Excel files for sensitive or prohibited words from a built-in or external word library and highlights matched content in yellow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[betty831221](https://clawhub.ai/user/betty831221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external reviewers, and document compliance teams use this skill to scan local documents for built-in or custom sensitive-word lists and produce highlighted copies for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes highlighted output files and could overwrite an original document if the output directory and filename collide. <br>
Mitigation: Use an explicit output directory and keep original documents in a separate location before running the checker. <br>
Risk: The built-in and custom word lists may miss context-specific sensitive terms or flag benign partial matches. <br>
Mitigation: Review the highlighted output and update the custom word list for the organization or document set being checked. <br>


## Reference(s): <br>
- [Usage Guide](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/betty831221/skills/cmt-1-0) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Highlighted PDF, Word, or Excel files with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local documents and writes annotated output files, usually to the Desktop unless an explicit output directory is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
