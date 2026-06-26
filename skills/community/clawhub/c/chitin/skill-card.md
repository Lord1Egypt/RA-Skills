## Description: <br>
Personality persistence for AI agents. Remember how you think, not just what happened. Structured insights that survive session restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Chitin to maintain structured behavioral, relational, principle, skill, and trigger insights across AI agent sessions. It helps agents retrieve compact personality context, reflect after sessions, and optionally share vetted insights with Carapace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent personality insights can contain sensitive personal, relational, or behavioral information if users add it. <br>
Mitigation: Review stored insights and triggers regularly, and do not store secrets or private details as insights. <br>
Risk: Embedding, semantic search, or Carapace sharing commands may send selected insight text or queries off-machine. <br>
Mitigation: Use embedding and Carapace commands only with data you are comfortable sending to external services. <br>
Risk: Global npm installation runs package code in the user's environment. <br>
Mitigation: Verify the npm package before global install and install only when persistent behavioral profiling is desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/morpheis/chitin) <br>
- [npm Package: @clawdactual/chitin](https://www.npmjs.com/package/@clawdactual/chitin) <br>
- [Project Homepage](https://github.com/Morpheis/chitin) <br>
- [Carapace](https://carapaceai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON retrieval output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core operations use a local SQLite database; retrieval output can be budgeted for compact agent context.] <br>

## Skill Version(s): <br>
1.4.5 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
