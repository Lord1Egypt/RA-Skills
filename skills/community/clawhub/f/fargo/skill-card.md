## Description: <br>
FargoRate helps agents look up pool player ratings, FargoRate IDs, match odds, race recommendations, handicaps, rankings, and rating changes using the fargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rgstephens](https://clawhub.ai/user/rgstephens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer pool-rating and handicap questions by selecting appropriate fargo CLI commands and interpreting results. It can also guide optional local SQLite tracking of player rating changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Homebrew install path uses an external fargo CLI from a third-party tap. <br>
Mitigation: Install only from the server-resolved publisher's tap when trusted, and review the CLI before running it in sensitive environments. <br>
Risk: The optional local SQLite database and change outputs can contain player history and manually added contact details. <br>
Mitigation: Keep database files local and avoid forwarding --changes or --json output to logs, bots, or shared channels unless those fields are acceptable to disclose. <br>


## Reference(s): <br>
- [ClawHub FargoRate Skill Page](https://clawhub.ai/rgstephens/fargo) <br>
- [FargoRate Skill Repository](https://github.com/rgstephens/fargo-skill) <br>
- [FargoRate](https://fargorate.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw JSON examples and local SQLite database guidance when --json or --db are used.] <br>

## Skill Version(s): <br>
0.4.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
