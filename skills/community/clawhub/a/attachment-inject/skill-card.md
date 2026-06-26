## Description: <br>
Attachment Inject helps agents inject dynamic content as attachment-style context instead of embedding it directly in the system prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to reduce prompt bloat and preserve prompt caching by loading or injecting dynamic skill, agent, and memory context only when needed. It provides patterns for on-demand reads, lightweight registry files, and placeholder-based injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes reading local agent and skill files and generating registry content, which can expose or propagate private workspace information if pointed at the wrong paths. <br>
Mitigation: Review the target paths and generated registry output before use, and keep reads limited to intended workspace files. <br>
Risk: Registry entries or dynamic injection placeholders can become stale or misleading if generated from incomplete or untrusted metadata. <br>
Mitigation: Regenerate registries from trusted skill and agent definitions and review concise descriptions before injecting them into prompts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
