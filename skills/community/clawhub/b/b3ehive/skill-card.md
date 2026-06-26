## Description: <br>
Runs three AI agents in parallel to implement, cross-evaluate, score, and select a code solution for a coding task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiyangzen](https://clawhub.ai/user/weiyangzen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use B3ehive to run three competing coding agents with different focuses, compare their outputs through structured evaluation, and deliver a selected implementation with markdown rationale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can present a fixed placeholder winner as an objectively selected best solution. <br>
Mitigation: Review all generated implementations, scorecards, and rationale manually before relying on the selected output. <br>
Risk: The release may be a prototype or template because the server security guidance notes a missing CLI entry point. <br>
Mitigation: Verify the executable entry point and run the phase scripts in a controlled workspace before use. <br>


## Reference(s): <br>
- [B3ehive ClawHub listing](https://clawhub.ai/weiyangzen/b3ehive) <br>
- [Technical specification](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Workspace files including runnable code, markdown comparison reports, scorecards, and decision rationale] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates phase-based workspace directories and markdown reports for review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
