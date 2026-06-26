## Description: <br>
Cognitive discipline for AI-native scientific experimentation: it helps agents set up controlled experiments, design reproducible evaluation pipelines, and structure long-running research workspaces with governance guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhelunsun](https://clawhub.ai/user/zhelunsun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and research agents use this skill to structure AI-native experiments with reproducible workflows, controlled baselines, evidence status, validation gates, and claim-safe handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence an agent to create or modify research repo structure, manifests, validators, checkpoints, proposals, and experiment records. <br>
Mitigation: Review those agent-written changes before relying on them, especially before costly model experiments or use with sensitive unpublished work. <br>
Risk: Research outputs may be overclaimed if candidate evidence, failed runs, or changed baselines are not reviewed. <br>
Mitigation: Use the skill's evidence status, protected-surface proposal process, calibration gate, and claim-safe memo before scaling or publishing findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhelunsun/ai-research-harness) <br>
- [Agent Harness Engineering project page](https://picrew.github.io/LLM-Harness/) <br>
- [Repo Architecture & Governance](references/repo-architecture.md) <br>
- [Experiment Design Methodology](references/experiment-design.md) <br>
- [Scoring & Statistics](references/scoring-statistics.md) <br>
- [Scientific Thinking Patterns for AI-Conducted Research](references/scientific-thinking.md) <br>
- [Agent Collaboration & Governance](references/agent-collaboration.md) <br>
- [Methodology Grounding for Research Design](references/methodology-grounding.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with optional file templates, validation commands, manifests, schemas, and experiment records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not include executable code or hidden data access.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
