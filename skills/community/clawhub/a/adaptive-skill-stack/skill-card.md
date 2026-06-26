## Description: <br>
Adaptive Skill Stack is a self-evolving meta-skill that analyzes each request, combines existing capabilities or builds new ones, and records reusable methods in its support files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they want an agent to adapt across mixed-domain tasks, track reusable capabilities, and maintain evolving registries, protocols, knowledge files, templates, or helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist task-derived capabilities and may store information from user tasks in registry, protocol, knowledge, template, or script files. <br>
Mitigation: Avoid using it with secrets or confidential task details unless persistence is acceptable, and review proposed support-file changes before keeping them. <br>
Risk: The skill can change support files after use, so its behavior may evolve over time without clear per-change approval. <br>
Mitigation: Use version control or a clean workspace, inspect diffs after each task, and require explicit approval before retaining behavior-changing updates. <br>
Risk: Generated or accumulated scripts and templates could introduce incorrect, unsafe, or misleading behavior. <br>
Mitigation: Review and scan generated files before execution or deployment, and run new scripts only after confirming their inputs, outputs, and file-write scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/adaptive-skill-stack) <br>
- [Capability registry](references/capability-registry.md) <br>
- [Adaptive stacking protocols](references/protocols.md) <br>
- [Knowledge file conventions](references/knowledge/README.md) <br>
- [Script library conventions](scripts/README.md) <br>
- [Template library conventions](assets/templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional code blocks and generated or updated skill support files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append or update registry, protocol, knowledge, template, and script files as task-derived capabilities are accumulated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
