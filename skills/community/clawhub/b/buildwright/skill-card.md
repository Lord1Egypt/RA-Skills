## Description: <br>
Lightweight engineering workflow for agent-led development. Provides plan, work, verify, ship, and analyse commands with TDD, documentation discipline, security review, code review, and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunakkathuria](https://clawhub.ai/user/raunakkathuria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Buildwright to guide agent-led feature work, verification, code review, security review, documentation updates, and shipping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shipping workflow can commit, push, and open a pull request. <br>
Mitigation: Use it only with repository credentials and branch protections appropriate for the project, and review staged changes before shipping. <br>
Risk: Agent-generated code, documentation, or review guidance can be incorrect or misaligned with repository practices. <br>
Mitigation: Review the generated .buildwright steering files, run the verify workflow, and inspect generated changes before relying on them. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/raunakkathuria/buildwright) <br>
- [ClawHub skill page](https://clawhub.ai/raunakkathuria/skills/buildwright) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, file paths, and implementation changes when the selected workflow calls for them] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project documentation, steering files, code changes, commits, and pull requests when the selected workflow calls for them.] <br>

## Skill Version(s): <br>
0.0.17 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
