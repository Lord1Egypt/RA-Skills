## Description: <br>
Context Mode helps agents research and analyze multiple sources by fetching, indexing, batch processing, and searching content without loading large raw inputs into context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to decide when to fetch, index, batch process, and search multi-source material while keeping agent responses concise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use ctx_* command execution tools during research workflows. <br>
Mitigation: Review generated commands before running them and keep command use read-only unless changes are explicitly approved. <br>
Risk: The skill can index fetched or local content for repeated search. <br>
Mitigation: Avoid indexing private or sensitive material unless storage and deletion behavior are understood. <br>
Risk: The skill depends on ctx_* tools available in the agent environment. <br>
Mitigation: Install and use it only in environments where those tools are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/context-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown guidance with tool-use recommendations, search summaries, analysis, and example shell-style commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for repeated retrieval over indexed sources; command and indexing behavior depends on trusted ctx_* tools in the agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
