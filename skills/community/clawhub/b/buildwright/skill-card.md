## Description: <br>
Lightweight engineering workflow for agent-led development. Provides plan, work, verify, ship, and analyse commands with TDD, documentation discipline, security review, code review, and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunakkathuria](https://clawhub.ai/user/raunakkathuria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Buildwright to guide agent-led repository work, including planning, implementation, verification, documentation, review, and shipping. It can also analyze brownfield codebases and create project steering documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify repository files and ship code using configured git and GitHub credentials. <br>
Mitigation: Review generated files before accepting them, and use /bw-ship only when ready for commit, push, and PR creation. <br>
Risk: Generated implementation, documentation, or steering files may be incorrect or unsuitable for the target repository. <br>
Mitigation: Run the configured quality gates and review generated changes before merging or publishing. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/raunakkathuria/buildwright) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance, Markdown documents, code changes, shell commands, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update repository files and run configured quality and security workflows when requested.] <br>

## Skill Version(s): <br>
0.0.16 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
