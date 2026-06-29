## Description: <br>
Continuous Dev Loop provides a governed development loop with roadmap, budget, ledger, and understanding-debt controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeyapu](https://clawhub.ai/user/modeyapu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run restartable repository development rounds, each limited to one verified slice with durable state and an explicit continue, stop, or block decision. It is intended for established development directions, not initial product strategy or open-ended brainstorming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to maintain loop state files and run normal project verification commands in a repository. <br>
Mitigation: Confirm the intended continuity files and allowed verification commands before use; reuse repo-native state where it exists. <br>
Risk: Repo-local policy may enable commits, pushes, hooks, or multi-agent writes with broader impact. <br>
Mitigation: Keep those actions explicitly authorized, scoped, and reviewed before execution. <br>


## Reference(s): <br>
- [Footer Contract](references/footer-contract.md) <br>
- [Multi-Agent Governance](references/multi-agent-governance.md) <br>
- [Precision Overview](references/precision-overview.md) <br>
- [Precision Profiles](references/precision-profiles.md) <br>
- [Precision Review Pipeline](references/precision-review-pipeline.md) <br>
- [Precision Runtime Compatibility](references/precision-runtime-compatibility.md) <br>
- [Repo Policy Profiles](references/repo-policy-profiles.md) <br>
- [Runtime Compatibility](references/runtime-compatibility.md) <br>
- [Stop Governance](references/stop-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with a machine-readable footer and optional JSON or Markdown state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One bounded development slice per round; continuation state is persisted in repo-native or supervisor-owned files.] <br>

## Skill Version(s): <br>
6.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
