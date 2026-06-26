## Description: <br>
This skill guides an agent to search and retrieve local files and documents indexed by Gety using the gety CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujfsd](https://clawhub.ai/user/lujfsd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent operators use this skill to locate local files, inspect search results, retrieve specific indexed documents, and manage Gety indexing connectors through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches and document retrieval can reveal contents from local folders indexed by Gety. <br>
Mitigation: Review which folders Gety indexes, keep search requests specific, and require confirmation before fetching full document text or changing indexed folders. <br>


## Reference(s): <br>
- [Gety CLI reference](references/gety_cli.md) <br>
- [ClawHub skill page](https://clawhub.ai/lujfsd/gety-local-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise search-result summaries, connector scope guidance, and exit-code handling advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
