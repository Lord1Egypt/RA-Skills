## Description: <br>
Autoresearch helps AI agents run systematic, metric-driven experiments by changing configured files, executing configured commands, recording results, and keeping or discarding changes based on measured outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Autoresearch to automate iterative optimization work, such as hyperparameter searches, ablation studies, performance tuning, and other tasks with a clear metric and constrained editable files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly edit code, run commands, and reset Git state during experiment loops. <br>
Mitigation: Use it only in a clean disposable branch or worktree, commit or back up local work first, and avoid automatic hard resets unless loss of uncommitted changes is acceptable. <br>
Risk: Unbounded experiment loops can consume time, compute, disk, or spawned agent sessions. <br>
Mitigation: Set explicit maximum experiment counts, total runtime, per-run timeouts, resource limits, and whether spawned sessions are allowed before starting. <br>
Risk: Poorly scoped experiments can modify files or run commands outside the intended search space. <br>
Mitigation: Define explicit writable files, read-only files, allowed commands, metric extraction, and constraints in the setup configuration. <br>


## Reference(s): <br>
- [Autoresearch Reference](artifact/reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/thomas-security/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration files, shell commands, code edits, git commits, and tab-separated experiment results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create autoresearch.config.md and results.tsv; experiment behavior depends on user-defined metric, target files, commands, limits, and constraints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
