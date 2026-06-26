## Description: <br>
Autoresearch helps agents set up and run autonomous neural network training experiments by editing training code, launching fixed-budget runs, evaluating metrics, and recording results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiyunrei2025](https://clawhub.ai/user/baiyunrei2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML researchers use this skill to run autonomous, iterative neural network experiments on a single NVIDIA GPU. The skill guides setup, baseline execution, code changes to training logic, experiment runs, metric extraction, and result logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The autonomous experiment loop can continue editing code and running GPU jobs indefinitely unless manually stopped. <br>
Mitigation: Run it only in a disposable clone, branch, container, or dedicated worktree with explicit limits for runtime, experiment count, GPU or cloud budget, and disk usage. <br>
Risk: The workflow can mutate repository state through code edits, commits, and resets. <br>
Mitigation: Use a dedicated experiment branch or worktree, review git state before and after runs, and decide in advance whether git reset is allowed. <br>
Risk: The setup depends on remote dependencies, data, and kernel sources that affect trust and reproducibility. <br>
Mitigation: Review dependency and remote kernel provenance, use trusted package indexes and dataset sources, and protect the local autoresearch cache from untrusted writes. <br>


## Reference(s): <br>
- [ClawHub Autoresearch release](https://clawhub.ai/baiyunrei2025/autoresearch-karpathy) <br>
- [Original autoresearch project](https://github.com/karpathy/autoresearch) <br>
- [Nanochat implementation](https://github.com/karpathy/nanochat) <br>
- [Climbmix dataset](https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [Project announcement](https://x.com/karpathy/status/2029701092347630069) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, code edits, TSV result entries, and experiment summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify training code, logs, experiment records, and git commits during autonomous experimentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
