## Description: <br>
Response speed optimizer - implements reply-first-then-process, parallel tool calls, and memory file caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opendolph](https://clawhub.ai/user/opendolph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce perceived response latency by acknowledging requests quickly, running independent work in parallel, and caching workspace memory/state files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill caches local agent memory and state files in the workspace, which may retain sensitive context. <br>
Mitigation: Install only in workspaces where this caching is acceptable, and use an opt-in setup with a clear way to clear or disable the cache. <br>
Risk: The skill includes a helper for executing shell commands in parallel, which can run broad local commands if exposed without review. <br>
Mitigation: Review or remove the shell-command helper before use, and limit execution to trusted commands and workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opendolph/fast-response-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and command-line usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional Node.js helper scripts for cache management and parallel task execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
