## Description: <br>
Advanced repository analysis and refactoring guide that identifies technical debt and architectural anti-patterns using AI reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit local git repositories for complexity, technical debt, possible logic leaks, and opportunities for agent-native refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects the repository path supplied by the user, which may include secrets, sensitive code, or sensitive history. <br>
Mitigation: Run it only on a narrowly selected repository path and remove secrets or sensitive history before use when needed. <br>
Risk: The invocation has a disclosed paid cost. <br>
Mitigation: Confirm the 0.10 USDC fee on the Base network before running the skill. <br>
Risk: Repository audit and refactoring guidance may be incomplete or unsuitable for a specific codebase. <br>
Mitigation: Review recommendations before applying changes and validate any proposed refactor with normal tests and code review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tmstudio667-commits/agent-git-oracle) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/tmstudio667-commits) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with repository analysis, refactoring recommendations, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository-specific recommendations; no files are produced by the skill text itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
