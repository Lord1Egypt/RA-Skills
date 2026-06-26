## Description: <br>
Intrinsic curiosity-driven continuous learning: detect gaps between expected and actual results, treat them as curiosity signals, and update skills accordingly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guiguid](https://clawhub.ai/user/guiguid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn result deltas, repeated corrections, missing knowledge, and periodic scans into structured research, integration, and curriculum-building loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent learning logs and long-term self-improvement records. <br>
Mitigation: Review the delta log before use and avoid storing sensitive or unnecessary information in persistent records. <br>
Risk: The skill can fetch configured external sources during knowledge scans. <br>
Mitigation: Use only trusted scan sources and avoid background or cron scanning unless explicitly approved. <br>
Risk: The skill may propose skill patches, new skills, or memory writes as part of integration. <br>
Mitigation: Require manual approval and review for any skill patch, skill creation, or memory write. <br>


## Reference(s): <br>
- [Curiosity Loop ClawHub listing](https://clawhub.ai/guiguid/curiosity-loop) <br>
- [Key Concepts - Flowers Lab, INRIA](references/flowers-lab-concepts.md) <br>
- [Flowers Lab, INRIA](https://www.robots.org/flowers-lab/) <br>
- [Flowers INRIA YouTube channel](https://www.youtube.com/channel/UCrBNVs3u3mwlRsm2v3EKuXA) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent delta logs, source scans, skill updates, or memory writes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
