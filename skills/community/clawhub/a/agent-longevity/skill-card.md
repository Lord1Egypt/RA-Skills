## Description: <br>
Agent Longevity helps long-running autonomous agents diagnose and reduce degradation patterns such as output homogeneity, circular value reasoning, memory bloat, perception waste, and inner-loop suffocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[citriac](https://clawhub.ai/user/citriac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of long-running autonomous agents use this skill to audit degradation patterns, tune perception scheduling, structure memory tiers, and log decisions so agents remain inspectable over extended operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local decision logs may contain sensitive agent context. <br>
Mitigation: Scope AGENT_DATA_DIR to a private agent data folder and review or rotate logs if they may contain sensitive context. <br>
Risk: Operators who cannot review the Chinese reference material may miss implementation caveats. <br>
Mitigation: Provide an English or bilingual summary before operational use. <br>


## Reference(s): <br>
- [Anti-Homogenization](artifact/references/anti_homogenization.md) <br>
- [Memory Architecture](artifact/references/memory_architecture.md) <br>
- [Perception Scheduling](artifact/references/perception_scheduling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSONL decision logs under AGENT_DATA_DIR when scripts are run.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
