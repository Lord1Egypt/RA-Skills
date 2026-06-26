## Description: <br>
Exports filtered Git and SVN commit histories for selected authors, date ranges, revision ranges, and repository paths into Markdown, CSV, JSON, or detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallaceliang](https://clawhub.ai/user/wallaceliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to collect commit history and change details from Git or SVN repositories they are authorized to inspect. It supports contribution summaries, audit preparation, migration review, and documentation of repository activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The export scripts use shell eval with user-supplied inputs. <br>
Mitigation: Review and patch the scripts to use safely quoted argument arrays before running them in sensitive environments. <br>
Risk: SVN examples allow passwords to be supplied on the command line. <br>
Mitigation: Use SVN authentication caching or another secret-handling mechanism instead of passing passwords as command arguments. <br>
Risk: Exported reports can contain personal data and internal repository details. <br>
Mitigation: Treat generated reports as sensitive, restrict access, and run the skill only on repositories the user is authorized to inspect. <br>


## Reference(s): <br>
- [Git command reference](references/git_commands.md) <br>
- [SVN command reference](references/svn_commands.md) <br>
- [SVN working-copy database query guide](references/svn_database_query.md) <br>
- [SlikSVN command-line tools](https://sliksvn.com/download/) <br>
- [VisualSVN downloads](https://www.visualsvn.com/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated reports may be Markdown, CSV, JSON, or detailed text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include names, emails, commit messages, changed file paths, revision identifiers, and repository paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
