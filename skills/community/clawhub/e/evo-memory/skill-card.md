## Description: <br>
Evo Memory provides a self-evolving agent memory system with permanent principles, reusable experience patterns, signal capture, and scheduled reflection for continuous learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiran71](https://clawhub.ai/user/weiran71) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Evo Memory to preserve durable principles, reusable lessons, and reflection notes across agent sessions. It is suited for workflows where the agent should learn from corrections, failures, preferences, and explicit review requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs always-on local hooks that can persist conversation and command-failure signals. <br>
Mitigation: Review the hook scripts before enabling them, decide what may be stored, and avoid using the skill around secrets or sensitive projects. <br>
Risk: Stored memory files may accumulate incorrect, outdated, or sensitive entries over time. <br>
Mitigation: Regularly inspect and prune pending.jsonl, principles.md, patterns/, citation logs, and the self-evolution bootstrap hook. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weiran71/evo-memory) <br>
- [Setup guide](artifact/setup.md) <br>
- [Permanent principles](artifact/principles.md) <br>
- [Experience pattern index](artifact/patterns/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSONL memory entries, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local memory, citation logs, and pending signal records under the configured self-evolution workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
