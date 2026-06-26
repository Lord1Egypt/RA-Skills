## Description: <br>
Autonomous Research Loop runs a recurring self-directed research workflow that generates topics, performs research, and creates Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloryjack](https://clawhub.ai/user/gloryjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators use this skill to run an autonomous background research loop that maintains a topic pool, generates new research, and posts outputs to Feishu. It is intended for Linux environments with the required Feishu destination and scheduling setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous background execution can continue generating research work without daily or total limits. <br>
Mitigation: Require a documented stop or removal process and daily or total run limits before enabling the loop. <br>
Risk: Research documents may be posted to Feishu without explicit approval or clear account scoping. <br>
Mitigation: Require explicit approval before Feishu posting and use least-privilege Feishu credentials tied to a known destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloryjack/autonomous-research-loop) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gloryjack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown research brief and Feishu document content with optional Python code blocks and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a recurring background loop; outputs may be posted to Feishu without approval if enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
