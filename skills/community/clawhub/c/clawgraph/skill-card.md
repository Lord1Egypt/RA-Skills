## Description: <br>
Automatically store explicit durable user facts and recall them later; do not infer or upgrade weak signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawgraphai](https://clawhub.ai/user/clawgraphai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use ClawGraph to store durable user, project, team, and preference facts in a persistent knowledge graph and query those facts in later conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain personal, client, or confidential facts beyond the current session. <br>
Mitigation: Store only explicit durable facts, avoid sensitive details unless the user is comfortable with local storage and provider processing, and periodically inspect exported memory. <br>
Risk: Fact extraction uses the configured OpenAI-compatible provider and requires an API key. <br>
Mitigation: Use an approved provider configuration, prefer a dedicated API key, and avoid sending regulated or confidential information unless that use is permitted. <br>


## Reference(s): <br>
- [ClawGraph ClawHub page](https://clawhub.ai/clawgraphai/clawgraph) <br>
- [ClawGraph homepage](https://github.com/clawgraph/clawgraph) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with shell and Python code blocks; CLI examples request JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawgraph CLI and OPENAI_API_KEY; memory is stored locally at ~/.clawgraph/data.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
