## Description: <br>
Benchmark CPU, memory, disk I/O, and network on your system when measuring server performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to run basic local CPU, memory, disk I/O, and network checks when measuring server performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disk and network benchmarks can write test files or contact external hosts outside the user's intended scope. <br>
Mitigation: Run the skill only in a scratch directory and only against network hosts the user intends to contact. <br>
Risk: The compare command can expose differences from sensitive files. <br>
Mitigation: Use compare only with non-sensitive files that are safe to show in the agent conversation. <br>
Risk: The security review marked this release suspicious because of unscoped disk, network, and file comparison behavior. <br>
Mitigation: Review the commands before installation and execute them in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/benchmark-tool) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Benchmark results may depend on host resources, selected disk path, and selected network host.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release, SKILL.md frontmatter, script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
