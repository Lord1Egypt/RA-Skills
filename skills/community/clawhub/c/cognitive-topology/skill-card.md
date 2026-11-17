## Description:

Cognitive Topology helps an agent split complex tasks into independent analysis branches, collect L2 markdown results, and synthesize the branch conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushang555](https://clawhub.ai/user/qiushang555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-branch analysis for complex tasks that benefit from parallel perspectives and explicit synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task and branch content may be retained in long-term OpenClaw memory.

Mitigation: Avoid running the skill on secrets or sensitive private data unless archival behavior is disabled, reviewed, or explicitly approved.

Risk: Topology JSON can point to branch files outside the expected branch directory.

Mitigation: Require path validation so L2 files are contained under the intended cognitive-topology branches directory before integration or archival.

Risk: Branch-style workflows can multiply incorrect assumptions if the initial task split is poor.

Mitigation: Review branch prompts and the synthesized result before relying on the final analysis.

## Reference(s):

- [Cognitive Topology reference guide](artifact/references/topology-guide.md)
- [ClawHub skill page](https://clawhub.ai/qiushang555/skills/cognitive-topology)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated topology, branch, memory, and synthesis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses branch L2 markdown files and a synthesis markdown file as intermediate and final artifacts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
