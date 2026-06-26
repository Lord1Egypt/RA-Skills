## Description: <br>
Clawng Term Memory version-controls OpenClaw agent identity, memory, operating rules, and installed skills in git, with commands to commit, push, inspect history, diff files, revert changes, and gather multi-agent memories for synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidharket](https://clawhub.ai/user/davidharket) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to persist and restore agent memory across machines by committing core knowledge files to a private GitHub repository. It also supports multi-machine memory collection for a daily synthesis workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up agent memory, rules, identity files, and installed skills to a GitHub repository, which can expose sensitive agent context if the repository or credentials are misconfigured. <br>
Mitigation: Use a private repository, least-privilege SSH or repo-scoped credentials, review diffs before pushing, and keep secrets out of tracked files. <br>
Risk: Automatic commit, push, and synthesis workflows can preserve or propagate incorrect or sensitive memory with limited review safeguards. <br>
Mitigation: Require human review for staged changes and avoid the automatic merge or synthesis flow until review controls are in place. <br>
Risk: The merge workflow writes collected memory to /tmp and prints it to stdout, which can disclose memory contents on shared or logged systems. <br>
Mitigation: Run the merge workflow only in trusted environments, restrict access to logs and temporary files, and clean up staging output after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidharket/clawng-term-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; shell scripts produce git commits, git history output, and memory staging text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May commit and push tracked OpenClaw knowledge files and write aggregated MEMORY.md contents to /tmp for synthesis.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
