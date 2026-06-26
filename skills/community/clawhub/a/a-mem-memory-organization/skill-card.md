## Description: <br>
Organize project, agent, or user memory using an A-MEM-style workflow with structured notes, semantic tags, contextual summaries, explicit links, and lightweight memory evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create durable memory notes, retrieve relevant historical context, link related observations, and refine memory conservatively over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory can retain secrets, sensitive personal data, or outdated context if users save it without review. <br>
Mitigation: Review notes before persistence, avoid storing secrets or sensitive personal data, and periodically prune memory files. <br>
Risk: Overbroad tags, weak links, or unnecessary rewrites can pollute retrieval and make future memory less reliable. <br>
Mitigation: Keep notes atomic, use precise keywords and stable tags, link only concrete relationships, and update older notes only when confidence is high. <br>


## Reference(s): <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaocaijic/a-mem-memory-organization) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or JSON note structures with concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update durable memory files using explicit note fields and conservative links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
